#!/usr/bin/env python3
"""
开发帮助工具：在本地开发目录修改后，同步更新到 OpenClaw 工作区。

用法：
    python3 dev_sync.py              # 同步到工作区（复制，不含 accounts/ 等个人数据）
    python3 dev_sync.py --publish    # 同步 + 发布到 ClawHub
    python3 dev_sync.py --install    # 从 ClawHub 安装最新版到工作区
"""

import json
import os
import shutil
import subprocess
import sys

# ── 路径 ───────────────────────────────────────────────────────────────────

DEV_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_SKILLS = os.path.expanduser("~/.openclaw/workspace/skills")
WORKSPACE_TARGET = os.path.join(WORKSPACE_SKILLS, "mail-assistant")
DATA_DIR = os.path.expanduser("~/.openclaw/workspace/.email-assistant")

EXCLUDE = {
    ".clawhub", "_meta.json",   # ClawHub metadata (keep original)
    "accounts",                 # personal data
    "auto_reply_rules.json",    # personal data
    "sync_state.json",          # personal data
    "__pycache__",              # cache
    ".git",
}


def sync_to_workspace():
    """Copy dev files to workspace skill directory (skip personal data)."""
    print(f"[SYNC] {DEV_DIR} → {WORKSPACE_TARGET}")

    if not os.path.exists(WORKSPACE_TARGET):
        os.makedirs(WORKSPACE_TARGET)

    for item in os.listdir(DEV_DIR):
        if item in EXCLUDE:
            continue

        src = os.path.join(DEV_DIR, item)
        dst = os.path.join(WORKSPACE_TARGET, item)

        if os.path.isdir(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
            print(f"  📁 {item}/")
        else:
            shutil.copy2(src, dst)
            print(f"  📄 {item}")

    print(f"[DONE] 已同步到 OpenClaw 工作区")
    print(f"  目标: {WORKSPACE_TARGET}")
    print(f"  数据: {DATA_DIR}（未动）")


def publish():
    """Sync then publish to ClawHub."""
    sync_to_workspace()
    print()
    print("[PUBLISH] 发布到 ClawHub...")

    # Read current version from SKILL.md metadata
    # Clawhub handles versioning, just pass --version
    result = subprocess.run(
        ["clawhub", "publish", DEV_DIR, "--slug", "mail-assistant",
         "--owner", "fanfan-2011", "--name", "Email Assistant"],
        capture_output=True, text=True, timeout=60,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"[ERROR] 发布失败: {result.stderr}", file=sys.stderr)
    else:
        print("[OK] 发布成功！")


def install():
    """Install the latest version from ClawHub into workspace."""
    print("[INSTALL] 从 ClawHub 安装最新版...")
    result = subprocess.run(
        ["clawhub", "install", "mail-assistant"],
        capture_output=True, text=True, timeout=60,
    )
    print(result.stdout)
    if result.returncode == 0:
        print("[OK] 安装成功！数据目录不受影响。")
    else:
        print(f"[ERROR] 安装失败: {result.stderr}", file=sys.stderr)


def main():
    if "--publish" in sys.argv:
        publish()
    elif "--install" in sys.argv:
        install()
    else:
        sync_to_workspace()


if __name__ == "__main__":
    main()
