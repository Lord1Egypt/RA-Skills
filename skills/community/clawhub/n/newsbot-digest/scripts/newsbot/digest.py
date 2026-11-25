"""Финал: дайджест в Markdown/HTML + result.json со ссылками на PDF во внутренних папках агента."""
from __future__ import annotations

import html
import json
import os
import shutil

import pandas as pd

from .config import ctx
from .utils import get_date_ru

NUM = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]


def _clean(v) -> str:
    return "" if v is None or (isinstance(v, float) and pd.isna(v)) else str(v)


def build_digest() -> dict:
    c = ctx()
    df = pd.read_excel(c.selected_xlsx)
    shutil.copy(c.selected_xlsx, c.out_dir / "selected.xlsx")

    items = []
    for _, row in df.iterrows():
        pdf_abs = _clean(row.get("translation_pdf"))
        items.append({
            "title": _clean(row.get("RU_TITLE")) or _clean(row.get("description")),
            "type": _clean(row.get("type")),
            "source": _clean(row.get("source")),
            "original_url": _clean(row.get("url")),
            "translation_pdf": pdf_abs or None,
            "translation_pdf_rel": os.path.relpath(pdf_abs, c.out_dir) if pdf_abs else None,
        })

    header = f"Новости | {get_date_ru(c.now)}"

    # Markdown (ссылки на PDF — относительные, внутри папки результата)
    md = [f"# {header}", ""]
    for n, it in enumerate(items):
        md.append(f"{NUM[n] if n < len(NUM) else f'{n + 1}.'} {it['title']}")
        links = []
        if it["original_url"]:
            links.append(f"[🔗 Оригинал]({it['original_url']})")
        if it["translation_pdf_rel"]:
            links.append(f"[📄 Перевод]({it['translation_pdf_rel']})")
        if links:
            md.append(" | ".join(links))
        md.append("")
    c.digest_md.write_text("\n".join(md), encoding="utf-8")

    # HTML (тот же формат, что раньше уходил в Telegram, но ссылки — на локальные PDF)
    h = [f"<b>{html.escape(header)}</b><br><br>"]
    for n, it in enumerate(items):
        h.append(f"{NUM[n] if n < len(NUM) else n + 1}<br>{html.escape(it['title'])}<br>")
        links = []
        if it["original_url"]:
            links.append(f"<a href='{html.escape(it['original_url'])}'>🔗 Оригинал</a>")
        if it["translation_pdf_rel"]:
            links.append(f"<a href='{html.escape(it['translation_pdf_rel'])}'>📄 Перевод</a>")
        h.append(" | ".join(links) + "<br><br>")
    (c.out_dir / "digest.html").write_text(
        "<!doctype html><meta charset='utf-8'><title>Новости</title>"
        "<body style='font-family:sans-serif;max-width:760px;margin:24px auto;line-height:1.5'>"
        + "".join(h) + "</body>", encoding="utf-8")

    result = {
        "date": c.date,
        "header": header,
        "output_dir": str(c.out_dir.resolve()),
        "digest_md": str(c.digest_md.resolve()),
        "digest_html": str((c.out_dir / "digest.html").resolve()),
        "selected_xlsx": str((c.out_dir / "selected.xlsx").resolve()),
        "pdf_dir": str(c.pdf_dir.resolve()),
        "items": items,
    }
    c.result_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result
