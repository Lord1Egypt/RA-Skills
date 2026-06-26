#!/usr/bin/env python3
"""
AI Doc Generator - 通用型开发者效率工具
一键生成专业 README、版本日志，支持 Git Commit 解析，语义化版本号计算
"""

import sys
import re
from datetime import datetime
from typing import Dict, List, Optional

COMMIT_TYPE_MAP = {
    "feat": {"category": "新增功能", "keywords": ["新增", "新功能", "add", "feature"]},
    "fix": {"category": "问题修复", "keywords": ["修复", "bug", "fix", "错误", "问题"]},
    "docs": {"category": "文档更新", "keywords": ["文档", "docs", "readme"]},
    "style": {"category": "优化改进", "keywords": ["格式", "style", "format"]},
    "refactor": {"category": "优化改进", "keywords": ["重构", "refactor", "优化"]},
    "perf": {"category": "优化改进", "keywords": ["性能", "perf", "performance", "优化"]},
    "test": {"category": "其他", "keywords": ["测试", "test"]},
    "chore": {"category": "其他", "keywords": ["构建", "chore", "杂项", "更新依赖"]},
}


def classify_commit(line: str) -> str:
    line_lower = line.lower()
    for commit_type in ["feat", "fix", "docs", "style", "refactor", "perf", "test", "chore"]:
        if line_lower.startswith(commit_type + ":") or line_lower.startswith(f"({commit_type})"):
            return commit_type
    for commit_type, info in COMMIT_TYPE_MAP.items():
        for keyword in info["keywords"]:
            if keyword in line_lower:
                return commit_type
    return "chore"


def parse_commits(commits_text: str) -> Dict[str, List[str]]:
    result = {k: [] for k in COMMIT_TYPE_MAP.keys()}
    for line in commits_text.strip().split("\n"):
        line = line.strip()
        if line:
            commit_type = classify_commit(line)
            result[commit_type].append(line)
    return result


def calculate_version(old_version: str, commits: Dict[str, List[str]]) -> str:
    if not old_version:
        return "v1.0.0"
    old_version = old_version.strip().lstrip("v")
    try:
        parts = old_version.split(".")
        major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
    except:
        return "v1.0.0"
    all_commits = " ".join([item for items in commits.values() for item in items]).lower()
    has_breaking = "breaking" in all_commits or "不兼容" in all_commits or "破坏性" in all_commits
    has_feat = len(commits.get("feat", [])) > 0
    has_fix_or_perf = len(commits.get("fix", [])) > 0 or len(commits.get("perf", [])) > 0
    if has_breaking:
        major += 1
        minor = 0
        patch = 0
    elif has_feat:
        minor += 1
        patch = 0
    elif has_fix_or_perf:
        patch += 1
    return f"v{major}.{minor}.{patch}"


def generate_changelog(version: str, date: str, commits: Dict[str, List[str]]) -> str:
    lines = [f"{version} ({date})", ""]
    if commits.get("feat"):
        lines.append("### 新增功能")
        for item in commits["feat"]:
            lines.append(f"- {item}")
        lines.append("")
    if commits.get("fix"):
        lines.append("### 问题修复")
        for item in commits["fix"]:
            lines.append(f"- {item}")
        lines.append("")
    improvements = commits.get("refactor", []) + commits.get("perf", []) + commits.get("style", [])
    if improvements:
        lines.append("### 优化改进")
        for item in improvements:
            lines.append(f"- {item}")
        lines.append("")
    others = commits.get("docs", []) + commits.get("test", []) + commits.get("chore", [])
    if others:
        lines.append("### 其他")
        for item in others:
            lines.append(f"- {item}")
        lines.append("")
    return "\n".join(lines).strip()


def parse_input_content(content: str) -> List[str]:
    lines = []
    for line in content.strip().split("\n"):
        line = line.strip()
        if line and not line.startswith("#"):
            lines.append(line)
    return lines


def generate_changelog_from_input(content: str, old_version: str = "", commits_text: str = "") -> Dict:
    today = datetime.now().strftime("%Y-%m-%d")
    commits_dict = {}
    if commits_text:
        commits_dict = parse_commits(commits_text)
    else:
        raw_items = parse_input_content(content)
        for item in raw_items:
            commit_type = classify_commit(item)
            commits_dict.setdefault(commit_type, []).append(item)
    if not commits_dict or all(not v for v in commits_dict.values()):
        commits_dict = {"chore": [content[:50] if content else "更新"]}
    new_version = calculate_version(old_version, commits_dict)
    changelog_content = generate_changelog(new_version, today, commits_dict)
    return {
        "version": new_version,
        "date": today,
        "content": changelog_content
    }


def generate_readme(project_name: str, description: str, features: List[str], 
                   tech_stack: List[str] = None, repo_url: str = "") -> str:
    lines = [
        f"# {project_name}",
        "",
        description,
        "",
        "## 特性",
        ""
    ]
    for feature in features:
        lines.append(f"- {feature}")
    lines.append("")
    if tech_stack:
        lines.append("## 技术栈")
        lines.append("")
        for tech in tech_stack:
            lines.append(f"- {tech}")
        lines.append("")
    lines.extend([
        "## 开始使用",
        "",
        "```bash",
        f"# 克隆项目",
        f"git clone {repo_url or 'https://github.com/your-repo/' + project_name + '.git'}",
        "```",
        "",
        "## 贡献",
        "",
        "欢迎提交 Issue 和 Pull Request！",
        "",
        "## 许可证",
        "",
        "MIT License"
    ])
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("=" * 60)
        print("AI Doc Generator - 开发者效率工具")
        print("=" * 60)
        print("")
        print("使用方法:")
        print("  python app.py changelog <内容> [旧版本号]")
        print("  python app.py readme <项目名> <描述>")
        print("")
        print("示例:")
        print('  python app.py changelog "feat: 新增登录功能\\nfix: 修复bug" v1.0.0')
        print('  python app.py readme "我的项目" "这是一个很棒的项目"')
        print("")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "changelog":
        if len(sys.argv) < 3:
            print("错误: 请提供更新内容")
            sys.exit(1)
        content = sys.argv[2]
        old_version = sys.argv[3] if len(sys.argv) > 3 else ""
        commits_text = content
        result = generate_changelog_from_input("", old_version, commits_text)
        print("\n" + "=" * 60)
        print("生成的 Changelog:")
        print("=" * 60)
        print(result["content"])
        print("")
    
    elif command == "readme":
        if len(sys.argv) < 4:
            print("错误: 请提供项目名和描述")
            sys.exit(1)
        project_name = sys.argv[2]
        description = sys.argv[3]
        features = sys.argv[4].split("|") if len(sys.argv) > 4 else []
        result = generate_readme(project_name, description, features)
        print("\n" + "=" * 60)
        print("生成的 README:")
        print("=" * 60)
        print(result)
        print("")
    
    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
