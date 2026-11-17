"""
push_to_obsidian.py — 推送简报到 Obsidian vault

三级 fallback：
  1. vault 路径（重试 3 次）
  2. ASCII 文件名
  3. 脚本目录 saved/

环境变量：
  OBSIDIAN_VAULT_PATH — vault 根路径（默认 E:\\Obsidian-Vault\\00-Inbox）
"""
from __future__ import annotations

import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path


def _safe_filename(name: str) -> str:
    """转 ASCII 安全文件名。"""
    return re.sub(r"[^\w\-\.]", "_", name)


def push(md_content: str, date_str: str, vault_path: Path) -> dict:
    """推送 markdown 到 vault，三级 fallback。"""
    filename = f"global-skill-daily_{date_str}.md"
    target = vault_path / filename

    # 添加 frontmatter
    frontmatter = f"""---
title: 全球 Skill 生态日报 {date_str}
date: {date_str}
tags: [skill-daily, global, clawhub, skillhub, ecosystem]
source: global-skill-daily
---

"""
    content_with_fm = frontmatter + md_content

    # Level 1: vault 路径，重试 3 次
    for attempt in range(3):
        try:
            vault_path.mkdir(parents=True, exist_ok=True)
            target.write_text(content_with_fm, encoding="utf-8")
            return {
                "success": True,
                "path": str(target),
                "fallback_level": 1,
                "attempts": attempt + 1,
            }
        except (OSError, PermissionError) as e:
            print(f"[push_to_obsidian] attempt {attempt+1}/3 failed: {e}")
            if attempt < 2:
                time.sleep(1)

    # Level 2: ASCII 文件名
    ascii_filename = _safe_filename(filename)
    ascii_target = vault_path / ascii_filename
    try:
        vault_path.mkdir(parents=True, exist_ok=True)
        ascii_target.write_text(content_with_fm, encoding="utf-8")
        return {
            "success": True,
            "path": str(ascii_target),
            "fallback_level": 2,
            "attempts": 3,
        }
    except (OSError, PermissionError) as e:
        print(f"[push_to_obsidian] ASCII filename failed: {e}")

    # Level 3: 脚本目录 saved/
    saved_dir = Path(__file__).parent.parent / "saved"
    saved_dir.mkdir(parents=True, exist_ok=True)
    saved_target = saved_dir / filename
    try:
        saved_target.write_text(content_with_fm, encoding="utf-8")
        return {
            "success": True,
            "path": str(saved_target),
            "fallback_level": 3,
            "attempts": 3,
        }
    except (OSError, PermissionError) as e:
        return {
            "success": False,
            "error": str(e),
            "fallback_level": 3,
            "attempts": 3,
        }


def main():
    if len(sys.argv) < 3:
        print("Usage: python push_to_obsidian.py <md_path> <date_str>")
        sys.exit(1)

    md_path = Path(sys.argv[1])
    date_str = sys.argv[2]

    if not md_path.exists():
        print(f"[push_to_obsidian] MD not found: {md_path}")
        sys.exit(1)

    md_content = md_path.read_text(encoding="utf-8")

    # 读 vault 路径
    import os
    vault_path_str = os.environ.get("OBSIDIAN_VAULT_PATH", r"E:\Obsidian-Vault\00-Inbox")
    vault_path = Path(vault_path_str)

    result = push(md_content, date_str, vault_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result["success"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
