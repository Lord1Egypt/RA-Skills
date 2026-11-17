#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""llms-generator — 一键生成 llms.txt（LLMs.txt v2 规范）+ 站点级 AI 可发现性包。
痛点：每个 AI 项目都需要 llms.txt 让 AI 代理发现；手工写慢且不规范。
理论根基：LGD 三律（有籍·有证·有门禁）。Usage:
  python scripts/llms_gen.py --name MyProject --url https://github.com/org/repo --desc "..." [--out llms.txt]
  python scripts/llms_gen.py --name X --url U --desc D --full README.md --out llms.txt   # 含全文
"""
import argparse, datetime, os, sys

def gen_llms(name, url, desc, links=None, full=None):
    now = datetime.date.today().isoformat()
    out = [f"# {name}", "", f"> {desc}", "", "## Ecosystem", ""]
    links = links or []
    for l in links:
        out.append(f"- {l}")
    out += ["", "## Identity & Archive", "",
            "- ORCID: https://orcid.org/0009-0001-0512-1237",
            f"- Repository: {url}", ""]
    if full:
        out += ["## Full content", "", full, ""]
    return "\n".join(out)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--name", required=True)
    p.add_argument("--url", required=True)
    p.add_argument("--desc", required=True)
    p.add_argument("--link", action="append", default=[], help="ecosystem link (repeatable)")
    p.add_argument("--full", help="markdown file to inline as full content")
    p.add_argument("--out", default="llms.txt")
    a = p.parse_args()
    full = open(a.full, encoding="utf-8", errors="replace").read() if a.full else None
    txt = gen_llms(a.name, a.url, a.desc, a.link, full)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(txt)
    print("written:", a.out, "(%d chars)" % len(txt))
    return 0

if __name__ == "__main__":
    sys.exit(main())
