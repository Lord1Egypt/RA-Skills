#!/usr/bin/env python3
"""
manifest.py - 通用维护清单管理 CLI
独立脚本，不污染 git-sync 主逻辑。

用法:
  python manifest.py list [repo]
  python manifest.py add <repo> <name> [--type skill] [--uploaded]
  python manifest.py remove <repo> <name>
  python manifest.py check <repo> <name>
  python manifest.py diff <repo>
  python manifest.py sync-readme <repo>

三单一致模型：
  维护清单 (manifest.json)  ≥  仓库实际文件  =  README.md
  - 清单是计划管理的全集，可以包含 uploaded:false 的条目
  - 仓库是清单中 uploaded:true 的子集
  - README.md 动态生成，永远 = 仓库实际内容
"""

import json
import os
import sys
import argparse
import tempfile
import re
from datetime import date
from pathlib import Path

# ── 路径集中管理 ─────────────────────────────────────────
from _paths import (
    _data_dir_abs, DEFAULT_DATA_DIR_RAW, SKILL_DIR,
    SKILLS_ROOT as SKILLS_DIR, MANIFEST_FILE as MANIFEST_PATH, CONFIG_FILE,
)

# ── 编码安全 ─────────────────────────────────────────────
# Windows Git Bash (GBK) 下 print(emoji) 直接崩，
# 模块级替换 print 为安全版本，避免挨个改 25+ 处调用。
import builtins
_original_print = builtins.print
def _safe_print(*args, **kwargs):
    try:
        _original_print(*args, **kwargs)
    except UnicodeEncodeError:
        safe_args = [str(a).encode("ascii", errors="replace").decode("ascii") for a in args]
        _original_print(*safe_args, **kwargs)
builtins.print = _safe_print

# ── 路径解析 ───────────────────────────────────────────
def _find_skills_dir():
    """从 scripts/ 往上 2 级确定 skills 目录: skills/<name>/scripts/ → skills/"""
    return str(Path(__file__).resolve().parent.parent.parent)


def load_manifest():
    if not os.path.exists(MANIFEST_PATH):
        return {"repos": {}}
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_manifest(data):
    # 原子写入：先写临时文件再 rename
    dir_name = os.path.dirname(MANIFEST_PATH)
    fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        os.replace(tmp_path, MANIFEST_PATH)
    except Exception:
        os.unlink(tmp_path)
        raise

def expand_path(p):
    return os.path.expanduser(p)

def get_repo_path(repo_name, data):
    """从 manifest.json 获取仓库路径，支持 ~ 展开"""
    repos = data.get("repos", {})
    if repo_name not in repos:
        return None
    p = repos[repo_name].get("path", "")
    return expand_path(p) if p else None

def get_uploaded_items(data, repo_name):
    """获取清单中 uploaded=True 的条目名称集合"""
    repos = data.get("repos", {})
    if repo_name not in repos:
        return set()
    items = repos[repo_name].get("items", {})
    return {name for name, v in items.items() if isinstance(v, dict) and v.get("uploaded", False)}

# ── 子命令实现 ─────────────────────────────────────────

def cmd_list(args):
    data = load_manifest()
    repos = data.get("repos", {})

    if args.repo:
        if args.repo not in repos:
            print(f"❌ 仓库 '{args.repo}' 不存在")
            sys.exit(1)
        repos = {args.repo: repos[args.repo]}

    for repo_name, repo_info in repos.items():
        items = repo_info.get("items", {})
        print(f"{repo_name} ({len(items)} items):")
        for name, v in items.items():
            if isinstance(v, dict):
                t = v.get("type", "?")
                d = v.get("added_at", "?")
                gitee_ok = v.get("gitee_ok", v.get("uploaded", False))
                github_ok = v.get("github_ok", v.get("uploaded", False))
                gitee_ver = v.get("gitee_version", v.get("version", "?"))
                github_ver = v.get("github_version", v.get("version", "?"))

                # 状态图标
                if gitee_ok and github_ok:
                    flag = "✅✅"
                elif gitee_ok:
                    flag = "✅⚠️ "
                elif github_ok:
                    flag = "⚠️ ✅"
                else:
                    flag = "⏳"

                note = v.get("note", "")
                print(f"  [{flag}] {name:<30} {t:<8} {d}")
                print(f"         └─ 码云:{gitee_ver} {'✅' if gitee_ok else '❌'}  GitHub:{github_ver} {'✅' if github_ok else '❌'}")
                if note:
                    print(f"         └─ {note}")
            else:
                print(f"  [?] {name:<30} (旧格式: {v})")
        print()

def cmd_add(args):
    data = load_manifest()
    repos = data.setdefault("repos", {})

    if args.repo not in repos:
        repos[args.repo] = {"path": "", "description": "", "items": {}}
        print(f"  ℹ️  已创建仓库: {args.repo}")

    items = repos[args.repo].setdefault("items", {})

    if args.name in items:
        print(f"❌ '{args.name}' 已存在于清单 '{args.repo}' 中")
        sys.exit(1)

    gitee_ok = args.gitee_ok or args.uploaded
    github_ok = args.github_ok or args.uploaded
    items[args.name] = {
        "type": args.type,
        "added_at": date.today().isoformat(),
        "uploaded": gitee_ok and github_ok,
        "gitee_ok": gitee_ok,
        "github_ok": github_ok,
        "version": "",
        "gitee_version": "",
        "github_version": "",
        "note": args.note or ""
    }
    save_manifest(data)
    ge = "✅" if gitee_ok else "❌"
    gh = "✅" if github_ok else "❌"
    print(f"  ✅ 已添加: [码云{ge}|GitHub{gh}] {args.name} → {args.repo}")

def cmd_remove(args):
    data = load_manifest()
    repos = data.get("repos", {})

    if args.repo not in repos:
        print(f"❌ 仓库 '{args.repo}' 不存在")
        sys.exit(1)

    items = repos[args.repo].get("items", {})
    if args.name not in items:
        print(f"❌ '{args.name}' 不在清单 '{args.repo}' 中")
        sys.exit(1)

    del items[args.name]
    save_manifest(data)
    print(f"  ✅ 已移除: {args.name} ← {args.repo}")

def cmd_check(args):
    """检查技能是否在清单内，输出双平台状态。
       输出供 git-sync.sh 解析：
       FOUND:gitee_ok,github_ok
       退出码：0=双平台ok, 1=部分/全失败, 2=NOT_FOUND
    """
    data = load_manifest()
    repos = data.get("repos", {})

    if args.repo not in repos:
        print("NOT_FOUND")
        sys.exit(2)

    items = repos[args.repo].get("items", {})
    if args.name not in items:
        print("NOT_FOUND")
        sys.exit(2)

    item = items[args.name]
    if not isinstance(item, dict):
        print("FOUND:false,false")
        sys.exit(1)

    gitee_ok = item.get("gitee_ok", item.get("uploaded", False))
    github_ok = item.get("github_ok", item.get("uploaded", False))
    print(f"FOUND:{str(gitee_ok).lower()},{str(github_ok).lower()}")
    if gitee_ok and github_ok:
        sys.exit(0)   # 双平台都成功
    else:
        sys.exit(1)   # 部分或全失败

def cmd_version(args):
    """查询或更新清单中某个条目的版本号。
       用法:
          python manifest.py version <repo> <name> [--platform gitee|github]              # 查询
          python manifest.py version <repo> <name> <version> [--platform gitee|github]   # 更新
    """
    data = load_manifest()
    repos = data.get("repos", {})

    if args.repo not in repos:
        print(f"❌ 仓库 '{args.repo}' 不存在")
        sys.exit(1)

    items = repos[args.repo].get("items", {})
    if args.name not in items:
        print(f"❌ '{args.name}' 不在清单 '{args.repo}' 中")
        sys.exit(1)

    item = items[args.name]
    platform = getattr(args, "platform", None)

    if not isinstance(item, dict):
        # 兼容旧格式，先转换
        items[args.name] = {"type": "skill", "added_at": "", "uploaded": False,
                            "gitee_ok": False, "github_ok": False,
                            "version": "1.0.0", "gitee_version": "1.0.0", "github_version": "1.0.0",
                            "note": str(item)}
        item = items[args.name]

    if args.version:
        old = item.get("version", "")
        item["version"] = args.version
        # 更新平台版本号
        if platform in ("gitee", "both", None):
            item["gitee_version"] = args.version
            item["gitee_ok"] = True
        if platform in ("github", "both", None):
            item["github_version"] = args.version
            item["github_ok"] = True
        # 重新计算 upload ed
        item["uploaded"] = item.get("gitee_ok", False) and item.get("github_ok", False)
        save_manifest(data)
        plat_str = f" [{platform}]" if platform else ""
        print(f"  ✅ 版本已更新{plat_str}: {args.name}  {old} → {args.version}")
    else:
        ver = item.get("version", "(未设置)")
        gitee_ver = item.get("gitee_version", ver)
        github_ver = item.get("github_version", ver)
        ge = "✅" if item.get("gitee_ok") else "❌"
        gh = "✅" if item.get("github_ok") else "❌"
        print(f"{args.name}  版本: {ver}")
        print(f"  码云: {gitee_ver} {ge}  GitHub: {github_ver} {gh}")

def cmd_diff(args):
    data = load_manifest()
    repos = data.get("repos", {})

    if args.repo not in repos:
        print(f"❌ 仓库 '{args.repo}' 不存在")
        sys.exit(1)

    repo_info = repos[args.repo]
    repo_path = get_repo_path(args.repo, data)
    uploaded_set = get_uploaded_items(data, args.repo)

    # 扫描仓库实际目录
    actual_set = set()
    if repo_path and os.path.isdir(repo_path):
        skills_dir = os.path.join(repo_path, "skills")
        if os.path.isdir(skills_dir):
            for entry in os.listdir(skills_dir):
                full = os.path.join(skills_dir, entry)
                if os.path.isdir(full):
                    actual_set.add(entry)

    print(f"清单(uploaded=true): {len(uploaded_set)} 项")
    print(f"仓库实际文件:     {len(actual_set)} 项")
    print()

    # 清单有但仓库没有 → 需要补传
    missing = uploaded_set - actual_set
    if missing:
        print("【缺失】在清单中(uploaded=true)但仓库不存在，需要补传:")
        for name in sorted(missing):
            print(f"  [缺失] {name}")
    else:
        print("【一致】所有 uploaded=true 的条目均存在于仓库中 ✅")

    # 仓库有但清单没有（或 uploaded=false）→ 清单需要更新
    extra = actual_set - uploaded_set
    if extra:
        print()
        print("【多余】仓库有但清单未登记 uploaded=true，建议添加到清单:")
        for name in sorted(extra):
            print(f"  [多余] {name}")

    print()

def cmd_sync_readme(args):
    """根据仓库实际文件全量重新生成 README.md
    README = 仓库实际内容，不依赖清单
    """
    data = load_manifest()
    repo_path = get_repo_path(args.repo, data)

    if not repo_path or not os.path.isdir(repo_path):
        print(f"❌ 仓库路径不存在: {repo_path}")
        sys.exit(1)

    readme_path = os.path.join(repo_path, "README.md")
    skills_dir = os.path.join(repo_path, "skills")

    if not os.path.isdir(skills_dir):
        print(f"❌ skills/ 目录不存在: {skills_dir}")
        sys.exit(1)

    # 扫描实际技能目录
    actual_skills = []
    for entry in sorted(os.listdir(skills_dir)):
        full = os.path.join(skills_dir, entry)
        if not os.path.isdir(full):
            continue
        # 提取描述
        desc = _extract_desc(full)
        actual_skills.append((entry, desc))

    print(f"扫描到 {len(actual_skills)} 个技能目录:")
    for name, desc in actual_skills:
        print(f"  - {name}: {desc[:60]}")

    # 全量生成 README.md
    new_readme = _generate_readme(actual_skills)
    backup_path = readme_path + ".bak"
    if os.path.exists(readme_path):
        import shutil

        shutil.copy2(readme_path, backup_path)
        print(f"  ℹ️  已备份原 README.md → README.md.bak")

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_readme)
    print(f"  ✅ README.md 已全量重新生成: {readme_path}")

def cmd_set_uploaded(args):
    """标记指定平台为已上传（不更新版本号）
       用法: python manifest.py set-uploaded <repo> <name> [--platform gitee|github|both]
    """
    data = load_manifest()
    repos = data.get("repos", {})
    if args.repo not in repos:
        print(f"ERROR: 仓库 '{args.repo}' 不存在", file=sys.stderr)
        sys.exit(1)
    items = repos[args.repo].get("items", {})
    if args.name not in items:
        print(f"ERROR: '{args.name}' 不在清单中", file=sys.stderr)
        sys.exit(1)
    item = items[args.name]
    if not isinstance(item, dict):
        print(f"ERROR: '{args.name}' 格式错误（旧格式）", file=sys.stderr)
        sys.exit(1)
    if args.platform in ("gitee", "both"):
        item["gitee_ok"] = True
    if args.platform in ("github", "both"):
        item["github_ok"] = True
    item["uploaded"] = item.get("gitee_ok", False) and item.get("github_ok", False)
    save_manifest(data)
    print(f"  OK: {args.name} gitee={item.get('gitee_ok')} github={item.get('github_ok')} uploaded={item['uploaded']}")

def _extract_desc(skill_dir):
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

def _load_config():
    """读取 skills/.standardization/git-sync/data/config.json，返回配置字典"""
    config_path = str(CONFIG_FILE)
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def _generate_readme(skills):
    """全量生成 README.md 内容"""
    today = date.today().isoformat()

    # 从 config.json 读取全部配置
    config = _load_config()
    gitee_user = config.get("gitee", {}).get("user", "your-gitee-username")
    github_user = config.get("github", {}).get("user", "your-github-username")
    repo_name = config.get("gitee", {}).get("repo", "workbuddy-skills")
    readme_cfg = config.get("readme", {})
    readme_title = readme_cfg.get("title", "WorkBuddy Skills Repository")
    readme_desc = readme_cfg.get("description", "本仓库存放 WorkBuddy 用户技能，支持码云（Gitee）和 GitHub 双平台同步。")
    readme_repo_name = readme_cfg.get("repo_name", "workbuddy-skills")

    # 技能列表表格
    table_lines = []
    for name, desc in skills:
        table_lines.append(f"| `{name}` | {desc} |")

    table = "\n".join(table_lines)

    # 目录树
    tree_lines = ["├── " + name + "/" for name, _ in skills[:-1]] if len(skills) > 1 else []
    if skills:
        if len(skills) == 1:
            tree_lines = ["└── " + skills[0][0] + "/"]
        else:
            tree_lines.append("└── " + skills[-1][0] + "/")
    tree = "\n".join(tree_lines)

    readme = f"""# {readme_title}

> **用户技能仓库** — 由 git-sync 自动同步维护。
> 最后更新：{today}

{readme_desc}

---

## 技能列表

以下为仓库中实际存在的技能（由 `manifest.py sync-readme` 全量生成，请勿手动修改此表格）：

| 技能名 | 描述 |
|--------|------|
{table}

---

## 目录结构

```
{readme_repo_name}/
├── README.md
├── LICENSE
└── skills/
{tree}
```

---

## 如何使用

### 方式一：从工蜂（Gitee）安装
```bash
cd ~/.workbuddy/skills
git clone https://gitee.com/{gitee_user}/{repo_name}.git temp-skills
cp -r temp-skills/skills/* .
rm -rf temp-skills
```

### 方式二：从 GitHub 安装
```bash
cd ~/.workbuddy/skills/
git clone https://github.com/{github_user}/{repo_name}.git temp-skills
cp -r temp-skills/skills/* .
rm -rf temp-skills
```

### 方式三：ZIP 包安装
从 Releases 下载对应技能的 ZIP 包，解压到 `~/.workbuddy/skills/` 目录。

---

## 维护说明

- 本仓库由 **git-sync** 技能自动维护
- README.md 由 `manifest.py sync-readme` **从仓库实际文件全量生成**，不手动编辑
- 维护清单：`skills/.standardization/git-sync/data/manifest.json`（记录计划管理的技能全集）
- 三单一致原则：**清单 ⊆ 仓库 ⊆ README.md**

---

## 许可证

MIT License
"""

    return readme

# ── CLI 参数解析 ─────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="manifest.py - 通用维护清单管理 CLI"
    )
    sub = parser.add_subparsers(dest="command", help="子命令")

    # list
    p_list = sub.add_parser("list", help="列出清单")
    p_list.add_argument("repo", nargs="?", help="仓库名（不填则列出所有）")

    # add
    p_add = sub.add_parser("add", help="加入清单")
    p_add.add_argument("repo", help="仓库名")
    p_add.add_argument("name", help="条目名称")
    p_add.add_argument("--type", default="skill", help="条目类型（默认: skill）")
    p_add.add_argument("--uploaded", action="store_true", help="标记为双平台已上传")
    p_add.add_argument("--gitee-ok", action="store_true", help="标记为码云已推送")
    p_add.add_argument("--github-ok", action="store_true", help="标记为 GitHub 已推送")
    p_add.add_argument("--note", help="备注")

    # remove
    p_remove = sub.add_parser("remove", help="从清单移除")
    p_remove.add_argument("repo", help="仓库名")
    p_remove.add_argument("name", help="条目名称")

    # check
    p_check = sub.add_parser("check", help="检查是否在清单内")
    p_check.add_argument("repo", help="仓库名")
    p_check.add_argument("name", help="条目名称")

    # version
    p_version = sub.add_parser("version", help="查询/更新条目版本号（支持分平台）")
    p_version.add_argument("repo", help="仓库名")
    p_version.add_argument("name", help="条目名称")
    p_version.add_argument("version", nargs="?", help="新版本号（不填则查询）")
    p_version.add_argument("--platform", choices=["gitee", "github", "both"], default="both",
                           help="指定平台（默认: both）")

    # diff
    p_diff = sub.add_parser("diff", help="对比清单(uploaded=true) vs 仓库实际文件")
    p_diff.add_argument("repo", help="仓库名")

    # sync-readme
    p_sync = sub.add_parser("sync-readme", help="根据仓库实际文件全量重新生成 README.md")
    p_sync.add_argument("repo", help="仓库名")

    # set-uploaded
    p_set = sub.add_parser("set-uploaded", help="标记指定平台为已上传（不更新版本号）")
    p_set.add_argument("repo", help="仓库名")
    p_set.add_argument("name", help="条目名称")
    p_set.add_argument("--platform", choices=["gitee", "github", "both"], default="both",
                       help="指定平台（默认: both）")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "list": cmd_list,
        "add": cmd_add,
        "remove": cmd_remove,
        "check": cmd_check,
        "version": cmd_version,
        "set-uploaded": cmd_set_uploaded,
        "diff": cmd_diff,
        "sync-readme": cmd_sync_readme,
    }
    commands[args.command](args)

if __name__ == "__main__":
    main()
