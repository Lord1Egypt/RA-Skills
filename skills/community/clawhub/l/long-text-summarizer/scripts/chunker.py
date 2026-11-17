#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chunker.py —— 长文分块器（供 long-text-summarizer 技能使用）

把超长文本/文档切成适合模型上下文的块，支持重叠(overlap)以保留边界语义。
输出 JSON 块列表，agent 可逐块摘要后再做归约(reduce)。

用法:
  python chunker.py file.txt                      # 默认 2000 token/块, 200 重叠
  python chunker.py file.txt --chunk 1500 --overlap 150
  python chunker.py file.txt --out chunks.json    # 写到文件而非 stdout
  python chunker.py file.md  --mode markdown       # 按标题优先切分
"""
import os, sys, json, argparse, re

CHARS_PER_TOKEN = 4  # 经验值，中文约 1.5~2 字/token，取保守值


def read_text(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".txt", ".md", ".markdown", ".py", ".json", ".csv", ".log"):
        return open(path, encoding="utf-8", errors="replace").read()
    if ext == ".docx":
        try:
            from docx import Document
            d = Document(path)
            return "\n".join(p.text for p in d.paragraphs if p.text.strip())
        except ImportError:
            sys.stderr.write("⚠️ 未安装 python-docx，无法读取 docx，请用 txt/md 或先 pip install python-docx\n")
            sys.exit(2)
    # 兜底：当文本读
    return open(path, encoding="utf-8", errors="replace").read()


def split_plain(text, chunk_tokens, overlap_tokens):
    chunk_chars = chunk_tokens * CHARS_PER_TOKEN
    overlap_chars = overlap_tokens * CHARS_PER_TOKEN
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + chunk_chars, n)
        chunks.append(text[start:end])
        if end >= n:
            break
        start = max(end - overlap_chars, start + 1)
    return chunks


def split_markdown(text, chunk_tokens, overlap_tokens):
    """优先按 # 标题切分，使块尽量落在语义边界；超出再按字符切。"""
    lines = text.splitlines()
    blocks, cur, cur_len = [], [], 0
    limit = chunk_tokens * CHARS_PER_TOKEN
    for ln in lines:
        cur.append(ln)
        cur_len += len(ln) + 1
        if cur_len >= limit:
            blocks.append("\n".join(cur))
            cur, cur_len = [], 0
    if cur:
        blocks.append("\n".join(cur))
    # 若块过少，退化到纯字符切
    if len(blocks) <= 1:
        return split_plain(text, chunk_tokens, overlap_tokens)
    return blocks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--chunk", type=int, default=2000, help="每块 token 数")
    ap.add_argument("--overlap", type=int, default=200, help="块间重叠 token 数")
    ap.add_argument("--mode", choices=["plain", "markdown"], default="plain")
    ap.add_argument("--out", default=None, help="输出 JSON 路径，缺省打印到 stdout")
    args = ap.parse_args()

    text = read_text(args.file)
    if args.mode == "markdown" or args.file.lower().endswith((".md", ".markdown")):
        chunks = split_markdown(text, args.chunk, args.overlap)
    else:
        chunks = split_plain(text, args.chunk, args.overlap)

    result = {
        "source": args.file,
        "chunk_tokens": args.chunk,
        "overlap_tokens": args.overlap,
        "num_chunks": len(chunks),
        "chunks": [{"index": i, "text": c} for i, c in enumerate(chunks)],
    }
    if args.out:
        json.dump(result, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"✅ 切成 {len(chunks)} 块，写入 {args.out}")
    else:
        print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
