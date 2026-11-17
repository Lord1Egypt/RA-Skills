#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wipo_lex_fetch.py — 从 WIPO Lex 文本页抓取条约/细则全文（逐字），并写入技能 references。

用途
----
把 WIPO Lex 官方文本页（形如 https://www.wipo.int/wipolex/en/text/384735）的**全文**
落地为 Markdown，替代此前的「要点详解」摘要。用于条约、议定书、实施细则、行政规程等
需要逐字引用的规范性文本。

设计要点（踩坑记录，勿改回）
--------------------------
· WIPO Lex 文本页为服务端渲染，正文在 HTML 中，**不需要浏览器**（与 Fee Calculator 不同）。
· 同一页面可能同时包含**两份文本**（例如议定书记录页内含协定正文，用于互参）。
  因此必须用「起止标记」显式切分，不能整页直取——否则会把两份条约混成一份。
· 正文中的中文存在排版性空格（如「第 一 条」「财 务」），抓取时按「CJK 之间去空格」归一，
  不改动任何文字；拉丁字母/数字之间的空格保留。
· 抓取后必须核对：首段、末段、关键条号计数（见 --inspect 输出），确认无截断。

用法
----
勘察（不改文件）：
    py -B wipo_lex_fetch.py --url https://www.wipo.int/wipolex/en/text/384637 --inspect
抓取（写入 references/）：
    py -B wipo_lex_fetch.py --url https://www.wipo.int/wipolex/en/text/384735 \
        --out references/madrid-agreement.md \
        --title "《商标国际注册马德里协定》" --source "WIPO Lex text/384735（中文正式翻译）" \
        --start-marker "第 一 条" --end-marker "[[EOF]]"

退出码：0 成功；1 网络/页面异常；2 找不到起止标记（未写入任何文件）。
"""

from __future__ import annotations

import argparse
import html as html_lib
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (compatible; madrid-trademark-skill/1.0; +https://www.wipo.int/wipolex/)"

CJK = r"\u3000-\u303f\u3400-\u4dbf\u4e00-\u9fff\uff00-\uffef"
# 只吃「水平空白」——**绝不能包含 \n**：中文行尾/行首都是 CJK，用 \s 会把所有换行
# 一并吃掉，导致目录与全部段落被压成一整行（曾真实发生，务必保持 [ \t\u3000]）。
HSPACE = r"[ \t\u3000]"
SPACE_BETWEEN_CJK = re.compile(rf"(?<=[{CJK}]){HSPACE}+(?=[{CJK}])")
SPACE_CJK_DIGIT = re.compile(rf"(?<=[{CJK}]){HSPACE}+(?=\d)|(?<=\d){HSPACE}+(?=[{CJK}])")


def configure_stdout() -> None:
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if reconfigure is not None:
        try:
            reconfigure(encoding="utf-8")
        except (ValueError, OSError):
            pass


def fetch(url: str, timeout: int = 60) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", "ignore")


def extract_document_html(raw: str) -> str:
    """取出内嵌的文档 HTML。

    WIPO Lex 文本页把**整份文档**以完整的 HTML 文档形式嵌在 `<div id="printID" …>` 内
    （页尾官方脚注也在其中，其中可能引用其它条约条文原文——那是脚注，不是混入他文）。
    若整页直取，页头导航会成为正文首行、且容易被 `</head>`/`</footer>` 之类的粗剥离
    规则吃掉正文尾部（曾导致议定书第 13–16 条丢失）。
    """
    marker = re.search(r'id="printID"[^>]*>', raw)
    search_from = marker.end() if marker else 0
    start = raw.find("<html", search_from)
    if start == -1:
        start = search_from
    end = raw.find("</html>", start)
    if end == -1:
        end = len(raw)
    return raw[start:end]


def strip_boilerplate(raw: str) -> str:
    """去掉脚本、样式与页头，保留正文相关的块级结构。

    注意：必须**同时按开标签与闭标签**切行——WIPO Lex 的官方目录是缺 `</td>` 的表格，
    只按闭标签切行会把整份目录压成一整行（并因 CJK 去空格而完全失去分隔）。
    """
    text = re.sub(r"(?is)<(script|style|head|noscript)[^>]*>.*?</\1>", " ", raw)
    text = re.sub(r"(?is)<br\s*/?>", "\n", text)
    text = re.sub(r"(?is)<(p|div|li|ol|ul|tr|td|th|h[1-6]|table|section|article)\b[^>]*>", "\n", text)
    text = re.sub(r"(?is)</(p|div|li|ul|ol|tr|td|th|h[1-6]|table|section|article)>", "\n", text)
    text = re.sub(r"(?is)<[^>]+>", " ", text)
    text = html_lib.unescape(text)
    text = text.replace("\u00a0", " ").replace("\u3000", " ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    lines: list[str] = []
    nav_noise = re.compile(
        r"^(About Intellectual Property|IP Training|Respect for IP|IP Outreach|IP for|IP and|"
        r"Patent & Technology Information|Trademark Information|Design Information|Geographical|"
        r"Skip to|Hidden|WIPO Lex|Menu|Search)"
    )
    for line in text.split("\n"):
        line = re.sub(r"[ \t]+", " ", line).strip()
        if not line or nav_noise.match(line):
            continue
        lines.append(line)
    return "\n".join(lines)


def normalize_spaces(text: str) -> str:
    """排版性空格归一（CJK 之间、CJK 与数字之间去空格），不改动任何文字。"""
    previous = None
    while previous != text:
        previous = text
        text = SPACE_BETWEEN_CJK.sub("", text)
        text = SPACE_CJK_DIGIT.sub("", text)
    return text


def slice_document(text: str, start_marker: str | None, end_marker: str | None) -> str:
    start = 0
    if start_marker:
        idx = text.find(start_marker)
        if idx < 0:
            raise LookupError(f"找不到起始标记：{start_marker!r}")
        start = idx
    end = len(text)
    if end_marker:
        idx = text.find(end_marker, start)
        if idx < 0:
            raise LookupError(f"找不到结束标记：{end_marker!r}")
        end = idx
    return text[start:end].strip("\n")


def inspect(url: str) -> None:
    raw = fetch(url)
    document_html = extract_document_html(raw)
    text = strip_boilerplate(document_html)
    normalized = normalize_spaces(text)
    print(f"URL: {url}")
    print(f"内嵌文档 HTML 字节={len(document_html)}（整页 {len(raw)}）")
    print(f"HTML bytes={len(raw)}  文本行数={len(text.splitlines())}  归一后字符数={len(normalized)}")
    print("\n--- 结构锚点（id 属性，前 40 个）---")
    ids = sorted(set(re.findall(r'id="([A-Za-z0-9_\-]+)"', raw)))
    print(", ".join(ids[:40]) if ids else "（无）")
    print("\n--- h1-h3 标题（前 20 个及其字符位置）---")
    for match in list(re.finditer(r"(?is)<h[1-3][^>]*>(.*?)</h[1-3]>", raw))[:20]:
        title = re.sub(r"\s+", " ", html_lib.unescape(re.sub(r"<[^>]+>", "", match.group(1)))).strip()
        print(f"  [{match.start()}] {title[:80]}")
    print("\n--- 疑似文档起始/分割标记的字符位置（归一后文本）---")
    for marker in ["第一条", "第 一 条", "议定书实施细则", "行政规程", "马德里协定", "本议定书",
                   "过渡条款", "保存人的职责", "第四十一条", "第19条", "第 一 部 分"]:
        positions = [m.start() for m in re.finditer(re.escape(normalize_spaces(marker)), normalized)]
        if positions:
            print(f"  {marker!r}: {positions[:8]}")
    print("\n--- 首 200 字 ---")
    print(normalized[:200].replace("\n", " | "))
    print("\n--- 末 200 字 ---")
    print(normalized[-200:].replace("\n", " | "))


def capture(url: str, out_path: Path, title: str, source: str, start_marker: str | None,
            end_marker: str | None, version_note: str | None,
            preserve_notes: Path | None = None) -> int:
    raw = fetch(url)
    text = normalize_spaces(strip_boilerplate(extract_document_html(raw)))
    try:
        body = slice_document(text, normalize_spaces(start_marker) if start_marker else None,
                              normalize_spaces(end_marker) if end_marker else None)
    except LookupError as exc:
        print(f"[ERR] {exc}——未写入文件", file=sys.stderr)
        return 2

    header = [
        f"# {title}",
        "",
        f"> **来源**：{source}",
        f"> **原文页**：{url}",
        f"> **抓取日期**：{date.today().isoformat()}（逐字全文，非摘要；仅做排版性空格归一，未改动任何文字）",
    ]
    if version_note:
        header.append(f"> **版本**：{version_note}")
    header += [
        "> **用途**：条款原文引用；如需按条定位，请检索「第X条」/「第X条之Y」/「Rule N」。",
        "> 抓取工具：`scripts/wipo_lex_fetch.py`（可复核、可重跑；页面更新后重新抓取即可）",
        "",
        "---",
        "",
    ]
    appendix = ""
    # 幂等重抓：若目标文件已含「附录」，自动保留，避免重抓时丢失或重复
    if not preserve_notes and out_path.exists():
        existing = out_path.read_text(encoding="utf-8")
        marker = existing.find("## 附录：")
        if marker > 0:
            appendix = "\n\n---\n\n" + existing[marker:].strip("\n") + "\n"
            print(f"[INFO] 已保留目标文件中原有附录 {len(appendix)} 字符（幂等重抓）")
    if preserve_notes and Path(preserve_notes).exists():
        old = Path(preserve_notes).read_text(encoding="utf-8").splitlines()
        # 去掉旧文件的首个 H1 与紧随的来源引用块，其余整体作为附录保留
        start = 0
        for index, line in enumerate(old):
            if line.startswith("# "):
                start = index + 1
                continue
            if line.startswith(">") or not line.strip():
                if start == index or line.startswith(">"):
                    start = index + 1
                    continue
            break
        notes_body = "\n".join(old[start:]).strip("\n")
        appendix = (
            "\n\n---\n\n"
            "## 附录：要点与勘误（本技能整理，非官方文本；条文正文以上文逐字全文为准）\n\n"
            f"{notes_body}\n"
        )
        print(f"[INFO] 已保留原要点内容 {len(notes_body)} 字符作为附录")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(header) + body + "\n" + appendix, encoding="utf-8")
    print(f"[OK] {out_path}  正文 {len(body)} 字符；总计 {len(body) + len(appendix)} 字符")
    return 0


def main(argv=None) -> int:
    configure_stdout()
    parser = argparse.ArgumentParser(description="WIPO Lex 全文抓取（逐字落地为 Markdown）")
    parser.add_argument("--url", required=True, help="WIPO Lex 文本页 URL")
    parser.add_argument("--inspect", action="store_true", help="仅勘察结构，不写文件")
    parser.add_argument("--out", help="输出文件（相对路径按技能根目录解析）")
    parser.add_argument("--title", help="文档标题（写入 H1）")
    parser.add_argument("--source", default="WIPO Lex", help="来源描述（写入文件头）")
    parser.add_argument("--version-note", help="版本说明（写入文件头）")
    parser.add_argument("--start-marker", help="正文起始标记（含该标记）")
    parser.add_argument("--end-marker", help="正文结束标记（不含该标记）")
    parser.add_argument("--preserve-notes",
                        help="把指定的旧文件（要点详解）作为「附录：要点与勘误」保留在全文之后")
    args = parser.parse_args(argv)

    try:
        if args.inspect:
            inspect(args.url)
            return 0
        if not (args.out and args.title):
            print("[ERR] 抓取模式须同时提供 --out 与 --title", file=sys.stderr)
            return 2
        out_path = Path(args.out)
        if not out_path.is_absolute():
            out_path = SKILL_DIR / out_path
        preserve = args.preserve_notes
        if preserve:
            preserve = Path(preserve)
            if not preserve.is_absolute():
                preserve = SKILL_DIR / preserve
        return capture(args.url, out_path, args.title, args.source,
                       args.start_marker, args.end_marker, args.version_note, preserve)
    except Exception as exc:  # noqa: BLE001
        print(f"[ERR] {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
