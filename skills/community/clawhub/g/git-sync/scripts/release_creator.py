"""GitHub + Gitee Release 创建器 — git-sync 子模块
用法: release_creator.py <name> <type> <version>
  创建 tag + GitHub Release + Gitee 发行版
  源码包由平台自动生成，不需上传
"""
import subprocess, sys, json, os
from _paths import WORK_REPO, CONFIG_FILE

WORK_REPO_STR = str(WORK_REPO)


def _get_repos() -> tuple:
    """从 config.json 读取仓库全名"""
    try:
        cfg = json.load(open(CONFIG_FILE, encoding="utf-8"))
        g = cfg.get("gitee", {})
        h = cfg.get("github", {})
        gitee = f"{g.get('user','wUwproject')}/{g.get('repo','workbuddy-skills')}"
        github = f"{h.get('user','Ldxs001')}/{h.get('repo','workbuddy-skills')}"
        return gitee, github
    except:
        return "wUwproject/workbuddy-skills", "Ldxs001/workbuddy-skills"


def _get_gitee_token() -> str:
    token = os.environ.get("GITEE_TOKEN", "")
    if token:
        return token
    try:
        cfg = json.load(open(CONFIG_FILE, encoding="utf-8"))
        return cfg.get("gitee_token", "")
    except Exception:
        return ""


def _get_github_token() -> str:
    remote_url = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=WORK_REPO_STR, capture_output=True, text=True
    ).stdout.strip()
    token = ""
    if ":" in remote_url and "@" in remote_url:
        token_part = remote_url.split("//")[1].split("@")[0]
        if ":" in token_part:
            token = token_part.split(":")[1]
    elif "token" in remote_url:
        token = remote_url.split("token=")[1].split("&")[0]
    return token


def main():
    if len(sys.argv) < 4:
        print("用法: release_creator.py <name> <type> <version>")
        sys.exit(1)
    name, typ, version = sys.argv[1], sys.argv[2], sys.argv[3]
    gitee_repo, github_repo = _get_repos()
    tag = f"v{version}" if typ == "agent" else f"{name}-v{version}"
    body = f"## {name} v{version}\n\n自动发布 by git-sync"

    # 1. tag
    subprocess.run(["git", "tag", tag, "-f"], cwd=WORK_REPO_STR, capture_output=True)

    # 2. push tag 到双平台
    for rm in ["origin", "gitee"]:
        subprocess.run(["git", "push", rm, tag, "-f"], cwd=WORK_REPO_STR, capture_output=True)

    # 3. GitHub Release（源码包由平台自动生成）
    gh_token = _get_github_token()
    if gh_token:
        data = json.dumps({
            "tag_name": tag, "name": f"{name} v{version}",
            "body": body, "draft": False, "prerelease": False
        })
        r = subprocess.run([
            "curl", "-s", "-X", "POST",
            f"https://api.github.com/repos/{github_repo}/releases",
            "-H", f"Authorization: token {gh_token}",
            "-H", "Content-Type: application/json", "-d", data
        ], capture_output=True, text=True)
        try:
            u = json.loads(r.stdout)
            if "id" in u:
                print(f"  ✅ GitHub Release: {u.get('html_url', '')}")
            else:
                print(f"  ℹ️  GitHub: {r.stdout[:200]}")
        except:
            print(f"  ⚠️  GitHub Release 异常: {r.stdout[:200]}")
    else:
        print("  ⚠️  无 GitHub token，已推送 tag")

    # 4. Gitee 发行版（源码包由平台自动生成）
    gitee_token = _get_gitee_token()
    if gitee_token:
        data = json.dumps({
            "access_token": gitee_token, "tag_name": tag,
            "target_commitish": "main", "name": f"{name} v{version}",
            "body": body, "prerelease": False
        })
        r = subprocess.run([
            "curl", "-s", "-X", "POST",
            f"https://gitee.com/api/v5/repos/{gitee_repo}/releases",
            "-H", "Content-Type: application/json;charset=UTF-8", "-d", data
        ], capture_output=True, text=True)
        try:
            u = json.loads(r.stdout)
            if "id" in u:
                print(f"  ✅ Gitee 发行版: https://gitee.com/{gitee_repo}/releases/{tag}")
            else:
                print(f"  ℹ️  Gitee: {r.stdout[:200]}")
        except:
            print(f"  ⚠️  Gitee 发行版异常: {r.stdout[:200]}")
    else:
        print("  ⚠️  无 Gitee token，已推送 tag")


if __name__ == "__main__":
    main()
