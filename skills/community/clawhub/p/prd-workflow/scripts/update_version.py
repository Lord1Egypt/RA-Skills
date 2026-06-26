#!/usr/bin/env python3
"""
版本更新辅助脚本 v2.0
从 workflows/version.js 读取版本信息，自动更新所有文件

用法：
    python3 update_version.py              # 从 version.js 读取版本，同步所有文件
    python3 update_version.py 4.2.0 "新功能"  # 更新版本号并同步
"""

import re
import json
import sys
import subprocess
from datetime import datetime
from pathlib import Path

def get_today():
    return datetime.now().strftime("%Y-%m-%d")

def read_version_js(file_path):
    """从 version.js 读取版本信息"""
    content = Path(file_path).read_text(encoding='utf-8')

    version = re.search(r"version:\s*'([^']+)'", content)
    release_date = re.search(r"releaseDate:\s*'([^']+)'", content)

    return {
        'version': version.group(1) if version else '1.0.0',
        'releaseDate': release_date.group(1) if release_date else get_today()
    }

def update_version_js(file_path, version, release_date=None):
    """更新 version.js 中的版本信息"""
    if release_date is None:
        release_date = get_today()

    content = Path(file_path).read_text(encoding='utf-8')

    # 更新版本号
    content = re.sub(r"version:\s*'[^']+'", f"version: '{version}'", content)
    # 更新发布日期
    content = re.sub(r"releaseDate:\s*'[^']+'", f"releaseDate: '{release_date}'", content)

    Path(file_path).write_text(content, encoding='utf-8')
    print(f"   ✅ workflows/version.js")

def add_changelog_entry(file_path, version, date, desc, detail, change_type='feature'):
    """在 version.js 的 changelog 数组顶部添加新条目"""
    content = Path(file_path).read_text(encoding='utf-8')

    # 构建新条目
    new_entry = f"""    {{
      version: '{version}',
      date: '{date}',
      type: '{change_type}',
      desc: '{desc}',
      detail: '{detail}'
    }},"""

    # 找到 changelog 数组的开始位置
    changelog_match = re.search(r'changelog:\s*\[', content)
    if changelog_match:
        # 检查是否已存在该版本
        if re.search(rf"version:\s*'{re.escape(version)}'", content):
            print(f"   ⚠️  version.js 中已存在 v{version}，跳过添加")
            return

        # 在 [ 后面插入新条目
        insert_pos = changelog_match.end()
        new_content = content[:insert_pos] + '\n' + new_entry + '\n' + content[insert_pos:]
        Path(file_path).write_text(new_content, encoding='utf-8')
        print(f"   ✅ workflows/version.js (添加版本历史)")

def update_version_history(file_path, version, changelog, date=None):
    """在版本历史表顶部插入新版本记录（如果不存在）"""
    if date is None:
        date = get_today()

    content = Path(file_path).read_text(encoding='utf-8')

    # 检查是否已存在该版本记录
    version_pattern = rf'\| \*\*v{re.escape(version)}\*\* \|'
    if re.search(version_pattern, content):
        # 已存在，更新该行的 changelog
        old_row_pattern = rf'(\| \*\*v{re.escape(version)}\*\* \| \*\*[\d-]+\*\* \| )([^\|]+)( \|)'
        new_row = f'| **v{version}** | **{date}** | **{changelog}** |'
        new_content = re.sub(old_row_pattern, new_row, content)
        if new_content != content:
            Path(file_path).write_text(new_content, encoding='utf-8')
            return True
        return False

    # 匹配版本历史表的模式
    pattern = r'(\| 版本 \| 日期 \| 变更内容 \|[\s\S]*?\|---+\|---+\|---+\|)'

    new_row = f'| **v{version}** | **{date}** | **{changelog}** |'

    def replacer(match):
        return match.group(1) + '\n' + new_row

    new_content = re.sub(pattern, replacer, content, count=1)

    if new_content != content:
        Path(file_path).write_text(new_content, encoding='utf-8')
        return True
    return False

def update_version_in_file(file_path, patterns):
    """更新文件中的版本号"""
    content = Path(file_path).read_text(encoding='utf-8')
    updated = False

    for pattern, replacement in patterns:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            content = new_content
            updated = True

    if updated:
        Path(file_path).write_text(content, encoding='utf-8')
    return updated

def main():
    project_dir = Path(__file__).parent.parent
    version_js_path = project_dir / "workflows" / "version.js"

    # 读取版本信息
    if len(sys.argv) >= 3:
        # 从命令行参数更新版本
        version = sys.argv[1]
        changelog_desc = sys.argv[2]
        changelog_detail = sys.argv[3] if len(sys.argv) >= 4 else changelog_desc
        date = get_today()

        print(f"🔧 更新版本到 {version}...")
        print(f"📝 Changelog: {changelog_desc}")
        print(f"📅 日期: {date}")
        print()

        # 更新 version.js
        update_version_js(version_js_path, version, date)
        add_changelog_entry(version_js_path, version, date, changelog_desc, changelog_detail)

    else:
        # 从 version.js 读取版本信息
        version_info = read_version_js(version_js_path)
        version = version_info['version']
        date = version_info['releaseDate']

        print(f"📋 同步版本信息...")
        print(f"   版本: v{version}")
        print(f"   日期: {date}")
        print()

    # 更新所有文件
    print("🔧 更新文件...")

    # 1. clawhub.json
    file_path = project_dir / "clawhub.json"
    if file_path.exists():
        data = json.loads(file_path.read_text(encoding='utf-8'))
        data['version'] = version
        data['meta']['releaseNotes'] = f"v{version}"
        file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        print(f"   ✅ clawhub.json")

    # 2. install.json
    file_path = project_dir / "install.json"
    if file_path.exists():
        data = json.loads(file_path.read_text(encoding='utf-8'))
        data['version'] = version
        file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        print(f"   ✅ install.json")

    # 3. _meta.json
    file_path = project_dir / "_meta.json"
    if file_path.exists():
        data = json.loads(file_path.read_text(encoding='utf-8'))
        data['version'] = version
        file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        print(f"   ✅ _meta.json")

    # 4. workflows/prd_template.js
    file_path = project_dir / "workflows" / "prd_template.js"
    if file_path.exists():
        update_version_in_file(file_path, [
            (r"this\.version = '[^']+'", f"this.version = '{version}'"),
        ])
        print(f"   ✅ workflows/prd_template.js")

    # 5. tests/test.js
    file_path = project_dir / "tests" / "test.js"
    if file_path.exists():
        update_version_in_file(file_path, [
            (r'测试套件 v[\d.]+', f'测试套件 v{version}'),
            (r"assertEqual\(template\.version, '[\d.]+'\)", f"assertEqual(template.version, '{version}')"),
        ])
        print(f"   ✅ tests/test.js")

    # 6. SKILL.md
    file_path = project_dir / "SKILL.md"
    if file_path.exists():
        update_version_in_file(file_path, [
            (r'\*\*版本\*\*:\s*v[\d.]+', f'**版本**: v{version}'),
            (r'\*\*更新日期\*\*:\s*[\d-]+', f'**更新日期**: {date}'),
            (r'\*\*技能版本\*\*:\s*[\d.]+', f'**技能版本**: {version}'),
        ])
        print(f"   ✅ SKILL.md")

    # 7. README.md
    file_path = project_dir / "README.md"
    if file_path.exists():
        update_version_in_file(file_path, [
            (r'# PRD Workflow v[\d.]+', f'# PRD Workflow v{version}'),
            (r'\*\*文档版本\*\*:\s*[\d.]+', f'**文档版本**: {version}'),
            (r'\*\*最后更新\*\*:\s*[\d-]+', f'**最后更新**: {date}'),
        ])
        print(f"   ✅ README.md")

    # 8. INSTALL.md
    file_path = project_dir / "INSTALL.md"
    if file_path.exists():
        update_version_in_file(file_path, [
            (r'\*\*技能版本\*\*:\s*[\d.]+', f'**技能版本**: {version}'),
            (r'\*\*更新日期\*\*:\s*[\d-]+', f'**更新日期**: {date}'),
            (r'\*\*最后更新\*\*:\s*[\d-]+', f'**最后更新**: {date}'),
        ])
        print(f"   ✅ INSTALL.md")

    # 9. workflows/main.js (从 version.js 读取，无需更新)

    # 10. workflows/ai_entry.js (从 version.js 读取，无需更新)

    print()
    print(f"✅ 所有文件已同步到 v{version}")
    print()
    print("💡 提示:")
    print("   - main.js 和 ai_entry.js 从 version.js 读取版本，无需手动更新")
    print("   - 下次发布只需运行: python3 scripts/update_version.py <版本号> <描述>")

if __name__ == '__main__':
    main()