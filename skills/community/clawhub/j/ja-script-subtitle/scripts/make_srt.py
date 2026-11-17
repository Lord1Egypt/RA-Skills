#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Step 3b —— 由「日文 SRT + 中文翻译字典」生成 纯中文 / 双语 SRT

用法:
    python make_srt.py <ja.srt> <zh.json> <out_dir> <prefix>

zh.json 形如 {"1": "中文…", "2": "中文…"}，键 = 台本非空行连续序号，
必须与 align_gen.py 输出的 SRT 序号严格一致（这是最容易错位的地方）。
生成: <out_dir>/<prefix>_zh.srt, <out_dir>/<prefix>_bilingual.srt
"""
import json, os, sys

if len(sys.argv) < 5:
    sys.exit(__doc__)
src, zhjson, outdir, prefix = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
os.makedirs(outdir, exist_ok=True)

ZH = {int(k): v for k, v in json.load(open(zhjson, encoding="utf-8")).items()}


def parse_srt(path):
    blocks, cur = [], {}
    for raw in open(path, encoding="utf-8"):
        raw = raw.rstrip("\n")
        if "-->" in raw:
            cur = {"time": raw}
        elif raw.strip() and cur.get("time") and not raw.strip().isdigit():
            cur["text"] = (cur.get("text", "") + "\n" + raw).strip()
        elif not raw.strip() and cur.get("text"):
            blocks.append(cur); cur = {}
    if cur.get("text"):
        blocks.append(cur)
    return blocks


blocks = parse_srt(src)
miss = [i for i in range(1, len(blocks) + 1) if i not in ZH]
if miss:
    print("!! 缺译文序号:", miss)
    print("   请检查 zh.json 的键是否为「非空行连续序号」")

zh, bi = [], []
for i, bk in enumerate(blocks, 1):
    z = ZH.get(i, "")
    zh.append(f"{i}\n{bk['time']}\n{z}\n")
    bi.append(f"{i}\n{bk['time']}\n{bk['text']}\n{z}\n")

open(f"{outdir}/{prefix}_zh.srt", "w", encoding="utf-8").write("\n".join(zh))
open(f"{outdir}/{prefix}_bilingual.srt", "w", encoding="utf-8").write("\n".join(bi))
print(f"行数 {len(blocks)} → {outdir}/{prefix}_zh.srt, {prefix}_bilingual.srt")
