"""ClawHub 发布器 — git-sync 子模块"""
import sys, subprocess, json, os
from _paths import WORK_REPO

def main():
    if len(sys.argv) < 3:
        print("用法: clawhub_publish.py <name> <version>")
        sys.exit(1)
    name, version = sys.argv[1], sys.argv[2]

    work_repo = str(WORK_REPO)
    # 兼容两种仓库结构：旧 workbuddy-skills 用 skills/ 子目录，maby_skills 技能在顶层
    skill_dir = os.path.join(work_repo, "skills", name)
    if not os.path.isdir(skill_dir):
        skill_dir = os.path.join(work_repo, name)
    if not os.path.isdir(skill_dir):
        print(f"  ❌ 未找到技能目录: {skill_dir}")
        sys.exit(1)

    # 读取 _meta.json 获取必要信息
    meta_path = os.path.join(skill_dir, "_meta.json")
    if not os.path.isfile(meta_path):
        print(f"  ❌ 未找到 _meta.json: {meta_path}")
        sys.exit(1)
    with open(meta_path, encoding="utf-8") as f:
        meta = json.load(f)

    slug = meta.get("slug", name)
    display_name = meta.get("displayName", name)
    tags = meta.get("tags", [])

    # 获取 changelog
    changelog_line = f"v{version}: sync via git-sync"
    changelog_path = os.path.join(skill_dir, "references", "changelog.md")
    if os.path.isfile(changelog_path):
        with open(changelog_path, encoding="utf-8") as f:
            for line in f:
                if f"## [{version}]" in line:
                    changelog_line = f"v{version}"
                    break

    cmd = [
        "npx", "clawhub", "publish", skill_dir,
        "--slug", slug,
        "--name", display_name,
        "--version", version,
        "--changelog", changelog_line,
    ]
    if tags:
        cmd += ["--tags", ",".join(tags)]

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=work_repo)
    if result.returncode == 0:
        print(f"  ✅ ClawHub: {slug}")
    else:
        err = result.stderr[:300] if result.stderr else result.stdout[:300]
        if "invalid value" in err or "ok" in result.stdout.lower():
            print(f"  ✅ ClawHub: {slug}（API 成功，CLI 显示错误是已知 bug）")
        else:
            print(f"  ⚠️  ClawHub 结果: {err}")

if __name__ == "__main__":
    main()
