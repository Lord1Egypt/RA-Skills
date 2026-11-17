#!/usr/bin/env python3
"""
md-faq-to-schema.py — 从 Markdown FAQ 定稿生成 schema.org FAQPage 结构化数据

用途：GEO 内容生产。FAQ 页的问答对是 AI 引擎最易整段摘录的格式；本脚本保证
     「页面可见文字」与「JSON-LD 里的问答」自动一致，避免两处手工维护产生口径漂移。

约定（Markdown 源文件格式）：
  - 每个问答用三级标题：`### 问题原文？`，答案为其后的正文（支持段落/列表/表格）
  - 组标题用 `## `，组分隔用 `---`（脚本会自动跳过）
  - 以 `>` 开头的行视为内部备注/引用，**不进结构化数据**（避免内部信息泄漏）
  - 生产备注之类的尾部章节用 `## 附：` 起头，脚本在第一个 `## 附：` 处截断

用法：
  python3 md-faq-to-schema.py <input.md> [output.json]

校验建议：生成后用 json.loads 复核一遍，并 grep 一遍内部关键词（待人审/工单/备注）
"""
import json
import pathlib
import re
import sys

MARKDOWN_STRIP = [
    (r"\*\*(.+?)\*\*", r"\1"),
    (r"`(.+?)`", r"\1"),
    (r"\[(.+?)\]\(.+?\)", r"\1"),
]
LEAK_WORDS = ("内部备注", "待人审", "工单", "不随文发布")


def table_to_text(text: str) -> str:
    """Markdown 表格 → 可读句子：2 列用「——」，3 列及以上带列头。"""
    lines, res, i = text.split("\n"), [], 0
    while i < len(lines):
        if lines[i].strip().startswith("|"):
            tbl = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                tbl.append(lines[i].strip())
                i += 1
            rows = [[c.strip() for c in r.strip("|").split("|")] for r in tbl]
            rows = [r for r in rows if not all(set(c) <= set("-: ") for c in r)]
            if not rows:
                continue
            header, data = rows[0], rows[1:]
            for r in data:
                if len(r) >= 3:
                    pairs = "；".join(f"{h}：{c}" for h, c in zip(header[1:], r[1:]) if c)
                    res.append(f"{r[0]}——{pairs}。")
                else:
                    res.append(f"{r[0]}——{r[1]}。")
        else:
            res.append(lines[i])
            i += 1
    return "\n".join(res)


def join_lists(text: str) -> str:
    """把连续的列表项合并成一句（用「；」连接），读起来更像答案而不是清单。"""
    out, buf = [], []
    for ln in text.split("\n"):
        if re.match(r"^\s*[-*]\s+|^\s*\d+\.\s+", ln):
            buf.append(re.sub(r"^\s*[-*]\s+|^\s*\d+\.\s+", "", ln).strip().rstrip("。"))
        else:
            if buf:
                out.append("；".join(buf) + "。")
                buf = []
            out.append(ln)
    if buf:
        out.append("；".join(buf) + "。")
    return "\n".join(out)


def strip_md(t: str) -> str:
    for pat, rep in MARKDOWN_STRIP:
        t = re.sub(pat, rep, t)
    return t


def build_items(md_text: str):
    body = md_text.split("## 附：")[0]
    if "\n---\n" in body:  # 跳过文件头元信息块
        body = body.split("\n---\n", 1)[1]
    # 去掉组分隔线与组标题，只留 ### 问答
    body = "\n".join(
        l for l in body.split("\n")
        if not re.match(r"^\s*---\s*$", l) and not re.match(r"^## ", l)
    )
    items = []
    for block in re.split(r"\n### ", body)[1:]:
        ls = block.split("\n")
        question = ls[0].strip()
        rest = [l for l in ls[1:] if not l.strip().startswith(">")]
        text = strip_md(join_lists(table_to_text("\n".join(rest))))
        text = re.sub(r"\s{2,}", " ", re.sub(r"\n+", " ", text)).strip()
        text = text.rstrip("。") + "。"
        items.append({
            "@type": "Question",
            "name": question,
            "acceptedAnswer": {"@type": "Answer", "text": text},
        })
    return items


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    src = pathlib.Path(sys.argv[1])
    out = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix(".schema.json")

    items = build_items(src.read_text(encoding="utf-8"))
    schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items}
    out.write_text(json.dumps(schema, ensure_ascii=False, indent=2), encoding="utf-8")

    lens = [len(i["acceptedAnswer"]["text"]) for i in items]
    leaks = [i["name"] for i in items
             if any(w in i["acceptedAnswer"]["text"] for w in LEAK_WORDS)]
    print(f"✅ 生成 {out}｜问答 {len(items)} 条｜答案长度 min/max/avg = "
          f"{min(lens)}/{max(lens)}/{sum(lens)//len(lens)}")
    if leaks:
        print(f"⚠️  疑似内部信息泄漏（请人工复核）：{leaks}")
    else:
        print("✅ 内部信息检查通过")


if __name__ == "__main__":
    main()
