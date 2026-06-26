#!/usr/bin/env python3
"""
知识库自动修复脚本生成器
根据检测结果生成可执行的修复脚本
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import shlex  # 用于命令行转义


def quote_path(path: str) -> str:
    """安全地转义文件路径，防止命令注入"""
    return shlex.quote(path)


def generate_fix_script(results: Dict, output_path: str = None) -> str:
    """生成自动修复脚本"""

    if output_path is None:
        timestamp = datetime.now().strftime('%Y%m%d-%H%M')
        output_path = f'auto-fix-{timestamp}.sh'

    script_lines = [
        '#!/bin/bash',
        f'# 知识库自动修复脚本',
        f'# 生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        f'# 知识库路径：{results["scan_path"]}',
        f'# 健康分：{results["scores"]["total_score"]}',
        '',
        '# ⚠️ 警告：执行前请仔细审查！',
        '# 此脚本会删除、修改文件，建议先备份知识库',
        '',
        'set -e  # 遇到错误立即停止',
        '',
        'echo "开始修复知识库..."',
        '',
    ]

    fix_count = 0

    # 1. 处理空壳文件
    if results['empty_files']:
        script_lines.append('# ===== 1. 删除空壳文件 =====')
        script_lines.append('# 建议：删除无意义的占位文件，保留有框架结构的文件')
        script_lines.append('')

        for item in results['empty_files']:
            file_path = Path(results['scan_path']) / item['file']
            issues = item['issues']
            quoted_file = quote_path(item['file'])

            # 判断是否建议删除
            if '占位符' in issues or ('内容过短' in issues and item['size'] < 50):
                script_lines.append(f'# 删除空壳：{item["file"]}')
                script_lines.append(f'# 原因：{", ".join(issues)}')
                script_lines.append(f'rm {quoted_file}')
                script_lines.append('')
                fix_count += 1
            else:
                script_lines.append(f'# ⚠️ 保留但需补充：{item["file"]}')
                script_lines.append(f'# 原因：{", ".join(issues)}')
                script_lines.append(f'# 建议：补充定义/方法/案例内容')
                script_lines.append('')

    # 2. 修复断链
    if results['broken_links']:
        script_lines.append('# ===== 2. 修复断链 =====')
        script_lines.append('# 策略：搜索相似文件名，推荐替换目标')
        script_lines.append('')

        # 构建文件索引，用于相似文件名搜索
        existing_files = list(set(
            [Path(f).stem for f in results.get('all_files', [])]
        ))

        for item in results['broken_links']:
            target = item['target']
            source = item['source']
            quoted_source = quote_path(source)
            quoted_target = quote_path(target)

            # 简单的相似文件名搜索
            similar = find_similar_filename(target, existing_files)

            if similar:
                quoted_similar = quote_path(similar)
                script_lines.append(f'# 修复断链：{source}')
                script_lines.append(f'# 原目标：[[{target}]]')
                script_lines.append(f'# 建议替换：[[{similar}]]')
                script_lines.append(f'sed -i \'\' \'s/\\[\\[{target}\\]\\]/[[{similar}]]/g\' {quoted_source}')
                script_lines.append('')
                fix_count += 1
            else:
                script_lines.append(f'# ❌ 无法自动修复：{source}')
                script_lines.append(f'# 目标不存在：[[{target}]]')
                script_lines.append(f'# 建议：手动创建目标文件或删除链接')
                script_lines.append('')

    # 3. 处理孤立节点
    if len(results['isolated_nodes']) > 5:
        script_lines.append('# ===== 3. 处理孤立节点 =====')
        script_lines.append('# 策略：建议整合或删除无连接的文件')
        script_lines.append('')

        for node in results['isolated_nodes'][:10]:
            script_lines.append(f'# 孤立文件：{node}')
            script_lines.append(f'# 建议：添加到相关主题或归档删除')
            script_lines.append(f'# rm "{node}.md"  # 取消注释以删除')
            script_lines.append('')

    # 4. 拆分过长文件
    script_lines.append('# ===== 4. 拆分过长文件（需手动执行）=====')
    script_lines.append('# 发现过长的文件建议按H2标题拆分')
    script_lines.append('')

    for item in results.get('density_stats', []):
        if '过长' in item['status']:
            script_lines.append(f'# 过长文件：{item["file"]}（{item["char_count"]}字符）')
            script_lines.append(f'# 建议：python3 scripts/split_long_file.py "{item["file"]}" --by-h2')
            script_lines.append('')

    # 总结
    script_lines.extend([
        '',
        'echo "修复完成！"',
        f'echo "已处理 {fix_count} 个问题"',
        'echo "请review更改后commit"',
        '',
        '# 提示：运行 git diff 查看所有更改'
    ])

    script_content = '\n'.join(script_lines)

    # 写入文件
    Path(output_path).write_text(script_content, encoding='utf-8')

    # 设置执行权限
    import os
    os.chmod(output_path, 0o755)

    print(f"修复脚本已生成：{output_path}")
    print(f"包含 {fix_count} 个自动修复项")

    return output_path


def find_similar_filename(target: str, existing_files: List[str]) -> str:
    """查找相似的文件名"""
    target_lower = target.lower()

    # 精确匹配（忽略大小写）
    for f in existing_files:
        if f.lower() == target_lower:
            return f

    # 包含匹配
    for f in existing_files:
        if target_lower in f.lower() or f.lower() in target_lower:
            return f

    # 词根匹配（简单实现）
    target_words = set(target_lower.replace('-', ' ').replace('_', ' ').split())
    for f in existing_files:
        file_words = set(f.lower().replace('-', ' ').replace('_', ' ').split())
        if target_words & file_words:  # 有交集
            return f

    return None


def generate_python_fix_script(results: Dict, output_path: str = None) -> str:
    """生成Python版本的修复脚本（更强大）"""

    if output_path is None:
        timestamp = datetime.now().strftime('%Y%m%d-%H%M')
        output_path = f'auto-fix-{timestamp}.py'

    script_content = f'''#!/usr/bin/env python3
"""
知识库自动修复脚本
生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
知识库路径：{results["scan_path"]}
健康分：{results["scores"]["total_score"]}
"""

import os
import shutil
from pathlib import Path

# 配置
KNOWLEDGE_BASE = "{results["scan_path"]}"
BACKUP_DIR = "backup_" + Path(KNOWLEDGE_BASE).name

def backup():
    """备份知识库"""
    if not os.path.exists(BACKUP_DIR):
        shutil.copytree(KNOWLEDGE_BASE, BACKUP_DIR)
        print(f"已备份到: {{BACKUP_DIR}}")
    else:
        print(f"备份已存在: {{BACKUP_DIR}}")

def fix_empty_files():
    """删除空壳文件"""
    empty_files = {json.dumps([item['file'] for item in results['empty_files']], ensure_ascii=False)}

    deleted = 0
    for file_path in empty_files:
        full_path = Path(KNOWLEDGE_BASE) / file_path
        if full_path.exists():
            print(f"删除空壳: {{file_path}}")
            # full_path.unlink()  # 取消注释以实际删除
            deleted += 1

    print(f"待删除空壳文件: {{deleted}}个")

def fix_broken_links():
    """修复断链"""
    # TODO: 实现断链修复逻辑
    print("断链修复需要手动处理")

def fix_isolated_nodes():
    """处理孤立节点"""
    isolated = {json.dumps(results['isolated_nodes'], ensure_ascii=False)}

    print(f"孤立节点: {{len(isolated)}}个")
    for node in isolated[:10]:
        print(f"  - {{node}}")

if __name__ == '__main__':
    print("开始修复知识库...")

    # 备份
    backup()

    # 执行修复
    fix_empty_files()
    fix_broken_links()
    fix_isolated_nodes()

    print("修复完成！请review更改后commit")
'''

    Path(output_path).write_text(script_content, encoding='utf-8')
    print(f"Python修复脚本已生成：{output_path}")

    return output_path


if __name__ == '__main__':
    import sys

    # 从JSON文件读取结果
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
        results = json.loads(Path(json_file).read_text(encoding='utf-8'))

        # 生成两种格式的脚本
        generate_fix_script(results)
        generate_python_fix_script(results)
    else:
        print("Usage: python auto_fix.py <results.json>")
