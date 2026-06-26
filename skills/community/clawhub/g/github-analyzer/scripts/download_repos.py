#!/usr/bin/env python3
"""
下载 GitHub 仓库代码包（zip）
用法: python3 download_repos.py "owner/repo1" "owner/repo2" ...
"""
import sys
import os
import urllib.request
import zipfile
import json

TOKEN = os.environ.get("GITHUB_TOKEN", "")
DOWNLOAD_DIR = os.path.expanduser("~/Downloads/github-analyzer")

def download_repo(full_name: str, out_dir: str):
    owner, repo = full_name.strip("/").split("/")[-2:]

    # 获取默认分支
    headers = {
        "Authorization": f"token {TOKEN}",
        "User-Agent": "github-analyzer/1.0"
    }
    req = urllib.request.Request(
        f"https://api.github.com/repos/{owner}/{repo}",
        headers=headers
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        repo_data = json.loads(r.read())
    branch = repo_data.get("default_branch", "main")

    zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip"
    out_path = os.path.join(out_dir, f"{owner}_{repo}.zip")

    print(f"⬇️  下载 {full_name} ...")
    req = urllib.request.Request(zip_url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as r:
        with open(out_path, "wb") as f:
            f.write(r.read())

    size_mb = os.path.getsize(out_path) / 1024 / 1024
    print(f"✅ 已保存: {out_path} ({size_mb:.1f} MB)")
    return out_path

def main():
    if len(sys.argv) < 2:
        print("用法: python3 download_repos.py owner/repo [owner/repo ...]")
        sys.exit(1)

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    results = []

    for arg in sys.argv[1:]:
        if "github.com" in arg:
            parts = arg.rstrip("/").split("github.com/")[-1].split("/")
            full_name = "/".join(parts[:2])
        else:
            full_name = arg
        try:
            path = download_repo(full_name, DOWNLOAD_DIR)
            results.append({"repo": full_name, "path": path, "status": "ok"})
        except Exception as e:
            print(f"❌ 下载失败 {full_name}: {e}")
            results.append({"repo": full_name, "error": str(e), "status": "failed"})

    print(f"\n📦 下载完成，文件保存在: {DOWNLOAD_DIR}")
    for r in results:
        if r["status"] == "ok":
            print(f"  ✅ {r['repo']} → {r['path']}")
        else:
            print(f"  ❌ {r['repo']} → {r['error']}")

if __name__ == "__main__":
    main()
