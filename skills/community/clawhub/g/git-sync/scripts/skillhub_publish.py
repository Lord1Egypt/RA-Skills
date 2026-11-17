"""SkillHub 发布器 — git-sync 子模块"""
import sys, subprocess, json, os, shutil, tempfile
from _paths import WORK_REPO

def main():
    if len(sys.argv) < 3:
        print("用法: skillhub_publish.py <name> <version>")
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

    # SkillHub CLI 路径
    skillhub_cli = os.path.expanduser("~/.skillhub/skills_store_cli.py")
    if not os.path.isfile(skillhub_cli):
        print(f"  ❌ 未找到 SkillHub CLI: {skillhub_cli}")
        sys.exit(1)

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
        sys.executable, skillhub_cli, "publish", skill_dir,
        "--changelog", changelog_line,
    ]

    # SkillHub 不允许 .gitignore 等 git 元文件：发布前移出技能目录（备份到系统临时目录，避免 .skh_bak 残留目录内），发布后恢复
    gi = os.path.join(skill_dir, ".gitignore")
    gi_bak = ""
    if os.path.isfile(gi):
        gi_bak = os.path.join(tempfile.gettempdir(), f".gitignore_skh_{name}_{version}")
        shutil.copy2(gi, gi_bak)
        os.remove(gi)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=work_repo)
    finally:
        if gi_bak and os.path.isfile(gi_bak) and not os.path.isfile(gi):
            shutil.copy2(gi_bak, gi)
        if gi_bak and os.path.isfile(gi_bak):
            os.remove(gi_bak)
    if result.returncode == 0:
        print(f"  ✅ SkillHub: {name}")
    else:
        print(f"  ⚠️  SkillHub 结果: {result.stderr[:300]}")

if __name__ == "__main__":
    main()
