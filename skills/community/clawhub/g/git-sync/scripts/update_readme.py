#!/usr/bin/env python3
"""
update_readme.py - 全量重新生成 README.md（从仓库实际文件）

不再手动维护 README.md，而是从 WORK_REPO/skills/ 实际目录扫描，
全量生成技能列表表格和目录结构，确保 README = 仓库实际内容。

用法: python update_readme.py <repo_name> <readme_path>
示例: python update_readme.py workbuddy-skills /path/to/README.md
"""

import json
import os
import re
import sys
from datetime import date
from pathlib import Path

# ── 路径集中管理 ─────────────────────────────────────────
from _paths import (
    _data_dir_abs, DEFAULT_DATA_DIR_RAW, SKILL_DIR, SKILLS_ROOT as SKILLS_DIR,
    CONFIG_FILE, MANIFEST_FILE as MANIFEST_PATH,
)






def load_config():
    """读取 skills/.standardization/git-sync/data/config.json"""
    config_path = str(CONFIG_FILE)
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def get_clone_urls(config):
    """从 config.json 生成 gitee/github clone URL"""
    urls = {'gitee': '', 'github': ''}
    gitee_cfg = config.get('gitee', {})
    github_cfg = config.get('github', {})
    if gitee_cfg.get('user') and gitee_cfg.get('repo'):
        urls['gitee'] = f"https://gitee.com/{gitee_cfg['user']}/{gitee_cfg['repo']}.git"
    if github_cfg.get('user') and github_cfg.get('repo'):
        urls['github'] = f"https://github.com/{github_cfg['user']}/{github_cfg['repo']}.git"
    return urls

def get_readme_config(config):
    """从 config.json 提取 README 文案配置"""
    return config.get('readme', {})

def extract_desc(skill_dir):
    """从 _meta.json 或 SKILL.md 提取描述"""
    # 优先 _meta.json
    meta_path = os.path.join(skill_dir, "_meta.json")
    if os.path.exists(meta_path):
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                d = json.load(f)
                desc = d.get("description", "")
                if desc:
                    return desc.strip()
        except Exception:
            pass

    # 降级：从 SKILL.md YAML frontmatter 提取
    skill_path = os.path.join(skill_dir, "SKILL.md")
    if os.path.exists(skill_path):
        try:
            with open(skill_path, "r", encoding="utf-8") as f:
                content = f.read()
            m = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
            if m:
                fm = m.group(1)
                for line in fm.split("\n"):
                    if line.strip().startswith("description:"):
                        return line.split(":", 1)[1].strip()
        except Exception:
            pass

    return "技能描述"

def generate_readme(repo_path, readme_path):
    """全量生成 README.md"""
    skills_dir = os.path.join(repo_path, "skills")
    today = date.today().isoformat()

    if not os.path.isdir(skills_dir):
        print(f"❌ skills/ 目录不存在: {skills_dir}")
        sys.exit(1)

    # 扫描实际技能目录（排除非技能目录）
    SKIP_DIRS = {".dist", ".standardization", "skills"}
    actual_skills = []
    for entry in sorted(os.listdir(skills_dir)):
        full = os.path.join(skills_dir, entry)
        if os.path.isdir(full) and entry not in SKIP_DIRS:
            desc = extract_desc(full)
            actual_skills.append((entry, desc))

    _safe_print(f"扫描到 {len(actual_skills)} 个技能目录:")
    for name, desc in actual_skills:
        _safe_print(f"  - {name}: {desc[:60]}")

    # 生成技能列表表格
    table_lines = []
    for name, desc in actual_skills:
        table_lines.append(f"| `{name}` | {desc} |")
    table = "\n".join(table_lines)

    # 生成目录树（从仓库根目录实际扫描）
    SKIP_ROOT = {".git", "__pycache__", ".gitignore", "README.md.bak"}
    root_entries = []
    for entry in sorted(os.listdir(repo_path)):
        if entry in SKIP_ROOT or entry.startswith("."):
            continue
        full = os.path.join(repo_path, entry)
        suffix = "/" if os.path.isdir(full) else ""
        root_entries.append((entry, suffix))
    tree_lines = []
    for entry, suffix in root_entries[:-1]:
        tree_lines.append(f"├── {entry}{suffix}")
    if root_entries:
        tree_lines.append(f"└── {root_entries[-1][0]}{root_entries[-1][1]}")
    tree = "\n".join(tree_lines)

    # 读取配置中的 clone URL 和 README 文案
    config = load_config()
    urls = get_clone_urls(config)
    gitee_url = urls['gitee'] or "https://gitee.com/USER/REPO.git"
    github_url = urls['github'] or "https://github.com/USER/REPO.git"
    readme_cfg = get_readme_config(config)
    readme_title = readme_cfg.get('title', 'WorkBuddy Skills Repository')
    readme_desc = readme_cfg.get('description', '本仓库托管技能合集，码云（Gitee）和 GitHub 双平台同步。')
    readme_repo_name = readme_cfg.get('repo_name', 'workbuddy-skills')

    # 构建新的 README.md
    new_readme = f"""# {readme_title}

> **用户技能仓库** — 由 git-sync 自动同步维护。
> 最后更新：{today}

{readme_desc}

---

## 技能列表

以下为仓库中实际存在的技能（由 `git-sync` 全量生成，请勿手动修改此表格）：

| 技能名 | 描述 |
|--------|------|
{table}

---

## 目录结构

```
{readme_repo_name}/
{tree}
```

---

## 如何使用

### 方式一：从码云（Gitee）安装
```bash
cd ~/.workbuddy/skills
git clone {gitee_url} temp-skills
cp -r temp-skills/skills/* .
rm -rf temp-skills
```

### 方式二：从 GitHub 安装
```bash
cd ~/.workbuddy/skills/
git clone {github_url} temp-skills
cp -r temp-skills/skills/* .
rm -rf temp-skills
```

### 方式三：ZIP 包安装
从 Releases 下载对应技能的 ZIP 包，解压到 `~/.workbuddy/skills/` 目录。

---

## 维护说明

- 本仓库由 **git-sync** 技能自动维护
- README.md 由 `update_readme.py` **从仓库实际文件全量生成**，不手动编辑
- 维护清单：`skills/.standardization/git-sync/data/manifest.json`（记录计划管理的技能全集）
- 三单一致原则：**清单 ⊇ 仓库 = README.md**

---

## 许可证

MIT License
"""

    # 写回文件
    backup_path = readme_path + ".bak"
    if os.path.exists(readme_path):
        import shutil

        shutil.copy2(readme_path, backup_path)
        _safe_print("  已备份原 README.md -> README.md.bak")

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_readme)
    _safe_print(f"  README.md 已全量重新生成: {readme_path}")

def _safe_print(msg):
    """兼容 GBK 终端的安全打印"""
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("ascii", errors="replace").decode("ascii"))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python update_readme.py <repo_name> <readme_path>")
        print("示例: python update_readme.py workbuddy-skills /path/to/README.md")
        sys.exit(1)

    repo_name = sys.argv[1]
    readme_path = sys.argv[2]

    # 从 skills/.standardization/git-sync/data/manifest.json 获取仓库路径
    manifest_path = str(MANIFEST_PATH)

    if not os.path.exists(manifest_path):
        print(f"❌ manifest.json 不存在: {manifest_path}")
        sys.exit(1)

    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    repos = data.get("repos", {})
    if repo_name not in repos:
        print(f"❌ 仓库 '{repo_name}' 不存在于 manifest.json")
        sys.exit(1)

    repo_path = os.path.expanduser(repos[repo_name].get("path", ""))
    if not repo_path or not os.path.isdir(repo_path):
        print(f"❌ 仓库路径不存在: {repo_path}")
        sys.exit(1)

    generate_readme(repo_path, readme_path)
