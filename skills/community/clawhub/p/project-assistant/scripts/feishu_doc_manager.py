#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书文档集成管理器
与飞书 Skill 协作，生成文档更新建议（不直接修改）
"""

import json
import os
import sys
import subprocess
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

# Windows 控制台编码处理
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# 飞书文档配置键
FEISHU_CONFIG_KEYS = [
    "feishu.doc_token",      # 文档 token
    "feishu.folder_token",   # 文件夹 token
    "feishu.wiki_token",     # 知识库 token
    "feishu.doc_url",        # 文档 URL（便于查看）
]

# 文档变更类型
CHANGE_TYPES = {
    "api_added": "新增 API",
    "api_modified": "API 变更",
    "api_removed": "API 移除",
    "module_added": "新增模块",
    "module_modified": "模块变更",
    "module_removed": "模块移除",
    "config_changed": "配置变更",
    "structure_changed": "结构变更"
}

# 更新优先级
PRIORITY_LEVELS = {
    "high": "🔴 高优先级",
    "medium": "🟡 中优先级",
    "low": "🟢 低优先级"
}


def get_git_diff_files(project_dir: str) -> List[str]:
    """获取 Git 变更的文件列表"""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return [f for f in result.stdout.strip().split('\n') if f]
    except:
        pass
    return []


def get_git_log(project_dir: str, count: int = 5) -> List[Dict]:
    """获取最近的提交记录"""
    try:
        result = subprocess.run(
            ["git", "log", f"-{count}", "--pretty=format:%H|%s|%an|%ad", "--date=short"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            commits = []
            for line in result.stdout.strip().split('\n'):
                parts = line.split('|')
                if len(parts) >= 4:
                    commits.append({
                        "hash": parts[0][:12],
                        "message": parts[1],
                        "author": parts[2],
                        "date": parts[3]
                    })
            return commits
    except:
        pass
    return []


def analyze_changes(project_dir: str, changed_files: List[str]) -> List[Dict]:
    """分析变更内容，生成文档更新建议"""
    suggestions = []

    for file in changed_files:
        ext = os.path.splitext(file)[1].lower()

        # API 文件变更
        if 'api' in file.lower() or 'controller' in file.lower() or 'route' in file.lower():
            suggestions.append({
                "file": file,
                "type": "api_modified",
                "priority": "high",
                "suggestion": f"API 文件 `{file}` 有变更，建议更新 API 文档",
                "doc_section": "API 接口文档"
            })

        # 配置文件变更
        elif file in ['package.json', 'requirements.txt', 'pom.xml', 'build.gradle', 'CMakeLists.txt']:
            suggestions.append({
                "file": file,
                "type": "config_changed",
                "priority": "medium",
                "suggestion": f"配置文件 `{file}` 有变更，建议更新环境配置文档",
                "doc_section": "环境配置"
            })

        # README 变更
        elif 'readme' in file.lower() or 'changelog' in file.lower():
            suggestions.append({
                "file": file,
                "type": "structure_changed",
                "priority": "low",
                "suggestion": f"文档文件 `{file}` 有更新",
                "doc_section": "项目说明"
            })

        # 模块/组件变更
        elif ext in ['.py', '.js', '.ts', '.java', '.go', '.rs', '.c', '.cpp']:
            module_name = os.path.dirname(file).split('/')[-1] or 'root'
            suggestions.append({
                "file": file,
                "type": "module_modified",
                "priority": "medium",
                "suggestion": f"模块 `{module_name}` 中的 `{os.path.basename(file)}` 有变更",
                "doc_section": f"模块文档 > {module_name}"
            })

    return suggestions


def generate_update_report(project_dir: str, doc_token: str = None,
                           suggestions: List[Dict] = None) -> str:
    """生成飞书友好的更新建议报告"""

    # 获取变更信息
    changed_files = get_git_diff_files(project_dir)
    commits = get_git_log(project_dir)

    if not suggestions:
        suggestions = analyze_changes(project_dir, changed_files)

    # 按优先级分组
    high_priority = [s for s in suggestions if s.get("priority") == "high"]
    medium_priority = [s for s in suggestions if s.get("priority") == "medium"]
    low_priority = [s for s in suggestions if s.get("priority") == "low"]

    # 生成报告
    report = f"""# 📋 飞书文档更新建议报告

> 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}
> 项目路径: `{project_dir}`
> 变更文件数: {len(changed_files)}

---

## 📊 变更概览

### 最近提交

| 提交 | 说明 | 作者 | 日期 |
|------|------|------|------|
"""
    for commit in commits[:5]:
        report += f"| `{commit['hash']}` | {commit['message'][:30]} | {commit['author']} | {commit['date']} |\n"

    report += f"""
### 变更文件

```
{chr(10).join(changed_files[:20])}
{"..." if len(changed_files) > 20 else ""}
```

---

## 🔴 高优先级更新 ({len(high_priority)} 项)

"""
    if high_priority:
        for s in high_priority:
            report += f"""### {CHANGE_TYPES.get(s['type'], s['type'])}

**文件**: `{s['file']}`
**文档章节**: {s['doc_section']}
**建议**: {s['suggestion']}

---

"""
    else:
        report += "_无高优先级更新_\n\n---\n\n"

    report += f"""## 🟡 中优先级更新 ({len(medium_priority)} 项)

"""
    if medium_priority:
        for s in medium_priority:
            report += f"- **{s['doc_section']}**: {s['suggestion']}\n"
    else:
        report += "_无中优先级更新_\n"

    report += f"""
---

## 🟢 低优先级更新 ({len(low_priority)} 项)

"""
    if low_priority:
        for s in low_priority:
            report += f"- {s['suggestion']}\n"
    else:
        report += "_无低优先级更新_\n"

    # 添加操作指南
    report += f"""
---

## 🚀 执行更新

### 方式一：追加到文档末尾

```bash
feishu_doc_update append --doc_token "{doc_token or '<文档token>'}"
```

### 方式二：创建新文档

```bash
feishu_doc_create --folder_token "<文件夹token>"
```

### 方式三：替换指定块

```bash
feishu_doc_update replace_block --doc_token "<文档token>" --block_id "<块ID>"
```

---

## ⚠️ 注意事项

1. 此报告为**建议**，不会自动修改飞书文档
2. 请确认后再执行更新操作
3. 建议先备份重要文档

---

*由 project-assistant 自动生成*
"""

    return report


def generate_doc_content_suggestion(file_path: str, change_type: str) -> str:
    """为单个文件生成文档内容建议"""

    ext = os.path.splitext(file_path)[1].lower()
    file_name = os.path.basename(file_path)

    suggestions = {
        "api_added": f"""## 新增接口: {file_name}

### 接口说明
<!-- 请填写接口用途 -->

### 请求方式
- Method: `POST/GET`
- Path: `/api/xxx`

### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| | | | |

### 返回示例
```json
{{
  "code": 0,
  "data": {{}}
}}
```
""",
        "api_modified": f"""## 接口变更: {file_name}

### 变更内容
<!-- 请描述变更 -->

### 兼容性
- [ ] 向下兼容
- [ ] 需要客户端更新

### 迁移指南
<!-- 如果有破坏性变更，请填写迁移步骤 -->
""",
        "module_added": f"""## 新增模块: {file_name}

### 功能说明
<!-- 请填写模块功能 -->

### 使用方式
```python
# 示例代码
```

### 依赖
- 依赖1
- 依赖2
"""
    }

    return suggestions.get(change_type, f"<!-- {file_path} 有变更，请更新相关文档 -->")


def check_doc_sync_status(project_dir: str, doc_token: str = None) -> Dict[str, Any]:
    """检查文档同步状态"""

    changed_files = get_git_diff_files(project_dir)
    suggestions = analyze_changes(project_dir, changed_files)

    # 统计
    high_count = len([s for s in suggestions if s.get("priority") == "high"])
    medium_count = len([s for s in suggestions if s.get("priority") == "medium"])
    low_count = len([s for s in suggestions if s.get("priority") == "low"])

    # 判断状态
    if high_count > 0:
        status = "need_update"
        status_text = "🔴 需要更新"
    elif medium_count > 0:
        status = "suggest_update"
        status_text = "🟡 建议更新"
    elif low_count > 0:
        status = "minor_update"
        status_text = "🟢 可选更新"
    else:
        status = "synced"
        status_text = "✅ 已同步"

    return {
        "status": status,
        "status_text": status_text,
        "changed_files": len(changed_files),
        "high_priority": high_count,
        "medium_priority": medium_count,
        "low_priority": low_count,
        "suggestions": suggestions
    }


def save_sync_record(project_dir: str, record: Dict) -> None:
    """保存同步记录"""
    record_path = os.path.join(project_dir, ".claude", "feishu_sync.json")
    os.makedirs(os.path.dirname(record_path), exist_ok=True)

    record["updated_at"] = datetime.now().isoformat()

    with open(record_path, 'w', encoding='utf-8') as f:
        json.dump(record, f, ensure_ascii=False, indent=2)


def print_help():
    """打印帮助"""
    help_text = """
飞书文档集成管理器

与飞书 Skill 协作，生成文档更新建议（不直接修改文档）

用法: feishu_doc_manager.py <projectDir> <command> [args]

命令:
  report [doc_token]
      生成飞书文档更新建议报告

  status [doc_token]
      检查文档同步状态

  suggest <file_path> <change_type>
      为单个文件生成文档内容建议

  config
      显示飞书配置项说明

示例:
  # 生成更新报告
  feishu_doc_manager.py ./project report

  # 检查同步状态
  feishu_doc_manager.py ./project status

  # 生成单个文件的文档建议
  feishu_doc_manager.py ./project suggest "src/api/user.py" "api_added"

配置项（通过 /set-config 设置）:
  feishu.doc_token      文档 token
  feishu.folder_token   文件夹 token
  feishu.wiki_token     知识库 token
  feishu.doc_url        文档 URL
"""
    print(help_text)


def main():
    if len(sys.argv) < 3:
        print_help()
        sys.exit(1)

    project_dir = sys.argv[1]
    command = sys.argv[2]

    if command == "report":
        doc_token = sys.argv[3] if len(sys.argv) > 3 else None
        report = generate_update_report(project_dir, doc_token)
        print(report)

    elif command == "status":
        doc_token = sys.argv[3] if len(sys.argv) > 3 else None
        result = check_doc_sync_status(project_dir, doc_token)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "suggest":
        if len(sys.argv) < 5:
            print("用法: feishu_doc_manager.py <projectDir> suggest <file_path> <change_type>")
            sys.exit(1)
        suggestion = generate_doc_content_suggestion(sys.argv[3], sys.argv[4])
        print(suggestion)

    elif command == "config":
        print("飞书配置项：")
        for key in FEISHU_CONFIG_KEYS:
            print(f"  /set-config {key} <value>")

    else:
        print(f"未知命令: {command}")
        print_help()


if __name__ == "__main__":
    main()