# -*- coding: utf-8 -*-
"""从开源 chinese-poetry 仓库下载公开领域中文语料作为训练数据。

用法:python scripts/fetch_corpus.py
下载成功 -> 写入 data/train.txt
全部失败 -> 保留 data/demo.txt 作为示例语料(训练脚本会自动回退)
"""

from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT = REPO_ROOT / "data" / "train.txt"

# 均为公开领域古籍文本(https://github.com/chinese-poetry/chinese-poetry)
BASE = "https://raw.githubusercontent.com/chinese-poetry/chinese-poetry/master/"
CANDIDATES = [
    ("古文观止", "蒙学/guwenguanzhi.json"),
    ("论语", "论语/lunyu.json"),
    ("增广贤文", "蒙学/zengguangxianwen.json"),
    ("唐诗三百首", "蒙学/tangshisanbaishou.json"),
    ("诗经", "诗经/shijing.json"),
    ("楚辞", "楚辞/chuci.json"),
]


def collect_strings(obj, out: list) -> None:
    """递归收集 JSON 里的所有字符串(章节名、段落、诗句都要)。"""
    if isinstance(obj, str):
        if obj.strip():
            out.append(obj.strip())
    elif isinstance(obj, list):
        for item in obj:
            collect_strings(item, out)
    elif isinstance(obj, dict):
        for v in obj.values():
            collect_strings(v, out)


def fetch(rel: str):
    url = BASE + urllib.parse.quote(rel)
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (MiniGPT-demo)"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> None:
    blocks: list[str] = []
    for name, url in CANDIDATES:
        try:
            data = fetch(url)
            out: list[str] = []
            collect_strings(data, out)
            text = "\n".join(out)
            if len(text) > 200:
                blocks.append(text)
                print(f"[OK] {name}: {len(text):,} 字符")
            else:
                print(f"[跳过] {name}: 内容为空")
        except Exception as e:  # 网络失败时跳过该源,不影响其他源
            print(f"[跳过] {name}: {e}")

    if not blocks:
        print("[失败] 所有候选源都不可用;可直接使用 data/demo.txt 训练。")
        sys.exit(1)

    text = "\n".join(blocks)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"已写入 {OUT}(共 {len(text):,} 字符)")


if __name__ == "__main__":
    main()
