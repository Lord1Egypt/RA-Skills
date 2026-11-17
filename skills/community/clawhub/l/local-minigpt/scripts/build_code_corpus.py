# -*- coding: utf-8 -*-
"""构建代码语料:CPython 官方仓库 3.13 分支的标准库源码(PSF 许可)。

产出:
  data/code_corpus.txt   训练用(约 1.5M 字符的真实 Python 源码)
  data/code_heldout.txt  留出考卷(最后 3 个文件,绝不参与训练)
本地 python3XX.zip 仅含 .pyc(无源码),因此以在线 CPython 源为准。
"""

from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_TRAIN = REPO_ROOT / "data" / "code_corpus.txt"
OUT_HELD = REPO_ROOT / "data" / "code_heldout.txt"

BASE = "https://raw.githubusercontent.com/python/cpython/3.13/Lib/"
MODULES = [
    "argparse.py", "dataclasses.py", "enum.py", "random.py", "functools.py",
    "pathlib.py", "shutil.py", "tempfile.py", "textwrap.py", "uuid.py",
    "difflib.py", "smtplib.py", "ipaddress.py", "inspect.py",
    "json/__init__.py", "json/decoder.py", "json/encoder.py", "json/scanner.py",
    "email/utils.py", "http/server.py",
    "asyncio/base_events.py", "asyncio/tasks.py",
    "unittest/case.py", "xml/etree/ElementTree.py",
]
MAX_TRAIN_CHARS = 1_500_000
MIN_FILE_CHARS = 200
MAX_FILE_CHARS = 120_000
HELDOUT_FILES = 3


def fetch(rel: str) -> str:
    url = BASE + rel
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (MiniGPT-coding-test)"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def main() -> None:
    fetched: list[tuple[str, str]] = []
    total = 0
    ok = fail = 0
    for rel in MODULES:
        try:
            text = fetch(rel)
        except Exception as e:
            print(f"[跳过] {rel}: {e}")
            fail += 1
            continue
        if not (MIN_FILE_CHARS <= len(text) <= MAX_FILE_CHARS) or "\x00" in text:
            print(f"[跳过] {rel}: 长度 {len(text):,} 超出范围")
            fail += 1
            continue
        fetched.append((rel, text))
        total += len(text)
        ok += 1
        print(f"[OK] {rel}: {len(text):,} 字符")
        if ok > len(MODULES):
            break

    if ok == 0:
        print("[失败] 没有取到任何源码;请检查网络。")
        sys.exit(1)

    # 最后 3 个成功的文件留作考卷,绝不参与训练
    train_pairs = fetched[:-HELDOUT_FILES]
    held_pairs = fetched[-HELDOUT_FILES:]
    train_blocks: list[str] = []
    budget = 0
    for rel, text in train_pairs:
        if budget >= MAX_TRAIN_CHARS:
            break
        train_blocks.append(f"# ===== {rel.split('/')[-1]} =====\n{text}")
        budget += len(text)
    held_blocks = [f"# ===== {r.split('/')[-1]} =====\n{t}" for r, t in held_pairs]

    train_text = "\n\n".join(train_blocks)
    held_text = "\n\n".join(held_blocks)
    OUT_TRAIN.write_text(train_text, encoding="utf-8")
    OUT_HELD.write_text(held_text, encoding="utf-8")
    print(f"\n训练语料: {OUT_TRAIN}({len(train_blocks)} 个文件,{len(train_text):,} 字符)")
    print(f"留出考卷: {OUT_HELD}({len(held_blocks)} 个文件,{len(held_text):,} 字符)")


if __name__ == "__main__":
    main()
