#!/usr/bin/env python3
"""
Детерминированный рендер аналитической записки: analysis.json -> .docx (≤ 2 страниц A4).
Без python-docx: файл Word собирается напрямую из XML (Office Open XML), поэтому нужен только
стандартный Python (+ Pillow для оценки вёрстки). Один и тот же JSON → побайтно один и тот же .docx.

Модель (Claude или локальная LLM) отвечает только за СОДЕРЖАНИЕ в analysis.json.
Оформление — шрифты, нумерация, таблицы «Логики решения», колонтитулы — задаёт этот скрипт.

Структура документа (фиксированная):
    [шапка: тип документа, заголовок, дата, источники, фокус]
    1. Общий вывод
    2. {Топик 1}  2.1. Сводка  2.2. Логика решения
    3. {Топик 2}  3.1. Сводка  3.2. Логика решения
    4. {Топик 3}  4.1. Сводка  4.2. Логика решения
    [Источники: D1 — файл; D2 — …]

Контроль «≤ 2 страниц» (--page-check auto): LibreOffice (если установлен) → Microsoft Word через
pywin32 (Windows) → собственная оценка вёрстки по метрикам шрифта Arial (работает всегда).

Использование:
    python build_docx.py analysis.json --out brief.docx [--manifest work/manifest.json]
                         [--max-pages 2] [--pdf] [--page-check auto|libreoffice|word|estimate]
    python build_docx.py analysis.json --check         # только валидация, без рендера

Коды выхода: 0 — ок; 2 — ошибки валидации JSON; 3 — не помещается в --max-pages.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path

try:  # пакет docbrief
    from . import layout as L
    from . import pdf as pdfmod
    from . import schema as S
except ImportError:  # скрипт рядом с layout.py, pdf.py и schema.py (скилл)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import layout as L
    import pdf as pdfmod
    import schema as S

# ------------------------------------------------------------------------- контракт
LIMITS = {
    "title": 110,
    "focus": 220,
    "overall.text": 800,
    "overall.key_point": 170,
    "overall.key_points_max": 3,
    "topic.title": 90,
    "topic.summary": 600,
    "evidence.item": 200,
    "evidence.total": 560,
    "reasoning.step": 200,
    "reasoning.total": 520,
    "conclusion": 240,
    "confidence_reason": 150,
    "caveats": 170,
    "topics_min": 2,
    "topics_max": 4,
    "items_min": 2,
    "items_max": 4,
}
CONFIDENCE = {"высокая": "2E7D32", "средняя": "B26A00", "низкая": "C62828"}
REF_RE = re.compile(r"^(D\d+)\b")

# ------------------------------------------------------------------------- оформление
FONT = "Arial"
NAVY = "1F3864"
ACCENT = "2E75B6"
GRAY = "595959"
LIGHT = "8C8C8C"
INK = "1A1A1A"
BODY = "222222"
BOX_FILL = "EEF3F8"
LABEL_FILL = "F2F4F7"
RULE = "BFC9D6"
LABEL_W = 3.1  # cm — колонка подписей в таблице «Логика решения»

PROFILES = [  # от просторного к плотному; берётся первый, что влезает в лимит страниц
    {"name": "standard", "body": 10.0, "small": 9.0, "h1": 12.0, "h2": 10.0, "title": 16.0,
     "line": 1.10, "after": 3, "h1_before": 9, "margins": (1.8, 1.6, 2.0, 1.8)},
    {"name": "compact", "body": 9.5, "small": 8.5, "h1": 11.5, "h2": 9.5, "title": 15.0,
     "line": 1.05, "after": 2, "h1_before": 7, "margins": (1.5, 1.4, 1.8, 1.6)},
    {"name": "dense", "body": 9.0, "small": 8.0, "h1": 11.0, "h2": 9.0, "title": 14.0,
     "line": 1.0, "after": 1, "h1_before": 5, "margins": (1.3, 1.2, 1.6, 1.4)},
]


# =========================================================================== валидация
def _s(v) -> str:
    return v.strip() if isinstance(v, str) else ""


UNIT_RE = re.compile(r"(стр\.|слайд)\s*(\d+)")
MENTION_RE = re.compile(r"(?<![A-Za-z0-9])D(\d+)(?![0-9])")


def validate(data: dict, known_ids: set[str] | None = None,
             doc_units: dict[str, tuple[str, int]] | None = None) -> list[str]:
    """Возвращает список ошибок на русском — их можно отдать модели на исправление.
    known_ids — допустимые ID документов; doc_units — {ID: (тип, число страниц/слайдов)}
    для проверки номеров страниц в ссылках.
    Перед проверкой ответ приводится к схеме (schema.normalize_analysis): строки вместо объектов,
    ссылки внутри текста, «Высокая (…)» и т.п. ошибками не считаются — это переупаковка.
    """
    E: list[str] = []
    if not isinstance(data, dict):
        return ["корень JSON должен быть объектом"]
    data = S.normalize_analysis(data)

    def need(path, val, limit_key=None, required=True):
        s = _s(val)
        if required and not s:
            E.append(f"{path}: пусто или не строка")
        if limit_key and len(s) > LIMITS[limit_key]:
            E.append(f"{path}: {len(s)} симв. > лимита {LIMITS[limit_key]} — сократите")
        return s

    if not isinstance(data, dict):
        return ["корень JSON должен быть объектом"]
    meta = data.get("meta") or {}
    need("meta.title", meta.get("title"), "title")
    need("meta.focus", meta.get("focus"), "focus", required=False)
    if meta.get("date") and not re.match(r"^\d{4}-\d{2}-\d{2}$", str(meta["date"])):
        E.append("meta.date: формат YYYY-MM-DD")

    ov = data.get("overall") or {}
    need("overall.text", ov.get("text"), "overall.text")
    kps = ov.get("key_points") or []
    if not isinstance(kps, list):
        E.append("overall.key_points: должен быть списком строк")
        kps = []
    if len(kps) > LIMITS["overall.key_points_max"]:
        E.append(f"overall.key_points: не более {LIMITS['overall.key_points_max']} пунктов")
    for i, kp in enumerate(kps):
        need(f"overall.key_points[{i}]", kp, "overall.key_point")

    topics = data.get("topics")
    if not isinstance(topics, list):
        return E + ["topics: должен быть списком"]
    if not LIMITS["topics_min"] <= len(topics) <= LIMITS["topics_max"]:
        E.append(f"topics: {len(topics)} шт., допустимо {LIMITS['topics_min']}–{LIMITS['topics_max']} (по умолчанию 3)")
    titles = set()
    for t_i, t in enumerate(topics):
        p = f"topics[{t_i}]"
        if not isinstance(t, dict):
            E.append(f"{p}: должен быть объектом")
            continue
        title = need(f"{p}.title", t.get("title"), "topic.title")
        if title.lower() in titles:
            E.append(f"{p}.title: дублирует другой топик")
        titles.add(title.lower())
        need(f"{p}.summary", t.get("summary"), "topic.summary")
        lg = t.get("logic") or {}
        ev = lg.get("evidence") or []
        if not (LIMITS["items_min"] <= len(ev) <= LIMITS["items_max"]):
            E.append(f"{p}.logic.evidence: {len(ev)} шт., нужно {LIMITS['items_min']}–{LIMITS['items_max']}")
        total = 0
        for e_i, e in enumerate(ev):
            ep = f"{p}.logic.evidence[{e_i}]"
            if not isinstance(e, dict):
                E.append(f"{ep}: должен быть объектом {{text, refs}}")
                continue
            total += len(need(f"{ep}.text", e.get("text"), "evidence.item"))
            refs = e.get("refs") or []
            if not refs or not isinstance(refs, list):
                E.append(f"{ep}.refs: укажите хотя бы одну ссылку на источник (напр. \"D2 · стр. 4\")")
            for r in refs if isinstance(refs, list) else []:
                m = REF_RE.match(_s(r))
                if not m:
                    E.append(f"{ep}.refs: «{r}» — ссылка должна начинаться с ID документа (D1, D2 …)")
                elif known_ids is not None and m.group(1) not in known_ids:
                    E.append(f"{ep}.refs: документа {m.group(1)} нет среди источников")
                elif doc_units and m.group(1) in doc_units:
                    dtype, n = doc_units[m.group(1)]
                    u = UNIT_RE.search(_s(r))
                    if u and dtype in ("PDF", "PPTX") and int(u.group(2)) > n:
                        E.append(f"{ep}.refs: «{r}» — в {m.group(1)} всего {n} "
                                 f"{'стр.' if dtype == 'PDF' else 'слайдов'}")
        if total > LIMITS["evidence.total"]:
            E.append(f"{p}.logic.evidence: суммарно {total} симв. > {LIMITS['evidence.total']}")
        rs = lg.get("reasoning") or []
        if not (LIMITS["items_min"] <= len(rs) <= LIMITS["items_max"]):
            E.append(f"{p}.logic.reasoning: {len(rs)} шагов, нужно {LIMITS['items_min']}–{LIMITS['items_max']}")
        total = sum(len(need(f"{p}.logic.reasoning[{i}]", s, "reasoning.step")) for i, s in enumerate(rs))
        if total > LIMITS["reasoning.total"]:
            E.append(f"{p}.logic.reasoning: суммарно {total} симв. > {LIMITS['reasoning.total']}")
        need(f"{p}.logic.conclusion", lg.get("conclusion"), "conclusion")
        conf = _s(lg.get("confidence")).lower()
        if conf not in CONFIDENCE:
            E.append(f"{p}.logic.confidence: одно из {list(CONFIDENCE)}")
        need(f"{p}.logic.confidence_reason", lg.get("confidence_reason"), "confidence_reason")
        need(f"{p}.logic.caveats", lg.get("caveats"), "caveats", required=False)

    if known_ids is not None:  # упоминания документов в свободном тексте тоже должны существовать
        for path, text in iter_texts(data):
            for m in MENTION_RE.finditer(text):
                if f"D{m.group(1)}" not in known_ids:
                    E.append(f"{path}: упомянут D{m.group(1)}, которого нет среди источников")

    for s_i, s in enumerate(data.get("sources") or []):
        if not isinstance(s, dict) or not _s(s.get("id")) or not _s(s.get("name")):
            E.append(f"sources[{s_i}]: нужен объект {{id, name, note?}}")
    return E


def iter_texts(data: dict):
    data = S.normalize_analysis(data)
    ov = data.get("overall") or {}
    yield "overall.text", _s(ov.get("text"))
    for i, k in enumerate(ov.get("key_points") or []):
        yield f"overall.key_points[{i}]", _s(k)
    for t_i, t in enumerate(data.get("topics") or []):
        if not isinstance(t, dict):
            continue
        p = f"topics[{t_i}]"
        yield f"{p}.summary", _s(t.get("summary"))
        lg = t.get("logic") or {}
        for e_i, e in enumerate(lg.get("evidence") or []):
            if isinstance(e, dict):
                yield f"{p}.logic.evidence[{e_i}].text", _s(e.get("text"))
        for r_i, r in enumerate(lg.get("reasoning") or []):
            yield f"{p}.logic.reasoning[{r_i}]", _s(r)
        for k in ("conclusion", "confidence_reason", "caveats"):
            yield f"{p}.logic.{k}", _s(lg.get(k))


def fill_report(data: dict) -> str:
    """Заполненность относительно лимитов — ориентир «≈80%» для автора."""
    def pct(n, lim):
        return f"{round(100 * n / lim)}%"
    data = S.normalize_analysis(data)
    ov = data.get("overall") or {}
    lines = [f"overall.text {pct(len(_s(ov.get('text'))), LIMITS['overall.text'])}"]
    for i, t in enumerate(data.get("topics") or []):
        lg = t.get("logic") or {}
        ev = sum(len(_s(e.get("text"))) for e in lg.get("evidence") or [] if isinstance(e, dict))
        rs = sum(len(_s(r)) for r in lg.get("reasoning") or [])
        lines.append(f"topics[{i}]: summary {pct(len(_s(t.get('summary'))), LIMITS['topic.summary'])}, "
                     f"evidence {pct(ev, LIMITS['evidence.total'])}, reasoning {pct(rs, LIMITS['reasoning.total'])}")
    return "Заполненность лимитов: " + "; ".join(lines)


def plural(n: int, one: str, few: str, many: str) -> str:
    if n % 10 == 1 and n % 100 != 11:
        return one
    return few if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14 else many


def sources_from_manifest(manifest: dict) -> list[dict]:
    units = {"PDF": ("стр.", "стр.", "стр."), "PPTX": ("слайд", "слайда", "слайдов"),
             "XLSX": ("лист", "листа", "листов")}
    out = []
    for d in manifest.get("documents", []):
        note = d["type"]
        if d["type"] in units:
            note += f", {d['units']} {plural(int(d['units']), *units[d['type']])}"
        out.append({"id": d["id"], "name": d["name"], "note": note})
    return out



def fmt_date(iso: str) -> str:
    try:
        return datetime.strptime(iso, "%Y-%m-%d").strftime("%d.%m.%Y")
    except Exception:
        return iso


def fmt_ref(r: str) -> str:
    r = _s(r).replace(" · ", ", ")
    return r


def type_summary(sources: list[dict]) -> str:
    counts: dict[str, int] = {}
    for s in sources:
        t = (s.get("note") or "").split(",")[0].strip().upper()
        if t:
            counts[t] = counts.get(t, 0) + 1
    return ", ".join(f"{n} {t}" for t, n in sorted(counts.items(), key=lambda x: (-x[1], x[0])))



# ============================================================================ модель записки
Run, Para, Cell, Table, DocModel = L.Run, L.Para, L.Cell, L.Table, L.DocModel


def build_model(data: dict, P: dict) -> DocModel:
    meta, ov, topics = data.get("meta", {}), data.get("overall", {}), data.get("topics", [])
    sources = data.get("sources") or []
    top, bottom, left, right = P["margins"]
    text_w = 21.0 - left - right
    blocks: list = []

    def h1(text):
        blocks.append(Para([Run(text, P["h1"], bold=True, color=NAVY)], before=P["h1_before"], after=3,
                           line=1.0, keep_next=True, style="Heading1"))

    def h2(text):
        blocks.append(Para([Run(text, P["h2"], bold=True, color=ACCENT)], before=4, after=2, line=1.0,
                           keep_next=True, style="Heading2"))

    # ---------- шапка
    blocks.append(Para([Run((meta.get("doc_type") or "Аналитическая записка").upper(), P["small"], bold=True,
                            color=ACCENT, spacing=1.0)], after=1, line=1.0))
    blocks.append(Para([Run(_s(meta.get("title")), P["title"], bold=True, color=NAVY)], after=3, line=1.0))
    src_bit = (f"Источники: {len(sources)}" + (f" ({type_summary(sources)})" if sources else "")) if sources else ""
    bits = [b for b in (fmt_date(meta.get("date") or ""), src_bit, _s(meta.get("prepared_for"))) if b]
    blocks.append(Para([Run("  ·  ".join(bits), P["small"], color=GRAY)], after=2 if _s(meta.get("focus")) else 0,
                       line=1.0))
    if _s(meta.get("focus")):
        blocks.append(Para([Run("Фокус анализа: ", P["small"], bold=True, color=GRAY),
                            Run(_s(meta["focus"]), P["small"], color=GRAY)], line=1.0))
    blocks[-1].border_bottom = (8, ACCENT, 4)

    # ---------- 1. Общий вывод
    h1("1. Общий вывод")
    kps = ov.get("key_points") or []
    box = [Para([Run(_s(ov.get("text")), P["body"], color=INK)], after=2 if kps else 0, line=P["line"],
                align="both")]
    for kp in kps:
        box.append(Para([Run("\u25aa\u2002", P["body"], bold=True, color=ACCENT), Run(_s(kp), P["body"], color=INK)],
                        line=P["line"], ind_left=0.45, first_line=-0.35))
    blocks.append(Table([[Cell(box, fill=BOX_FILL, borders={"left": (24, ACCENT)})]], [text_w],
                        margins=(70, 70, 140, 120)))

    # ---------- топики
    fs = P["small"] + 0.5
    for i, t in enumerate(topics, start=2):
        h1(f"{i}. {_s(t.get('title'))}")
        h2(f"{i}.1. Сводка")
        blocks.append(Para([Run(_s(t.get("summary")), P["body"])], after=P["after"] + 1, line=P["line"],
                           align="both"))
        h2(f"{i}.2. Логика решения")
        lg = t.get("logic", {})
        spec = [("Исходные факты", "evidence"), ("Ход рассуждения", "reasoning"), ("Вывод", "conclusion"),
                ("Уверенность", "confidence")]
        if _s(lg.get("caveats")):
            spec.append(("Оговорки", "caveats"))
        rows = []
        for r_i, (label, key) in enumerate(spec):
            edge = (6, ACCENT) if r_i == 0 else (4, RULE)
            borders = {"top": edge}
            if r_i == len(spec) - 1:
                borders["bottom"] = (6, ACCENT)
            paras: list = []
            if key == "evidence":
                for e in lg.get("evidence") or []:
                    runs = [Run("\u2022\u2002", fs, color=ACCENT), Run(_s(e.get("text")), fs)]
                    refs = "; ".join(fmt_ref(x) for x in e.get("refs") or [])
                    if refs:
                        runs.append(Run(f"  [{refs}]", P["small"] - 0.5, color=LIGHT))
                    paras.append(Para(runs, after=1, line=P["line"], ind_left=0.35, first_line=-0.3))
            elif key == "reasoning":
                for s_i, s in enumerate(lg.get("reasoning") or []):
                    paras.append(Para([Run(f"{s_i + 1}.\u2002", fs, bold=True, color=ACCENT), Run(_s(s), fs)],
                                      after=1, line=P["line"], ind_left=0.4, first_line=-0.4))
            elif key == "conclusion":
                paras.append(Para([Run(_s(lg.get("conclusion")), fs, bold=True, color=INK)], line=P["line"]))
            elif key == "confidence":
                conf = _s(lg.get("confidence")).lower()
                runs = [Run(conf.capitalize(), fs, bold=True, color=CONFIDENCE.get(conf, GRAY))]
                if _s(lg.get("confidence_reason")):
                    runs.append(Run(" — " + _s(lg["confidence_reason"]), fs, color=GRAY))
                paras.append(Para(runs, line=P["line"]))
            else:
                paras.append(Para([Run(_s(lg.get("caveats")), fs, italic=True, color=GRAY)], line=P["line"]))
            rows.append([Cell([Para([Run(label, P["small"], bold=True, color=NAVY)], line=1.0)], fill=LABEL_FILL,
                              borders=dict(borders)),
                         Cell(paras or [Para([Run("", fs)])], borders=dict(borders))])
        blocks.append(Table(rows, [LABEL_W, text_w - LABEL_W], margins=(35, 35, 90, 90)))

    # ---------- источники
    if sources:
        items = []
        for s in sources:
            note = f" ({_s(s.get('note'))})" if _s(s.get("note")) else ""
            items.append(f"{_s(s.get('id'))} — {_s(s.get('name'))}{note}")
        blocks.append(Para([Run("Источники: ", P["small"] - 0.5, bold=True, color=GRAY),
                            Run("; ".join(items) + ".", P["small"] - 0.5, color=GRAY)],
                           before=8, line=1.0, border_top=(4, RULE, 3)))

    footer = Para([Run(meta.get("footer_note") or "Подготовлено с использованием ИИ на основе предоставленных "
                       "материалов. Выводы требуют проверки по первоисточникам.", 7, color=LIGHT),
                   Run("\tстр. ", 7, color=LIGHT), Run("{PAGE}", 7, color=LIGHT), Run(" из ", 7, color=LIGHT),
                   Run("{NUMPAGES}", 7, color=LIGHT)], line=1.0, style="Footer", tab_right=text_w)
    return DocModel(blocks, P["margins"], footer=footer, meta=meta, profile=P)


# ============================================================================ запись OOXML
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
_BAD_XML = re.compile("[\x00-\x08\x0b\x0c\x0e-\x1f\ud800-\udfff\ufffe\uffff]")


def _esc(t: str) -> str:
    t = _BAD_XML.sub("", t)
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _tw(cm: float) -> int:
    return int(round(cm * 567))


def _rpr(r: Run) -> str:
    hp = int(round(r.size * 2))
    out = f'<w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:eastAsia="{FONT}" w:cs="{FONT}"/>'
    if r.bold:
        out += "<w:b/><w:bCs/>"
    if r.italic:
        out += "<w:i/><w:iCs/>"
    if r.color:
        out += f'<w:color w:val="{r.color}"/>'
    if r.spacing:
        out += f'<w:spacing w:val="{int(round(r.spacing * 20))}"/>'
    out += f'<w:sz w:val="{hp}"/><w:szCs w:val="{hp}"/>'
    return f"<w:rPr>{out}</w:rPr>"


def _run(r: Run) -> str:
    rpr = _rpr(r)
    if r.text in ("{PAGE}", "{NUMPAGES}"):  # поле Word: номер страницы / число страниц
        instr = r.text.strip("{}")
        return (f'<w:r>{rpr}<w:fldChar w:fldCharType="begin"/></w:r>'
                f'<w:r>{rpr}<w:instrText xml:space="preserve"> {instr} </w:instrText></w:r>'
                f'<w:r>{rpr}<w:fldChar w:fldCharType="separate"/></w:r>'
                f'<w:r>{rpr}<w:t>1</w:t></w:r>'
                f'<w:r>{rpr}<w:fldChar w:fldCharType="end"/></w:r>')
    body = []
    for piece in re.split(r"(\t|\n)", r.text):
        if piece == "\t":
            body.append("<w:tab/>")
        elif piece == "\n":
            body.append("<w:br/>")
        elif piece:
            body.append(f'<w:t xml:space="preserve">{_esc(piece)}</w:t>')
    return f"<w:r>{rpr}{''.join(body)}</w:r>"


def _bdr(side: str, spec: tuple) -> str:
    sz, color, space = spec
    return f'<w:{side} w:val="single" w:sz="{sz}" w:space="{int(space)}" w:color="{color}"/>'


def _para(p: Para) -> str:
    ppr = ""
    if p.style:
        ppr += f'<w:pStyle w:val="{p.style}"/>'
    if p.keep_next:
        ppr += "<w:keepNext/>"
    if p.border_top or p.border_bottom:
        ppr += "<w:pBdr>" + (_bdr("top", p.border_top) if p.border_top else "") + \
               (_bdr("bottom", p.border_bottom) if p.border_bottom else "") + "</w:pBdr>"
    if p.tab_right is not None:
        ppr += f'<w:tabs><w:tab w:val="right" w:pos="{_tw(p.tab_right)}"/></w:tabs>'
    ppr += (f'<w:spacing w:before="{int(round(p.before * 20))}" w:after="{int(round(p.after * 20))}" '
            f'w:line="{int(round(p.line * 240))}" w:lineRule="auto"/>')
    if p.ind_left or p.first_line:
        ind = f'w:left="{_tw(p.ind_left)}"'
        if p.first_line < 0:
            ind += f' w:hanging="{_tw(-p.first_line)}"'
        elif p.first_line > 0:
            ind += f' w:firstLine="{_tw(p.first_line)}"'
        ppr += f"<w:ind {ind}/>"
    if p.align:
        ppr += f'<w:jc w:val="{p.align}"/>'
    return f"<w:p><w:pPr>{ppr}</w:pPr>{''.join(_run(r) for r in p.runs)}</w:p>"


def _table(t: Table) -> str:
    widths = [_tw(w) for w in t.widths]
    top, bottom, left, right = t.margins
    nil = "".join(f'<w:{s} w:val="nil"/>' for s in ("top", "left", "bottom", "right", "insideH", "insideV"))
    out = [f'<w:tbl><w:tblPr><w:tblW w:w="{sum(widths)}" w:type="dxa"/><w:jc w:val="center"/>'
           f'<w:tblBorders>{nil}</w:tblBorders><w:tblLayout w:type="fixed"/>'
           f'<w:tblCellMar><w:top w:w="{top}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/>'
           f'<w:bottom w:w="{bottom}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tblCellMar>'
           f'<w:tblLook w:val="0000" w:firstRow="0" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" '
           f'w:noHBand="1" w:noVBand="1"/></w:tblPr>',
           "<w:tblGrid>" + "".join(f'<w:gridCol w:w="{w}"/>' for w in widths) + "</w:tblGrid>"]
    for row in t.rows:
        out.append("<w:tr>" + ("<w:trPr><w:cantSplit/></w:trPr>" if t.cant_split else ""))
        for cell, w in zip(row, widths):
            b = ""
            for side in ("top", "left", "bottom", "right"):
                spec = cell.borders.get(side)
                b += (f'<w:{side} w:val="single" w:sz="{spec[0]}" w:space="0" w:color="{spec[1]}"/>' if spec
                      else f'<w:{side} w:val="nil"/>')
            shd = f'<w:shd w:val="clear" w:color="auto" w:fill="{cell.fill}"/>' if cell.fill else ""
            out.append(f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/><w:tcBorders>{b}</w:tcBorders>{shd}</w:tcPr>'
                       + "".join(_para(p) for p in cell.paras) + "</w:tc>")
        out.append("</w:tr>")
    out.append("</w:tbl>")
    return "".join(out)


def _styles(P: dict, text_w: float) -> str:
    def sz(v):
        return int(round(v * 2))
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            f'<w:styles xmlns:w="{W_NS}">'
            f'<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="{FONT}" w:eastAsia="{FONT}" w:hAnsi="{FONT}" '
            f'w:cs="{FONT}"/><w:sz w:val="{sz(P["body"])}"/><w:szCs w:val="{sz(P["body"])}"/>'
            f'<w:lang w:val="ru-RU" w:eastAsia="ru-RU" w:bidi="ar-SA"/></w:rPr></w:rPrDefault>'
            f'<w:pPrDefault><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr></w:pPrDefault>'
            f'</w:docDefaults>'
            f'<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/>'
            f'<w:pPr><w:widowControl/><w:spacing w:after="{P["after"] * 20}" w:line="{int(P["line"] * 240)}" '
            f'w:lineRule="auto"/></w:pPr><w:rPr><w:color w:val="{BODY}"/><w:sz w:val="{sz(P["body"])}"/>'
            f'<w:szCs w:val="{sz(P["body"])}"/></w:rPr></w:style>'
            f'<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>'
            f'<w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:qFormat/><w:pPr><w:keepNext/>'
            f'<w:spacing w:before="{P["h1_before"] * 20}" w:after="60" w:line="240" w:lineRule="auto"/>'
            f'<w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:bCs/><w:color w:val="{NAVY}"/>'
            f'<w:sz w:val="{sz(P["h1"])}"/><w:szCs w:val="{sz(P["h1"])}"/></w:rPr></w:style>'
            f'<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>'
            f'<w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:unhideWhenUsed/><w:qFormat/><w:pPr><w:keepNext/>'
            f'<w:spacing w:before="80" w:after="40" w:line="240" w:lineRule="auto"/><w:outlineLvl w:val="1"/></w:pPr>'
            f'<w:rPr><w:b/><w:bCs/><w:color w:val="{ACCENT}"/><w:sz w:val="{sz(P["h2"])}"/>'
            f'<w:szCs w:val="{sz(P["h2"])}"/></w:rPr></w:style>'
            f'<w:style w:type="paragraph" w:styleId="Footer"><w:name w:val="footer"/><w:basedOn w:val="Normal"/>'
            f'<w:uiPriority w:val="99"/><w:unhideWhenUsed/><w:pPr><w:tabs><w:tab w:val="right" '
            f'w:pos="{_tw(text_w)}"/></w:tabs><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>'
            f'<w:rPr><w:color w:val="{LIGHT}"/><w:sz w:val="14"/><w:szCs w:val="14"/></w:rPr></w:style>'
            f'<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/>'
            f'<w:uiPriority w:val="99"/><w:semiHidden/><w:unhideWhenUsed/><w:tblPr><w:tblInd w:w="0" w:type="dxa"/>'
            f'<w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="108" w:type="dxa"/>'
            f'<w:bottom w:w="0" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>'
            f'</w:styles>')


def to_docx(model: DocModel) -> bytes:
    P = model.profile
    top, bottom, left, right = model.margins
    body = "".join(_table(b) if isinstance(b, Table) else _para(b) for b in model.blocks)
    sect = (f'<w:sectPr><w:footerReference w:type="default" r:id="rId3"/>'
            f'<w:pgSz w:w="{_tw(model.page[0])}" w:h="{_tw(model.page[1])}"/>'
            f'<w:pgMar w:top="{_tw(top)}" w:right="{_tw(right)}" w:bottom="{_tw(bottom)}" w:left="{_tw(left)}" '
            f'w:header="{_tw(model.header_dist)}" w:footer="{_tw(model.footer_dist)}" w:gutter="0"/>'
            f'<w:cols w:space="708"/><w:docGrid w:linePitch="360"/></w:sectPr>')
    document = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                f'<w:document xmlns:w="{W_NS}" xmlns:r="{R_NS}"><w:body>{body}{sect}</w:body></w:document>')
    footer = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
              f'<w:ftr xmlns:w="{W_NS}" xmlns:r="{R_NS}">{_para(model.footer)}</w:ftr>')
    settings = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                f'<w:settings xmlns:w="{W_NS}"><w:zoom w:percent="100"/><w:defaultTabStop w:val="708"/>'
                f'<w:autoHyphenation/><w:characterSpacingControl w:val="doNotCompress"/>'
                f'<w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" '
                f'w:val="15"/></w:compat><w:decimalSymbol w:val=","/><w:listSeparator w:val=";"/></w:settings>')
    meta = model.meta
    date = meta.get("date") if re.match(r"^\d{4}-\d{2}-\d{2}$", str(meta.get("date") or "")) else "2000-01-01"
    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f'<dc:title>{_esc(_s(meta.get("title")))}</dc:title><dc:subject>{_esc(_s(meta.get("focus")))}</dc:subject>'
            '<dc:creator>multi-doc-brief</dc:creator><cp:lastModifiedBy>multi-doc-brief</cp:lastModifiedBy>'
            '<cp:revision>1</cp:revision>'
            f'<dcterms:created xsi:type="dcterms:W3CDTF">{date}T00:00:00Z</dcterms:created>'
            f'<dcterms:modified xsi:type="dcterms:W3CDTF">{date}T00:00:00Z</dcterms:modified></cp:coreProperties>')
    app = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
           '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
           'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
           '<Application>multi-doc-brief</Application><DocSecurity>0</DocSecurity></Properties>')
    ctypes = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
              '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
              '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
              '<Default Extension="xml" ContentType="application/xml"/>'
              '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.'
              'wordprocessingml.document.main+xml"/>'
              '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.'
              'wordprocessingml.styles+xml"/>'
              '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.'
              'wordprocessingml.settings+xml"/>'
              '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.'
              'wordprocessingml.footer+xml"/>'
              '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.'
              'core-properties+xml"/>'
              '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.'
              'extended-properties+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/'
            'officeDocument" Target="word/document.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/'
            'core-properties" Target="docProps/core.xml"/>'
            '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/'
            'extended-properties" Target="docProps/app.xml"/></Relationships>')
    doc_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/'
                'styles" Target="styles.xml"/>'
                '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/'
                'settings" Target="settings.xml"/>'
                '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/'
                'footer" Target="footer1.xml"/></Relationships>')
    parts = [("[Content_Types].xml", ctypes), ("_rels/.rels", rels), ("docProps/app.xml", app),
             ("docProps/core.xml", core), ("word/_rels/document.xml.rels", doc_rels),
             ("word/document.xml", document), ("word/footer1.xml", footer), ("word/settings.xml", settings),
             ("word/styles.xml", _styles(P, model.text_width))]
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, text in parts:  # фиксированные порядок и время записей => одинаковые байты
            zi = zipfile.ZipInfo(name, date_time=(2000, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, text.encode("utf-8"))
    return buf.getvalue()


def render(data: dict, P: dict) -> bytes:
    """analysis.json + профиль → байты .docx."""
    return to_docx(build_model(data, P))


# ============================================================================ контроль страниц
def find_soffice() -> str | None:
    """LibreOffice: переменная SOFFICE_PATH → PATH → типовые пути Windows/macOS."""
    if os.environ.get("DOCBRIEF_NO_SOFFICE"):
        return None
    env = os.environ.get("SOFFICE_PATH")
    if env and Path(env).exists():
        return env
    found = shutil.which("soffice") or shutil.which("libreoffice")
    if found:
        return found
    for cand in (r"C:\Program Files\LibreOffice\program\soffice.exe",
                 r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
                 "/Applications/LibreOffice.app/Contents/MacOS/soffice"):
        if Path(cand).exists():
            return cand
    return None


def to_pdf(docx_bytes: bytes, workdir: Path) -> Path | None:
    exe = find_soffice()
    if not exe:
        return None
    src = workdir / "probe.docx"
    src.write_bytes(docx_bytes)
    try:
        # отдельный профиль LibreOffice: конвертация работает, даже если у пользователя открыт LibreOffice
        profile = Path(tempfile.gettempdir()) / "mdb_lo_profile"
        subprocess.run([exe, f"-env:UserInstallation={profile.as_uri()}", "--headless", "--convert-to", "pdf",
                        "--outdir", str(workdir), str(src)], check=True, capture_output=True, timeout=180)
    except Exception:  # noqa: BLE001
        return None
    pdf = workdir / "probe.pdf"
    return pdf if pdf.exists() else None


_WORD_OK: bool | None = None
_WORD_SCRIPT = r"""
import sys, pythoncom, win32com.client
src, pdf = sys.argv[1], sys.argv[2]
pythoncom.CoInitialize()
word = win32com.client.DispatchEx("Word.Application")
try:
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(src, False, True, False)  # ConfirmConversions, ReadOnly, AddToRecentFiles
    doc.Repaginate()
    print("PAGES", int(doc.ComputeStatistics(2)))  # wdStatisticPages
    try:
        doc.ExportAsFixedFormat(pdf, 17)  # wdExportFormatPDF
    except Exception:
        pass
    doc.Close(False)
finally:
    word.Quit()
"""


def word_pages(docx_bytes: bytes, workdir: Path) -> tuple[int | None, bytes | None]:
    """Microsoft Word через COM (Windows + pywin32): точное число страниц и PDF-превью.
    Запускается отдельным процессом с тайм-аутом: если Word покажет диалог (активация, восстановление
    документа), ноутбук не зависнет — проверка перейдёт на оценку вёрстки.
    """
    global _WORD_OK
    if _WORD_OK is False or sys.platform != "win32" or os.environ.get("DOCBRIEF_NO_WORD"):
        return None, None
    try:
        import win32com.client  # noqa: F401  — pywin32 есть?
    except Exception:  # noqa: BLE001
        _WORD_OK = False
        return None, None
    src = (workdir / "probe_word.docx").resolve()
    pdf_path = src.with_suffix(".pdf")
    src.write_bytes(docx_bytes)
    try:
        r = subprocess.run([sys.executable, "-c", _WORD_SCRIPT, str(src), str(pdf_path)], capture_output=True,
                           text=True, timeout=int(os.environ.get("DOCBRIEF_WORD_TIMEOUT", "120")))
        m = re.search(r"PAGES (\d+)", r.stdout or "")
        if not m:
            _WORD_OK = False
            return None, None
        _WORD_OK = True
        return int(m.group(1)), (pdf_path.read_bytes() if pdf_path.exists() else None)
    except Exception:  # noqa: BLE001  — тайм-аут / Word не установлен
        _WORD_OK = False
        return None, None


def count_pages(pdf: Path) -> int:
    return pdfmod.count_pages(pdf)


def check_pages(docx_bytes: bytes, model: DocModel, max_pages: int, method: str = "auto") -> dict:
    """→ {"pages", "method", "ok", "pdf" (bytes|None), "estimate"}"""
    est_ok, est = L.fits(model, max_pages)
    res = {"pages": est["pages"], "method": "оценка", "ok": est_ok, "pdf": None, "estimate": est}
    if method in ("auto", "libreoffice") and find_soffice():
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:
            pdf = to_pdf(docx_bytes, Path(td))
            if pdf is not None:
                n = count_pages(pdf)
                return {**res, "pages": n, "method": "LibreOffice", "ok": n <= max_pages, "pdf": pdf.read_bytes()}
    if method in ("auto", "word"):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:
            n, pdf_bytes = word_pages(docx_bytes, Path(td))
            if n is not None:
                return {**res, "pages": n, "method": "Microsoft Word", "ok": n <= max_pages, "pdf": pdf_bytes}
    return res


def build(data: dict, max_pages: int = 2, method: str = "auto") -> dict:
    """Перебирает профили от просторного к плотному. → {"docx", "pages", "profile", "method", "ok", "pdf", ...}"""
    method = os.environ.get("DOCBRIEF_PAGE_CHECK", method)
    data = S.normalize_analysis(data)
    res = None
    for P in PROFILES:
        model = build_model(data, P)
        blob = to_docx(model)
        res = {**check_pages(blob, model, max_pages, method), "docx": blob, "profile": P["name"]}
        if res["ok"]:
            break
    return res


def text_volume(data: dict) -> int:
    data = S.normalize_analysis(data)
    n = len(_s(data.get("overall", {}).get("text"))) + sum(len(_s(k)) for k in data.get("overall", {}).get("key_points") or [])
    for t in data.get("topics", []):
        lg = t.get("logic", {})
        n += len(_s(t.get("summary"))) + sum(len(_s(e.get("text"))) for e in lg.get("evidence") or [])
        n += sum(len(_s(s)) for s in lg.get("reasoning") or []) + len(_s(lg.get("conclusion")))
        n += len(_s(lg.get("confidence_reason"))) + len(_s(lg.get("caveats")))
    return n


def longest_fields(data: dict, k=4) -> list[str]:
    data = S.normalize_analysis(data)
    items = []
    for i, t in enumerate(data.get("topics", [])):
        items.append((len(_s(t.get("summary"))), f"topics[{i}].summary"))
        lg = t.get("logic", {})
        items.append((sum(len(_s(e.get("text"))) for e in lg.get("evidence") or []), f"topics[{i}].logic.evidence"))
        items.append((sum(len(_s(s)) for s in lg.get("reasoning") or []), f"topics[{i}].logic.reasoning"))
    items.append((len(_s(data.get("overall", {}).get("text"))), "overall.text"))
    return [f"{name} ({n} симв.)" for n, name in sorted(items, reverse=True)[:k]]



# ============================================================================== main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("analysis", help="analysis.json")
    ap.add_argument("--out", default="brief.docx")
    ap.add_argument("--manifest", help="manifest.json из extract.py — заполнит «Источники» и проверит ссылки")
    ap.add_argument("--max-pages", type=int, default=2)
    ap.add_argument("--pdf", action="store_true", help="сохранить PDF-превью рядом с docx (LibreOffice/Word)")
    ap.add_argument("--page-check", default="auto", choices=["auto", "libreoffice", "word", "estimate"])
    ap.add_argument("--check", action="store_true", help="только валидация")
    a = ap.parse_args()
    for stream in (sys.stdout, sys.stderr):  # консоль Windows в cp1251 не должна ронять вывод
        try:
            stream.reconfigure(errors="replace")
        except Exception:  # noqa: BLE001
            pass

    data = json.loads(Path(a.analysis).read_text(encoding="utf-8"))
    doc_units = None
    if a.manifest:
        manifest = json.loads(Path(a.manifest).read_text(encoding="utf-8"))
        if not data.get("sources"):
            data["sources"] = sources_from_manifest(manifest)
        doc_units = {d["id"]: (d["type"], int(d["units"])) for d in manifest.get("documents", [])}
    elif not data.get("sources"):
        print("[!] нет --manifest и нет sources: ссылки не проверяются, блок «Источники» не будет выведен",
              file=sys.stderr)
    known = {_s(s.get("id")) for s in data.get("sources") or [] if isinstance(s, dict)} or None
    data.setdefault("meta", {}).setdefault("date", datetime.now().strftime("%Y-%m-%d"))

    errors = validate(data, known, doc_units)
    if errors:
        print("ОШИБКИ ВАЛИДАЦИИ analysis.json:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(2)
    if a.check:
        print(f"OK: валидно. Объём текста {text_volume(data)} симв.\n{fill_report(data)}")
        return

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    res = build(data, a.max_pages, a.page_check)
    out.write_bytes(res["docx"])
    if a.pdf and res["pdf"]:
        out.with_suffix(".pdf").write_bytes(res["pdf"])
    est = res["estimate"]
    how = f"{res['pages']} стр. ({res['method']}" + (f"; шрифт для оценки: {est['fonts']}" if res["method"] == "оценка"
                                                     else "") + ")"
    if not res["ok"]:
        print(f"НЕ ПОМЕЩАЕТСЯ: {how} при лимите {a.max_pages} даже в профиле «{res['profile']}». "
              f"Сократите самые длинные поля: {', '.join(longest_fields(data))}.", file=sys.stderr)
        sys.exit(3)
    print(f"OK: {out}  ·  профиль «{res['profile']}»  ·  {how}")
    print(fill_report(data))


if __name__ == "__main__":
    main()
