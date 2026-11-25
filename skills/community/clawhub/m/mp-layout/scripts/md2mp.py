#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Markdown -> 微信公众号可粘贴的内联样式 HTML。零依赖，Python 3.8+。

用法:
    python3 md2mp.py article.md --color "#2F6F5E" -o article.html
    cat article.md | python3 md2mp.py --color "#1F3A5F" > article.html

支持: # / ## / ### 标题(# 视为文章标题, 输出为 H2 之上的大标题), 段落, **加粗**, *强调*,
> 引用, - / 1. 列表, ![说明](url) 图片, [文字](url) 外链 -> 文字 + 脚注, --- 分隔线。
"""
import argparse, html, re, sys

TEXT = "#3A3A3A"
MUTED = "#8A8A8A"
FONT = '-apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", "Microsoft YaHei", sans-serif'

def styles(c):
    return {
        "section": f'padding: 0 16px; font-size: 16px; line-height: 1.75; letter-spacing: 1px; color: {TEXT}; font-family: {FONT};',
        "title": f'font-size: 22px; font-weight: 700; color: {TEXT}; margin: 1em 0 1.5em; line-height: 1.4;',
        "p": 'margin: 0 0 1.2em; text-align: left;',
        "h2": f'font-size: 20px; font-weight: 700; color: {c}; margin: 2em 0 1em; line-height: 1.4; letter-spacing: 1px;',
        "h2mark": f'display: inline-block; width: 6px; height: 20px; background: {c}; border-radius: 3px; vertical-align: -3px; margin-right: 10px;',
        "h3": f'font-size: 17px; font-weight: 700; color: {TEXT}; margin: 1.6em 0 0.8em; line-height: 1.5;',
        "strong": f'color: {c}; font-weight: 700;',
        "em": f'font-style: normal; border-bottom: 2px solid {c}; padding-bottom: 1px;',
        "quote": f'margin: 1.5em 0; padding: 0.2em 0 0.2em 14px; border-left: 3px solid {c}; color: {MUTED}; font-size: 15px;',
        "list": 'margin: 0 0 1.2em; padding-left: 1.4em;',
        "li": 'margin: 0.3em 0;',
        "img": 'display: block; width: 100%; border-radius: 6px; margin: 1.6em auto 0.5em;',
        "cap": f'text-align: center; font-size: 13px; color: {MUTED}; margin: 0 0 1.6em; letter-spacing: 0;',
        "hr": f'text-align: center; color: {c}; margin: 2em 0; letter-spacing: 8px;',
        "foot": f'font-size: 13px; color: {MUTED}; margin: 2em 0 0; word-break: break-all;',
    }

class Conv:
    def __init__(self, color):
        self.s = styles(color)
        self.footnotes = []
        self.images = 0

    def inline(self, t):
        t = html.escape(t, quote=False)
        # 外链 -> 文字 + 脚注编号
        def link(m):
            self.footnotes.append(m.group(2))
            return f'{m.group(1)}<sup style="color:{MUTED};font-size:12px;">[{len(self.footnotes)}]</sup>'
        t = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', link, t)
        t = re.sub(r'\*\*(.+?)\*\*', lambda m: f'<strong style="{self.s["strong"]}">{m.group(1)}</strong>', t)
        t = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', lambda m: f'<em style="{self.s["em"]}">{m.group(1)}</em>', t)
        t = re.sub(r'`([^`]+)`', lambda m: f'<code style="font-size:14px;padding:1px 4px;background:#F5F5F5;border-radius:3px;">{m.group(1)}</code>', t)
        return t

    def convert(self, md):
        out = []
        lines = md.splitlines()
        i, n = 0, len(lines)
        para = []
        def flush():
            if para:
                out.append(f'<p style="{self.s["p"]}">{self.inline(" ".join(x.strip() for x in para))}</p>')
                para.clear()
        while i < n:
            ln = lines[i]
            st = ln.strip()
            if not st:
                flush(); i += 1; continue
            m = re.match(r'^(#{1,3})\s+(.*)$', st)
            if m:
                flush()
                lvl, txt = len(m.group(1)), self.inline(m.group(2))
                if lvl == 1:
                    out.append(f'<h1 style="{self.s["title"]}">{txt}</h1>')
                elif lvl == 2:
                    out.append(f'<h2 style="{self.s["h2"]}"><span style="{self.s["h2mark"]}"></span>{txt}</h2>')
                else:
                    out.append(f'<h3 style="{self.s["h3"]}">{txt}</h3>')
                i += 1; continue
            m = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)$', st)
            if m:
                flush(); self.images += 1
                cap = m.group(1) or f'图 {self.images}'
                out.append(f'<img src="{html.escape(m.group(2))}" alt="{html.escape(cap)}" style="{self.s["img"]}">')
                out.append(f'<p style="{self.s["cap"]}">{html.escape(cap)}</p>')
                i += 1; continue
            if re.match(r'^(-{3,}|\*{3,})$', st):
                flush(); out.append(f'<p style="{self.s["hr"]}">· · ·</p>'); i += 1; continue
            if st.startswith('>'):
                flush(); q = []
                while i < n and lines[i].strip().startswith('>'):
                    q.append(lines[i].strip()[1:].strip()); i += 1
                out.append(f'<blockquote style="{self.s["quote"]}">{self.inline(" ".join(q))}</blockquote>')
                continue
            m = re.match(r'^(\d+\.|[-*+])\s+(.*)$', st)
            if m:
                flush(); ordered = m.group(1)[0].isdigit(); items = []
                while i < n:
                    mm = re.match(r'^(\d+\.|[-*+])\s+(.*)$', lines[i].strip())
                    if not mm: break
                    items.append(f'<li style="{self.s["li"]}">{self.inline(mm.group(2))}</li>'); i += 1
                tag = 'ol' if ordered else 'ul'
                out.append(f'<{tag} style="{self.s["list"]}">{"".join(items)}</{tag}>')
                continue
            para.append(ln); i += 1
        flush()
        if self.footnotes:
            notes = '<br>'.join(f'[{k+1}] {html.escape(u)}' for k, u in enumerate(self.footnotes))
            out.append(f'<p style="{self.s["foot"]}">{notes}</p>')
        body = "\n".join(out)
        return f'<section style="{self.s["section"]}">\n{body}\n</section>\n'

def main():
    ap = argparse.ArgumentParser(description="Markdown -> 公众号内联样式 HTML")
    ap.add_argument("src", nargs="?", help="Markdown 文件，缺省读 stdin")
    ap.add_argument("--color", default="#2F6F5E", help="品牌色 HEX，默认松绿 #2F6F5E")
    ap.add_argument("-o", "--out", help="输出文件，缺省写 stdout")
    a = ap.parse_args()
    if not re.match(r'^#[0-9A-Fa-f]{6}$', a.color):
        sys.exit("--color 必须是 #RRGGBB 形式")
    md = open(a.src, encoding="utf-8").read() if a.src else sys.stdin.read()
    c = Conv(a.color)
    out = c.convert(md)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(out)
    else:
        sys.stdout.write(out)
    sys.stderr.write(f"[md2mp] 图片 {c.images} 张（建议 3–5），外链转脚注 {len(c.footnotes)} 条\n")

if __name__ == "__main__":
    main()
