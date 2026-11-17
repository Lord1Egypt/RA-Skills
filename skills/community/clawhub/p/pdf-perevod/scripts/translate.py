# -*- coding: utf-8 -*-
"""translate.py — перевод PDF на русский с сохранением исходной вёрстки.

Принцип: страница не пересобирается. Скрипт находит текстовые блоки, агент переводит
их по идентификаторам, скрипт убирает исходный текст из блока и вписывает русский в ту
же рамку (тем же кеглем, цветом и начертанием; если русский длиннее — кегль плавно
уменьшается). Графики, иллюстрации, фон, таблицы и цвета остаются оригинальными.

Команды:
  extract  <job> [--pages 1-10] [--all]     блоки для перевода (по умолчанию — только непереведённые)
  put      <job> --json '{"p3u2": "…"}' | --file <путь>   сдать переводы блоков
  glossary <job> [--json '{"term": "перевод"}']            единый словарь терминов документа
  status   <job>                             прогресс и предупреждения
  build    <job> [--paper a4|source] [--allow-missing]      собрать <название>_перевод.pdf

Сканы и растровые картинки с текстом: после pdf.py ocr их блоки берутся из распознавания,
исходные надписи закрашиваются цветом фона, русский текст набирается сверху. Без OCR
такие страницы копируются как есть и перечисляются в отчёте.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import statistics
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _core as core  # noqa: E402

UNITS_VERSION = 3
EXTRACT_CAP = 16_000
A4 = (595.28, 841.89)
BULLET_RE = re.compile(r"^\s*(?:[—–\-•▪■●◦]|\d{1,2}[.)])\s+")
BULLET_ONLY_RE = re.compile(r"^\s*[—–\-•▪■●◦·]\s*$")


def _line_text(line: dict) -> str:
    return "".join(sp["text"] for sp in line["spans"])


def _is_bold(sp: dict) -> bool:
    name = sp.get("font", "").lower()
    return bool(sp["flags"] & 16) or any(k in name for k in ("bold", "black", "heavy", "semibold", "demi", "medium"))


def _line_style(line: dict) -> tuple:
    best, size, color, bold, italic = 0, 10.0, 0, False, False
    for sp in line["spans"]:
        n = len(sp["text"].strip())
        if n > best:
            best = n
            size, color = float(sp["size"]), int(sp["color"])
            name = sp.get("font", "").lower()
            bold = _is_bold(sp)
            italic = bool(sp["flags"] & 2) or "italic" in name or "oblique" in name
    return size, color, bold, italic


def _line_weight(line: dict) -> str:
    flags = [_is_bold(sp) for sp in line["spans"] if sp["text"].strip()]
    if flags and all(flags):
        return "all"
    return "none" if not any(flags) else "mixed"


def _rich_text(lines: list[dict]) -> tuple[str, bool]:
    segs: list[list] = []
    plain = ""
    for ln in lines:
        first = True
        for sp in ln["spans"]:
            t = re.sub(r"\s+", " ", sp["text"])
            if not t.strip() and not segs:
                continue
            if first and plain:
                if plain.endswith("-") and len(plain) > 2 and plain[-2].isalpha() and t.lstrip()[:1].islower():
                    plain = plain[:-1]
                    segs[-1][0] = segs[-1][0].rstrip()[:-1]
                    t = t.lstrip()
                elif not plain.endswith(" "):
                    t = " " + t.lstrip()
            first = False
            b = _is_bold(sp)
            sup = bool(sp["flags"] & 1) and len(t.strip()) <= 3 and not re.search(r"[^\W\d_]{2,}", t)
            if segs and segs[-1][1] == b and segs[-1][2] == sup:
                segs[-1][0] += t
            else:
                segs.append([t, b, sup])
            plain += t
    letters_b = sum(len(re.findall(r"[^\W\d_]", t)) for t, b, _s in segs if b)
    letters_r = sum(len(re.findall(r"[^\W\d_]", t)) for t, b, _s in segs if not b)
    mixed = letters_b >= 3 and letters_r >= 3
    has_sup = any(sp for _t, _b, sp in segs)
    if not mixed and not has_sup:
        return re.sub(r"\s+", " ", plain).strip(), False
    out = ""
    for t, b, sp in segs:
        if sp and t.strip():
            out += "%s<sup>%s</sup>%s" % (" " if t.startswith(" ") else "", t.strip(), " " if t.endswith(" ") else "")
        elif mixed and b and t.strip():
            lead = " " if t.startswith(" ") else ""
            tail = " " if t.endswith(" ") else ""
            out += "%s<b>%s</b>%s" % (lead, t.strip(), tail)
        else:
            out += t
    return re.sub(r"\s+", " ", out).strip(), mixed


def _join_lines(texts: list[str]) -> str:
    out = ""
    for t in texts:
        t = re.sub(r"\s+", " ", t).strip()
        if not t:
            continue
        if out.endswith("-") and len(out) > 2 and out[-2].isalpha() and t[:1].islower():
            out = out[:-1] + t
        elif out:
            out += " " + t
        else:
            out = t
    return out


def _needs_translation(text: str) -> bool:
    latin = len(re.findall(r"[A-Za-z]", text))
    return latin >= 2 and len(re.findall(r"[A-Za-z]{2,}", text)) >= 1


_FUNC_WORDS = {"the", "a", "an", "of", "to", "and", "or", "in", "for", "with", "that", "by", "at", "on", "from", "as",
               "is", "are", "was", "were", "be", "their", "its", "this", "these", "than", "which", "who", "but", "not", "&"}
_END_PUNCT_RE = re.compile(r"[.!?:;…][\"'»”’)\]]*\d{0,2}$")


def _is_horizontal(ln: dict) -> bool:
    return abs(ln["dir"][0] - 1) < 0.02 and abs(ln["dir"][1]) < 0.02


def _strong_link(a: str, b: str) -> bool:
    a = a.strip()
    last = re.sub(r"[^\w&]+$", "", a.split()[-1].lower()) if a.split() else ""
    return a[-1:] in ",-–—/" or last in _FUNC_WORDS or (b[:1] == "(" and len(a) < 40)


def _continues(prev_text: str, next_text: str, strong_only: bool = False) -> bool:
    a = _strip_tags(prev_text).strip()
    b = _strip_tags(next_text).strip()
    if not a or not b or _END_PUNCT_RE.search(a):
        return False
    if BULLET_RE.match(b) or b[:1] in "•·▪■●◦—–":
        return False
    if _strong_link(a, b):
        return True
    if strong_only:
        return False
    first = re.search(r"[^\W\d_]", b)
    return bool(first and first.group(0).islower())


def _numeric_label(text: str) -> bool:
    """Строка-число: цифры с единицами и знаками, без слов (p. p., %, $, +/-)."""
    t = _strip_tags(text)
    return bool(re.search(r"\d", t)) and not re.search(r"[A-Za-z\u0410-\u044f\u0401\u0451]{3,}", t)

def _merge_groups(groups: list[list[dict]]) -> list[list[dict]]:
    text_cache: dict[int, str] = {}

    def text_of(g) -> str:
        key = (id(g), len(g))
        if key not in text_cache:
            text_cache[key] = _rich_text(g)[0]
        return text_cache[key]

    alive = {id(g) for g in groups}

    grid: dict[int, list] = {}
    for g in groups:
        grid.setdefault(int(g[0]["bbox"][0] // 3), []).append(g)
    for cell in grid.values():
        cell.sort(key=lambda g: g[0]["bbox"][1])

    def below(a):
        la = a[-1]
        sa, ca, _ba, ia = _line_style(la)
        key = int(la["bbox"][0] // 3)
        best = None
        for k in (key - 1, key, key + 1):
            for b in grid.get(k, ()):
                if b is a or id(b) not in alive:
                    continue
                lb = b[0]
                step = lb["bbox"][1] - la["bbox"][1]
                if step < 0.95 * sa:
                    continue
                if step > 1.75 * sa:
                    break
                if abs(la["bbox"][0] - lb["bbox"][0]) > 2.5:
                    continue
                sb, cb, _bb, ib = _line_style(lb)
                if abs(sa - sb) > 0.03 * sa or ca != cb or ia != ib:
                    continue
                if {_line_weight(la), _line_weight(lb)} == {"all", "none"}:
                    continue
                pitches = [g[i + 1]["bbox"][1] - g[i]["bbox"][1] for g in (a, b) for i in range(len(g) - 1)]
                if pitches and abs(step - statistics.median(pitches)) > 0.25 * sa:
                    continue
                widest = max(l["bbox"][2] - l["bbox"][0] for l in a + b)
                if la["bbox"][2] - la["bbox"][0] < 0.7 * widest:
                    continue
                both_single = len(a) == 1 and len(b) == 1
                if not _continues(text_of(a), text_of(b), strong_only=both_single):
                    continue
                if best is None or step < best[0]:
                    best = (step, b)
        return best[1] if best else None

    for a in sorted(groups, key=lambda g: g[0]["bbox"][1]):
        if id(a) not in alive:
            continue
        for _ in range(60):
            if len(_line_text(a[-1]).strip()) < (25 if len(a) == 1 else 20):
                break
            b = below(a)
            if b is None:
                break
            a.extend(b)
            alive.discard(id(b))

    def edge(g, kind):
        vals = [l["bbox"][2] if kind == "right" else (l["bbox"][0] + l["bbox"][2]) / 2 for l in g]
        return max(vals) - min(vals), sum(vals) / len(vals)

    for kind, tol, cap in (("right", 1.5, 4), ("center", 2.0, 5)):
        labels = []
        for g in groups:
            if id(g) in alive and len(g) <= 4:
                spread, pos = edge(g, kind)
                if spread < tol:
                    labels.append((g, pos))
        cols: dict[int, list] = {}
        for g, pos in labels:
            cols.setdefault(int(pos // 2), []).append((g, pos))
        for col in cols.values():
            col.sort(key=lambda t: t[0][0]["bbox"][1])
        done: set[int] = set()
        for g, pos in sorted(labels, key=lambda t: t[0][0]["bbox"][1]):
            if id(g) in done or id(g) not in alive:
                continue
            chain, cur, cur_pos = [g], g, pos
            while len(chain) < 12:
                la = cur[-1]
                sa, ca, ba, _ia = _line_style(la)
                nxt = None
                for k in (int(cur_pos // 2) - 1, int(cur_pos // 2), int(cur_pos // 2) + 1):
                    for h, hpos in cols.get(k, ()):
                        step = h[0]["bbox"][1] - la["bbox"][1]
                        if step < 0.9 * sa or id(h) in done or id(h) not in alive or any(h is c for c in chain):
                            continue
                        if step > 1.4 * sa:
                            break
                        sh, ch, bh, _ih = _line_style(h[0])
                        if abs(hpos - cur_pos) < tol and abs(sh - sa) <= 0.03 * sa and ch == ca and bh == ba:
                            if nxt is None or step < nxt[0]:
                                nxt = (step, h, hpos)
                if nxt is None:
                    break
                chain.append(nxt[1])
                cur, cur_pos = nxt[1], nxt[2]
            for c in chain:
                done.add(id(c))
            if len(chain) < 2 or sum(len(c) for c in chain) > cap:
                continue
            # столбец чисел в таблице (−20.0 pp / +16.5 pp …) — не подписи в столбик:
            # склейка в один блок ломает построчное выравнивание при сборке
            if all(_numeric_label(text_of(c)) for c in chain):
                continue
            head = re.search(r"[^\W_]", _strip_tags(text_of(chain[0])))
            weak_ok = bool(head and not head.group(0).islower())
            if not all(_continues(text_of(x), text_of(y), strong_only=not weak_ok) for x, y in zip(chain, chain[1:])):
                continue
            for c in chain[1:]:
                chain[0].extend(c)
                alive.discard(id(c))
    return [g for g in groups if id(g) in alive]


def page_units(pymupdf, page, pno: int, raw: dict | None = None) -> list[dict]:
    flags = pymupdf.TEXT_PRESERVE_WHITESPACE | pymupdf.TEXT_MEDIABOX_CLIP
    if raw is None:
        raw = page.get_text("dict", flags=flags)
    units: list[dict] = []

    def flush(lines: list[dict]) -> None:
        if not lines:
            return
        text, mixed = _rich_text(lines)
        if not text:
            return
        sizes = [(_line_style(ln), len(_line_text(ln))) for ln in lines]
        (size, color, bold, italic), _n = max(sizes, key=lambda s: s[1])
        if mixed:
            bold = False
        x0 = min(ln["bbox"][0] for ln in lines); y0 = min(ln["bbox"][1] for ln in lines)
        x1 = max(ln["bbox"][2] for ln in lines); y1 = max(ln["bbox"][3] for ln in lines)
        pitch = 1.2
        if len(lines) > 1:
            steps = [b["bbox"][1] - a["bbox"][1] for a, b in zip(lines, lines[1:]) if b["bbox"][1] > a["bbox"][1]]
            if steps and size > 0:
                pitch = min(1.7, max(1.0, statistics.median(steps) / size))
        align = "left"
        if len(lines) > 1:
            lefts = [ln["bbox"][0] for ln in lines]; rights = [ln["bbox"][2] for ln in lines]
            mids = [(a + b) / 2 for a, b in zip(lefts, rights)]
            spread = lambda v: max(v) - min(v)  # noqa: E731
            if spread(rights) < 1.5 and spread(lefts) > 1.5:
                align = "right"
            elif spread(mids) < (3 if spread(lefts) > 6 else 1.5) and spread(lefts) > 0.5:
                align = "center"
        units.append({
            "text": text, "bbox": [round(v, 2) for v in (x0, y0, x1, y1)],
            "lines": [[round(v, 2) for v in ln["bbox"]] for ln in lines],
            "size": round(size, 2), "color": "#%06x" % color, "bold": bold, "italic": italic,
            "pitch": round(pitch, 2), "align": align, "n_lines": len(lines), "rich": mixed,
        })

    groups: list[list[dict]] = []
    rotated: list[tuple[int, int, dict]] = []
    for bi, block in enumerate(raw.get("blocks", [])):
        if block.get("type") != 0:
            continue
        for li, ln in enumerate(block.get("lines", [])):
            if _line_text(ln).strip() and not _is_horizontal(ln):
                rotated.append((bi, li, ln))
        lines = [ln for ln in block.get("lines", [])
                 if _line_text(ln).strip() and _is_horizontal(ln) and not BULLET_ONLY_RE.match(_line_text(ln))]
        if not lines:
            continue
        lines.sort(key=lambda ln: (round(ln["bbox"][1], 1), ln["bbox"][0]))
        tabular = False
        if len(lines) <= 80:
            for k, a in enumerate(lines):
                for b in lines[k + 1:]:
                    ha = min(a["bbox"][3] - a["bbox"][1], b["bbox"][3] - b["bbox"][1])
                    overlap = min(a["bbox"][3], b["bbox"][3]) - max(a["bbox"][1], b["bbox"][1])
                    apart = max(b["bbox"][0] - a["bbox"][2], a["bbox"][0] - b["bbox"][2])
                    if ha > 0 and overlap > 0.6 * ha and apart > 0.8 * ha:
                        tabular = True
                        break
                if tabular:
                    break
        if tabular:
            groups.extend([ln] for ln in lines)
            continue
        cur: list[dict] = []
        for ln in lines:
            if cur:
                ps, _pc, pb, _pi = _line_style(cur[-1])
                s, _c, b, _i = _line_style(ln)
                gap = ln["bbox"][1] - cur[-1]["bbox"][3]
                weight_break = ({_line_weight(cur[-1]), _line_weight(ln)} == {"all", "none"}) and gap > 0.35 * ps
                apart = ln["bbox"][0] > cur[-1]["bbox"][2] + 1 or ln["bbox"][2] < cur[-1]["bbox"][0] - 1
                new_par = (
                    abs(s - ps) > 0.12 * ps
                    or weight_break
                    or apart
                    or gap > 0.75 * ps
                    or BULLET_RE.match(_line_text(ln))
                )
                if new_par:
                    groups.append(cur)
                    cur = []
            cur.append(ln)
        if cur:
            groups.append(cur)

    for g in _merge_groups(groups):
        g.sort(key=lambda ln: (round(ln["bbox"][1], 1), ln["bbox"][0]))
        flush(g)

    if rotated:
        import math
        def ang(ln):
            return round(math.degrees(math.atan2(ln["dir"][1], ln["dir"][0])) * 2) / 2
        angles = [ang(ln) for _b, _l, ln in rotated]
        distinct = len(set(angles))
        keep = []
        for (bi, li, ln), a in zip(rotated, angles):
            text = re.sub(r"\s+", " ", _line_text(ln)).strip()
            letters = len(re.findall(r"[^\W\d_]", text))
            shared = sum(1 for b in angles if abs(b - a) < 0.75)
            regular = abs(a / 45 - round(a / 45)) * 45 < 1.0
            if letters >= 4 and (shared >= 2 or (regular and distinct <= 6)) and not (distinct > 12 and shared < 3):
                keep.append((bi, li, ln))
        rotated = keep
    if rotated:
        rawc = page.get_text("rawdict", flags=flags)
        for bi, li, ln in rotated:
            text = re.sub(r"\s+", " ", _line_text(ln)).strip()
            try:
                all_chars = [c for sp in rawc["blocks"][bi]["lines"][li]["spans"] for c in sp["chars"]]
            except (IndexError, KeyError):
                all_chars = []
            chars = [c for c in all_chars if c["c"].strip()]
            if len(text) < 2 or len(chars) < 2:
                continue
            size, color, bold, italic = _line_style(ln)
            dx, dy = ln["dir"]
            p0 = chars[0]["origin"]
            adv = max(0.3 * size, ((chars[-1]["origin"][0] - chars[-2]["origin"][0]) ** 2
                                   + (chars[-1]["origin"][1] - chars[-2]["origin"][1]) ** 2) ** 0.5)
            p1 = (chars[-1]["origin"][0] + dx * adv, chars[-1]["origin"][1] + dy * adv)
            units.append({
                "text": text, "bbox": [round(v, 2) for v in ln["bbox"]], "lines": [],
                "chars": [[round(v, 2) for v in c["bbox"]] for c in all_chars],
                "rot": [round(dx, 4), round(dy, 4)], "p0": [round(p0[0], 2), round(p0[1], 2)],
                "p1": [round(p1[0], 2), round(p1[1], 2)],
                "size": round(size, 2), "color": "#%06x" % color, "bold": bold, "italic": italic,
                "pitch": 1.2, "align": "left", "n_lines": 1, "rich": False,
            })

    sizes = [u["size"] for u in units for _ in range(max(1, len(u["text"]) // 40))]
    body = statistics.median(sizes) if sizes else 10.0
    for u in list(units):
        if re.fullmatch(r"[A-Z]", u["text"].strip()) and u["size"] >= 1.8 * body:
            cands = [v for v in units if v is not u and re.sub(r"^(?:<[bi]>)+", "", v["text"])[:1].islower()
                     and v["bbox"][0] >= u["bbox"][0] and v["bbox"][1] < u["bbox"][3] + body
                     and v["bbox"][3] > u["bbox"][1] - body]
            if cands:
                tgt = min(cands, key=lambda v: abs(v["bbox"][1] - u["bbox"][1]) + abs(v["bbox"][0] - u["bbox"][2]))
                letter = u["text"].strip()
                tgt["text"] = re.sub(r"^((?:<[bi]>)*)", lambda m: m.group(1) + letter, tgt["text"], count=1)
                tgt["lines"] = u["lines"] + tgt["lines"]
                units.remove(u)

    def flush_right(u) -> bool:
        rights = [lb[2] for lb in u["lines"]] or [u["bbox"][2]]
        return max(rights) - min(rights) < 1.5

    labels = [u for u in units if u["n_lines"] <= 3 and not u.get("rot") and _needs_translation(u["text"]) and flush_right(u)]
    for u in labels:
        mates = [v for v in labels if abs(v["bbox"][2] - u["bbox"][2]) < 1.5 and abs(v["size"] - u["size"]) < 0.6]
        if len(mates) >= 3 and max(v["bbox"][0] for v in mates) - min(v["bbox"][0] for v in mates) > 6:
            u["align"] = "right"
    centered = [u for u in units if u["align"] == "center" and u["n_lines"] <= 4]
    for u in units:
        if u.get("rot") or u["align"] != "left" or u["n_lines"] > 3 or not _needs_translation(u["text"]):
            continue
        if u["n_lines"] > 1:
            mids = [(lb[0] + lb[2]) / 2 for lb in u["lines"]]
            if max(mids) - min(mids) > 1.5:
                continue
        row = [v for v in centered if abs(v["bbox"][1] - u["bbox"][1]) < 2.5 and abs(v["size"] - u["size"]) < 0.3]
        if len(row) >= 2:
            u["align"] = "center"

    out = []
    for i, u in enumerate(units, 1):
        u["id"] = "p%du%d" % (pno, i)
        u["page"] = pno
        u["translate"] = _needs_translation(u["text"])
        role = "b"
        if u["size"] >= 1.25 * body or (u["bold"] and len(u["text"]) < 90 and u["n_lines"] <= 2):
            role = "h"
        elif u["size"] <= 0.82 * body:
            role = "s"
        u["role"] = role
        out.append(u)
    return out


def _ocr_raw(rows: list[dict]) -> dict:
    flat = sorted((r for r in rows if abs(r["angle"]) < 10), key=lambda r: (round(r["bbox"][1], 1), r["bbox"][0]))

    def short(r: dict) -> bool:
        return len(r["text"].split()) <= 3 and r["bbox"][2] - r["bbox"][0] <= 120

    def numeric(r: dict) -> bool:
        """Строка-число с единицей: -20.0 pp, +5.8 pp, $30.09 — слов в ней нет."""
        return bool(re.search(r"\d", r["text"])) and not re.search(r"[^\W\d_]{3,}", r["text"])

    def joins(p: dict, r: dict) -> float:
        gap = r["bbox"][1] - p["bbox"][3]
        overlap = min(r["bbox"][2], p["bbox"][2]) - max(r["bbox"][0], p["bbox"][0])
        width = min(r["bbox"][2] - r["bbox"][0], p["bbox"][2] - p["bbox"][0])
        if overlap <= 0:
            return 0.0
        same = (-0.5 * p["size"] < gap <= 0.9 * max(p["size"], r["size"])
                and abs(r["size"] - p["size"]) <= 0.25 * p["size"] and abs(r["bbox"][0] - p["bbox"][0]) <= 3.0
                and not (short(p) and not short(r) and gap > 0.4 * p["size"])
                and not (short(r) and not short(p) and r["text"][:1].isupper()
                         and not _END_PUNCT_RE.search(p["text"].strip()) and not _strong_link(p["text"], r["text"]))
                and not (numeric(p) and numeric(r)))
        stack = (short(p) and short(r) and -0.5 * p["size"] < gap <= 0.5 * max(p["size"], r["size"])
                 and overlap >= 0.5 * width and abs(r["size"] - p["size"]) <= 0.3 * p["size"]
                 # столбец чисел в таблице — не многострочная подпись: склейка ломает
                 # построчное выравнивание, каждое значение должно остаться своим блоком
                 and not (numeric(p) and numeric(r)))
        return overlap / max(width, 1.0) if (same or stack) else 0.0

    blocks: list[list[dict]] = []
    for r in flat:
        best, score = None, 0.0
        for b in blocks:
            p = b[-1]
            if r["bbox"][1] - p["bbox"][3] > 1.0 * max(p["size"], r["size"]):
                continue
            sc = joins(p, r)
            if sc > score:
                best, score = b, sc
        if best is None:
            blocks.append([r])
        else:
            best.append(r)
    row_sizes = {id(r): [r["size"]] for r in flat}
    wordy = {id(r): bool(re.search(r"[^\W\d_]{2,}", r["text"])) for r in flat}
    for i, a in enumerate(flat):
        if not wordy[id(a)]:
            continue
        for b in flat[i + 1:]:
            if b["bbox"][1] >= a["bbox"][3]:
                break
            if not wordy[id(b)]:
                continue
            ov = min(a["bbox"][3], b["bbox"][3]) - max(a["bbox"][1], b["bbox"][1])
            ha, hb = a["bbox"][3] - a["bbox"][1], b["bbox"][3] - b["bbox"][1]
            if ov >= 0.7 * min(ha, hb) and abs(a["size"] - b["size"]) <= 0.15 * max(a["size"], b["size"]):
                row_sizes[id(a)].append(b["size"])
                row_sizes[id(b)].append(a["size"])
    for r in flat:
        r["size"] = round(statistics.median(row_sizes[id(r)]), 2)
    for b in blocks:
        size = round(statistics.median(r["size"] for r in b), 2)
        for r in b:
            r["size"] = size
    sizes = sorted({r["size"] for b in blocks for r in b})
    clusters: list[list[float]] = []
    for sz in sizes:
        if clusters and sz <= clusters[-1][0] * 1.12:
            clusters[-1].append(sz)
        else:
            clusters.append([sz])
    snap = {sz: round(statistics.median(c), 2) for c in clusters for sz in c}
    for b in blocks:
        for r in b:
            r["size"] = snap[r["size"]]

    def line(r: dict) -> dict:
        return {"bbox": list(r["bbox"]), "dir": (1.0, 0.0),
                "spans": [{"text": r["text"], "size": r["size"], "flags": 0, "font": "ocr", "color": int(r["fg"][1:], 16)}]}

    return {"blocks": [{"type": 0, "lines": [line(r) for r in b]} for b in blocks]}


def ocr_units(pymupdf, page, pno: int, rows: list[dict], start: int) -> list[dict]:
    import math
    units = page_units(pymupdf, page, pno, raw=_ocr_raw(rows)) if rows else []
    by_box: dict[tuple, list] = {}
    for r in rows:
        by_box.setdefault(tuple(round(v, 2) for v in r["bbox"]), []).append(r)
    for u in units:
        paint, busy = [], False
        for lb in u["lines"]:
            cands = by_box.get(tuple(lb))
            r = cands.pop(0) if cands else None
            if r is None:
                paint.append({"quad": [[lb[0], lb[1]], [lb[2], lb[1]], [lb[2], lb[3]], [lb[0], lb[3]]], "bg": "#ffffff"})
                continue
            item = {"quad": r["quad"], "bg": r["bg"]}
            if r.get("strip"):
                item["strip"] = r["strip"]
            paint.append(item)
            busy = busy or bool(r.get("busy"))
        u["ocr"] = True
        u["paint"] = paint
        if busy:
            u["busy"] = True
        h = 1.2 * u["size"]
        u["lines"] = [[lb[0], round((lb[1] + lb[3]) / 2 - h / 2, 2), lb[2], round((lb[1] + lb[3]) / 2 + h / 2, 2)] for lb in u["lines"]]
        u["bbox"] = [round(min(lb[0] for lb in u["lines"]), 2), round(min(lb[1] for lb in u["lines"]), 2),
                     round(max(lb[2] for lb in u["lines"]), 2), round(max(lb[3] for lb in u["lines"]), 2)]
    for r in rows:
        if abs(r["angle"]) < 10 or len(r["text"]) < 2:
            continue
        q = r["quad"]
        ang = math.radians(r["angle"])
        dx, dy = math.cos(ang), math.sin(ang)
        if abs(dx) < 0.1:
            dx, dy = 0.0, -1.0
        nx, ny = -dy, dx
        pts = sorted(q, key=lambda p: p[0] * nx + p[1] * ny)[2:]
        pts.sort(key=lambda p: p[0] * dx + p[1] * dy)
        p0, p1 = pts[0], pts[1]
        units.append({
            "text": r["text"], "bbox": list(r["bbox"]), "lines": [], "chars": [],
            "rot": [round(dx, 4), round(dy, 4)], "p0": [round(p0[0], 2), round(p0[1], 2)],
            "p1": [round(p1[0], 2), round(p1[1], 2)],
            "size": r["size"], "color": r["fg"], "bold": False, "italic": False,
            "pitch": 1.2, "align": "left", "n_lines": 1, "rich": False,
            "ocr": True, "paint": [{"quad": q, "bg": r["bg"]}], "page": pno,
            "translate": _needs_translation(r["text"]), "role": "s",
        })
    for k, u in enumerate(units, start):
        u["id"] = "p%du%d" % (pno, k)
    return units


def _paint_layer_units(pymupdf, page, units: list[dict]) -> None:
    try:
        import _ocr as ocr
        _bgr, rgb, s = ocr.render(pymupdf, page, 100)
    except Exception:
        rgb, s = None, 1.0
    for u in units:
        if u.get("rot"):
            continue
        paint, fgs = [], []
        for lb in u["lines"]:
            quad = [[lb[0], lb[1]], [lb[2], lb[1]], [lb[2], lb[3]], [lb[0], lb[3]]]
            item = {"quad": quad, "bg": "#ffffff"}
            if rgb is not None:
                bg, fg, busy, strip = ocr.colors(rgb, [[p[0] * s, p[1] * s] for p in quad])
                item["bg"] = bg
                if strip:
                    item["strip"] = strip
                fgs.append(fg)
            paint.append(item)
        u["paint"] = paint
        if fgs:
            u["color"] = max(set(fgs), key=fgs.count)
        u["layer"] = True


def _attach_ocr(pymupdf, jdir: Path, store: dict, doc) -> bool:
    ocr_dir = jdir / "ocr"
    if not ocr_dir.is_dir():
        return False
    seen = set(store.setdefault("ocr_pages", []))
    changed = False
    for f in sorted(ocr_dir.glob("[0-9][0-9][0-9][0-9].json")):
        pno = int(f.stem)
        if pno in seen or pno > store["pages_done"]:
            continue
        data = core.read_json(f, {})
        rows = data.get("rows") or []
        kind = data.get("kind", "scan")
        page = doc[pno - 1]
        if page.rotation:
            page.remove_rotation()
        if kind in ("scan", "broken"):
            store["units"] = [u for u in store["units"] if u["page"] != pno]
            start = 1
        else:
            start = max([int(u["id"].split("u")[1]) for u in store["units"] if u["page"] == pno] + [0]) + 1
        store["units"].extend(ocr_units(pymupdf, page, pno, rows, start))
        store["units"].sort(key=lambda u: (u["page"], int(u["id"].split("u")[1])))
        seen.add(pno)
        store["ocr_pages"] = sorted(seen)
        changed = True
    return changed


def load_units(pymupdf, jdir: Path, deadline=None) -> dict:
    path = jdir / "tr" / "units.json"
    store = core.read_json(path, {"v": UNITS_VERSION, "pages_done": 0, "units": []})
    meta = core.read_json(jdir / "meta.json", {})
    total = int(meta.get("pages_total", 0))
    kinds = {int(p["n"]): p.get("kind", "text") for p in meta.get("page_info", [])}
    if store.get("v") != UNITS_VERSION:
        tr_dir = jdir / "tr"
        had_units = bool(store.get("units"))
        if had_units:
            core.write_json(tr_dir / "units.old.json", store)
            for name in ("translations.json", "autofill.json"):
                f, old = tr_dir / name, tr_dir / name.replace(".json", ".old.json")
                if f.is_file():
                    os.replace(f, old)
            for name in ("warnings.json", "progress.json", "fit.json", "work.pdf"):
                f = tr_dir / name
                if f.is_file():
                    f.unlink()
        store = {"v": UNITS_VERSION, "pages_done": 0, "units": [], "migrate": had_units}
        core.write_json(path, store)
    doc = None
    if store["pages_done"] >= total:
        changed = False
        if store.get("migrate"):
            _migrate_translations(jdir, store)
            changed = True
        if (jdir / "ocr").is_dir():
            doc = pymupdf.open(jdir / "source.pdf")
            changed = _attach_ocr(pymupdf, jdir, store, doc) or changed
        if changed:
            core.write_json(path, store)
        return store
    doc = pymupdf.open(jdir / "source.pdf")
    for pno in range(store["pages_done"] + 1, total + 1):
        page = doc[pno - 1]
        if page.rotation:
            page.remove_rotation()
        kind = kinds.get(pno, "text")
        if kind not in ("scan", "broken"):
            units = page_units(pymupdf, page, pno)
            if kind == "scan_text":
                _paint_layer_units(pymupdf, page, units)
            store["units"].extend(units)
        store["pages_done"] = pno
        if deadline is not None and deadline.expired():
            break
    if store["pages_done"] >= total and store.get("migrate"):
        _migrate_translations(jdir, store)
    if (jdir / "ocr").is_dir():
        _attach_ocr(pymupdf, jdir, store, doc)
    core.write_json(path, store)
    return store


def _read_loose(path: Path, default):
    import json
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _migrate_translations(jdir: Path, store: dict) -> None:
    tr_dir = jdir / "tr"
    old_units = _read_loose(tr_dir / "units.old.json", {})
    old_units = old_units.get("units", []) if isinstance(old_units, dict) else []
    old_tr = _read_loose(tr_dir / "translations.old.json", {})
    old_auto = _read_loose(tr_dir / "autofill.old.json", {})
    if not isinstance(old_tr, dict):
        old_tr = {}
    if not isinstance(old_auto, dict):
        old_auto = {}
    queue: dict = {}
    for u in old_units:
        if isinstance(u, dict) and u.get("id") in old_tr:
            queue.setdefault((u.get("page"), _norm_src(u.get("text", ""))), []).append(u["id"])
    new_tr = core.read_json(tr_dir / "translations.json", {})
    new_auto = core.read_json(tr_dir / "autofill.json", {})
    old_to_new: dict = {}
    kept = 0
    for u in store["units"]:
        ids = queue.get((u["page"], _norm_src(u["text"])))
        if not ids or not u["translate"]:
            continue
        old_id = ids.pop(0) if len(ids) > 1 else ids[0]
        old_to_new.setdefault(old_id, u["id"])
        if u["id"] not in new_tr:
            new_tr[u["id"]] = old_tr[old_id]
            kept += 1
            src = old_auto.get(old_id)
            if src:
                new_auto[u["id"]] = src
    for uid, src in list(new_auto.items()):
        if src in old_to_new:
            new_auto[uid] = old_to_new[src]
        elif src not in new_tr:
            new_auto.pop(uid)
    core.write_json(tr_dir / "translations.json", new_tr)
    core.write_json(tr_dir / "autofill.json", new_auto)
    store.pop("migrate", None)
    store["migrated"] = {"kept": kept, "of": len(old_tr)}


class _PageRect:

    def __init__(self, size):
        w, h = size or (595.0, 842.0)
        self.x0, self.y0, self.x1, self.y1, self.width, self.height = 0.0, 0.0, float(w), float(h), float(w), float(h)


def _norm_src(t: str) -> str:
    return re.sub(r"\s+", " ", _TAG_RE.sub("", t)).strip().lower()


def _load_tr(jdir: Path) -> dict:
    return core.read_json(jdir / "tr" / "translations.json", {})


def cmd_extract(args) -> None:
    pymupdf = core.require_pymupdf()
    jdir = core.job_dir(args.job)
    deadline = core.Deadline(200)
    store = load_units(pymupdf, jdir, deadline)
    meta = core.read_json(jdir / "meta.json", {})
    total = int(meta.get("pages_total", 0))
    if store["pages_done"] < total:
        core.out({"ok": True, "complete": False, "pages_indexed": store["pages_done"], "pages_total": total,
                  "next": "Документ большой: повторите translate.py extract — разбор продолжится."})
    tr = _load_tr(jdir)
    wanted = set(core.parse_pages(args.pages, total))
    by_page: dict = {}
    for u in store["units"]:
        by_page.setdefault(u["page"], []).append(u)
    page_sizes = {p["n"]: (p["w"], p["h"]) for p in meta.get("page_info", [])}
    by_key: dict = {}
    for u in store["units"]:
        if u["translate"]:
            by_key.setdefault(_norm_src(u["text"]), []).append(u)
    shown, used, seen_src, last_page = [], 0, {}, None
    pages_sorted = sorted(wanted)
    stop_page = None
    for u in store["units"]:
        if u["page"] not in wanted or not u["translate"]:
            continue
        if stop_page is not None and u["page"] >= stop_page:
            continue
        if not args.all and u["id"] in tr:
            continue
        key = _norm_src(u["text"])
        if key in seen_src:
            continue
        item = {"id": u["id"], "t": u["text"], "role": u["role"]}
        if u.get("ocr"):
            item["ocr"] = True
            head = re.match(r"([a-z]+)", _strip_tags(u["text"]))
            if head and u["n_lines"] > 1 and head.group(1) not in _FUNC_WORDS and head.group(1) != "by":
                item["note"] = "начинается со строчной буквы: продолжение соседнего блока или абзац с буквицей, которую OCR не увидел — переводите по смыслу"
        if u.get("rot"):
            item["note"] = "наклонная подпись в одну строку — переводите предельно коротко"
        if len(by_key.get(key, [])) > 1:
            item["same"] = len(by_key[key]) - 1
        if u["n_lines"] <= 3 or len(u["text"]) < 90:
            twins = [o for o in by_key.get(key, [u]) if o["n_lines"] <= 3 or len(o["text"]) < 90][:40] or [u]
            fits, widths = [], []
            for o in twins:
                if o.get("rot"):
                    _anchor, max_len = _rot_plan(by_page.get(o["page"], [])).get(o["id"], ("center", 40.0))
                    fits.append(max(3, int(max_len / (0.56 * o["size"] * 0.85))))
                    continue
                page_units_ = [q for q in by_page.get(o["page"], []) if not q.get("rot")]
                xs = [q["bbox"] for q in page_units_]
                box, _al = _expand_rect(o, [q for q in page_units_ if q is not o], _PageRect(page_sizes.get(o["page"])),
                                        min(b[0] for b in xs), max(b[2] for b in xs))
                fits.append(_capacity(o, box))
                if o["n_lines"] > 1 or o["align"] == "center":
                    widths.append(_per_line(o, box))
            item["fit"] = min(fits)
            if widths and min(widths) < 24:
                item["w"] = min(widths)
        cost = len(u["text"]) + 40
        if shown and used + cost > EXTRACT_CAP:
            stop_page = u["page"]
            shown = [s for s in shown if int(s["id"][1:].split("u")[0]) < stop_page] or shown
            continue
        shown.append(item)
        seen_src[key] = item
        used += cost
        last_page = u["page"]
    resp = {
        "ok": True, "job": args.job, "units": shown, "count": len(shown),
        "glossary": core.read_json(jdir / "tr" / "glossary.json", {}),
        "legend": "id — идентификатор блока; t — исходный текст (теги <b>…</b> — полужирное выделение: сохраните их в переводе вокруг тех же по смыслу слов; "
                  "<sup>…</sup> — маркер сноски верхним индексом: оставьте его как есть на том же месте); "
                  "role: h — заголовок или крупный текст, b — основной текст, s — мелкий (сноски, подписи); "
                  "fit — сколько знаков перевода помещается в рамку блока без заметного уменьшения шрифта; w — сколько знаков в одной строке узкой рамки: слово длиннее w не поместится, берите слова короче; same — сколько ещё блоков с тем же текстом во всём документе (переведутся автоматически; fit у таких блоков — по самой тесной рамке); "
                  "ocr — текст распознан с картинки: в буквах и цифрах возможны ошибки OCR, переводите смысл, а сомнительное число сверьте по странице (pdf.py pages) или пропустите блок.",
    }
    if stop_page is not None:
        rest = [p for p in pages_sorted if p >= stop_page]
        resp["next_pages"] = "%d-%d" % (rest[0], rest[-1])
    pending = [p for p in _pages_pending_ocr(meta) if p in wanted]
    if pending:
        resp["pages_pending_ocr"] = pending[:60]
        resp["warnings"] = ["Страницы %s — сканы или картинки с текстом, ещё не распознанные: их блоков здесь нет. "
                            "Запустите pdf.py ocr %s и повторите extract." % (pending[:20], args.job)]
    if not shown:
        resp["note"] = "На этих страницах нечего переводить (всё переведено или нет текста)."
    else:
        resp["next"] = "Переведите блоки и сдайте: translate.py put %s --json '{\"%s\": \"…\", …}'" % (args.job, shown[0]["id"])
    core.out(resp)


def _latin_share(text: str) -> float:
    letters = re.findall(r"[A-Za-zА-Яа-яЁё]", text)
    if not letters:
        return 0.0
    return sum(1 for ch in letters if ch.isascii()) / len(letters)


CALQUES = [
    (r"\bкодинг\w*", "программирование"), (r"\bсофт(?!вер)\w{0,3}\b", "программы / ПО"), (r"\bредизайн\w*", "перестройка"),
    (r"\bворкфлоу\b", "рабочие процессы"), (r"\bимплементац\w+", "внедрение"), (r"\bдрайв(ить|ер\w*)\b", "фактор роста / двигать"),
    (r"\bкейс\w{0,3}\b", "пример / случай"), (r"\bинсайт\w*", "вывод / наблюдение"), (r"\bвалидир\w+", "проверять / подтверждать"),
    (r"\bхай-?перформер\w*", "лидеры"), (r"\bэнтерпрайз\w*", "крупные компании"),
]


def _calques(text: str) -> list[str]:
    low = text.lower()
    return ["«%s» → %s" % (m.group(0), fix) for rx, fix in CALQUES for m in [re.search(rx, low)] if m]


_WORD_RE = re.compile(r"[А-Яа-яЁёA-Za-z][А-Яа-яЁёA-Za-z0-9-]*")


def _glossary_forms(val: str) -> tuple[str, list[str]]:
    alts = [a.strip() for grp in re.findall(r"\(([^)]*)\)", val) for a in re.split(r"[,;/|]", grp) if a.strip()]
    main = re.sub(r"\s+", " ", re.sub(r"\([^)]*\)", " ", val)).strip()
    return main, alts


def _stems(text: str) -> list[str]:
    out = []
    for w in re.findall(r"[А-Яа-яЁёA-Za-z]{2,}", text):
        w = w.lower()
        out.append(w if len(w) <= 2 else w[:-1] if len(w) <= 4 else w[:-2])
    return out


def _has_form(ru_low: str, form: str) -> bool:
    f = form.strip()
    if not f:
        return False
    if f.upper() == f or re.search(r"[A-Za-z]", f):
        return re.search(r"(?<![А-Яа-яЁёA-Za-z0-9])%s(?![А-Яа-яЁёA-Za-z0-9])" % re.escape(f.lower()), ru_low) is not None
    stems = _stems(f)
    return bool(stems) and all(st in ru_low for st in stems)


def _glossary_check(term: str, val: str, ru_plain: str, src_plain: str) -> tuple[bool, str | None, bool]:
    main, alts = _glossary_forms(str(val))
    ru_low = ru_plain.lower()
    if (main and _has_form(ru_low, main)) or any(_has_form(ru_low, a) for a in alts):
        return True, None, False
    label = re.fullmatch(r"(?i)%s(?:e?s)?[.:]?" % re.escape(term.strip()), _norm_src(src_plain)) is not None
    if not label:
        return False, None, False
    budget = len(ru_plain) + 2
    if main and len(main) <= budget:
        return False, main, True
    fitting = [a for a in alts if len(a) <= budget and re.search(r"[А-Яа-яЁё]", a)]
    if fitting:
        return False, max(fitting, key=len), True
    return False, None, True


def cmd_put(args) -> None:
    pymupdf = core.require_pymupdf()
    jdir = core.job_dir(args.job)
    store = load_units(pymupdf, jdir, core.Deadline(200))
    by_id = {u["id"]: u for u in store["units"]}
    data = core.load_payload(args, "переводы блоков")
    if isinstance(data, list):
        data = {str(d.get("id")): d.get("ru") or d.get("t") or d.get("text") for d in data if isinstance(d, dict)}
    if not isinstance(data, dict):
        core.fail("Ожидался объект {id блока: перевод}.")
    tr = _load_tr(jdir)
    glossary = core.read_json(jdir / "tr" / "glossary.json", {})
    auto = core.read_json(jdir / "tr" / "autofill.json", {})
    issues = core.read_json(jdir / "tr" / "warnings.json", {})
    saved, unknown, warnings, bad_values, applied = 0, [], [], [], []
    for uid, ru in data.items():
        uid = str(uid)
        u = by_id.get(uid)
        if u is None:
            unknown.append(uid)
            continue
        if not isinstance(ru, str) or not ru.strip():
            bad_values.append(uid)
            continue
        ru = core.typo_ru(re.sub(r"\s+", " ", ru).strip())
        mark = len(warnings)
        src_plain, ru_plain = _strip_tags(u["text"]), _strip_tags(ru)
        src_idx = core.number_index(src_plain)
        missing, _minor = core.check_numbers(ru_plain, src_idx)
        if missing:
            warnings.append({"id": uid, "problem": "в переводе есть числа, которых нет в исходном блоке: %s" % ", ".join(missing)})
        ru_idx = core.number_index(ru_plain)
        lost = [t for t in core.find_number_tokens(src_plain) if not (core.number_forms(t) & ru_idx) and len(t) > 1]
        if lost:
            warnings.append({"id": uid, "problem": "в переводе пропали числа: %s" % ", ".join(lost[:6])})
        if u.get("rich") and "<b>" not in ru.lower():
            warnings.append({"id": uid, "problem": "в исходном блоке первая фраза выделена <b>…</b>, в переводе выделения нет"})
        if "<sup>" in u["text"].lower() and "<sup>" not in ru.lower():
            warnings.append({"id": uid, "problem": "в исходном блоке есть маркер сноски <sup>…</sup>, в переводе он потерян"})
        ru_body = re.sub(r"^(?:источник|source)\s*:.*$", "", ru_plain, flags=re.I).strip()
        ru_body = re.sub(r"(?<![A-Za-z])(?:[A-Z][A-Za-z0-9&.'-]*|[A-Z0-9&.-]{2,})(?![A-Za-z])", " ", ru_body)
        if len(ru_body) > 40 and _latin_share(ru_body) > 0.6:
            warnings.append({"id": uid, "problem": "перевод почти целиком латиницей — похоже, блок не переведён"})
        elif (_norm_src(ru_plain) == _norm_src(src_plain) and _needs_translation(src_plain)
              and re.search(r"(?<![A-Za-z])[a-z]{4,}", src_plain)):
            warnings.append({"id": uid, "problem": "перевод совпадает с исходным текстом — блок не переведён"})
        bad_words = _calques(ru_plain)
        if bad_words:
            warnings.append({"id": uid, "problem": "калька вместо русского слова: %s" % "; ".join(bad_words[:4])})
        src_left = src_plain.lower()
        for term, val in sorted(glossary.items(), key=lambda kv: -len(kv[0])):
            term_rx = re.compile(r"(?<![a-z])%s(?:e?s)?(?![a-z])" % re.escape(term.lower())) if term else None
            if term_rx and term_rx.search(src_left):
                src_left = term_rx.sub(" ", src_left)
                if term_rx.search(ru_plain.lower()):
                    continue
                ok, subst, label = _glossary_check(term, str(val), ru_plain, src_plain)
                if ok:
                    continue
                if subst:
                    if ru_plain[:1].isupper() and subst[:1].islower():
                        subst = subst[0].upper() + subst[1:]
                    new = "<b>%s</b>" % subst if "<b>" in ru.lower() else subst
                    applied.append({"id": uid, "was": ru_plain, "now": subst})
                    ru, ru_plain = new, subst
                    continue
                problem = "термин «%s» переведён не по словарю («%s»)" % (term, val)
                if label:
                    problem += ("; это подпись-ярлык: если словарная форма не помещается в рамку, добавьте краткую форму "
                                "в словарь — glossary --json '{\"%s\": \"%s (КРАТКО)\"}' — и сдайте блок заново" % (term, _glossary_forms(str(val))[0]))
                warnings.append({"id": uid, "problem": problem})
        tr[uid] = ru
        auto.pop(uid, None)
        saved += 1
        mine = [w["problem"] for w in warnings[mark:]]
        if mine:
            issues[uid] = mine
        else:
            issues.pop(uid, None)
        key = _norm_src(u["text"])
        for o in store["units"]:
            if o["id"] != uid and o["translate"] and _norm_src(o["text"]) == key and (o["id"] not in tr or o["id"] in auto):
                tr[o["id"]] = ru
                auto[o["id"]] = uid
    core.write_json(jdir / "tr" / "translations.json", tr)
    core.write_json(jdir / "tr" / "autofill.json", auto)
    core.write_json(jdir / "tr" / "warnings.json", issues)
    left = sum(1 for u in store["units"] if u["translate"] and u["id"] not in tr)
    resp = {"ok": True, "saved": saved, "left_untranslated": left, "warnings": warnings[:40]}
    if unknown:
        resp["unknown_ids"] = unknown[:20]
    if bad_values:
        resp["ignored_empty_or_non_text"] = bad_values[:20]
    if applied:
        resp["glossary_applied"] = applied[:30]
        resp["glossary_note"] = "В подписях-ярлыках подставлена словарная форма термина. Если в узкую рамку нужна краткая форма, добавьте её в словарь в скобках: {\"EVs\": \"электромобили (ЭМ)\"}."
    if warnings:
        resp["note"] = "Проверьте блоки из warnings и при необходимости сдайте их заново (put с тем же id перезаписывает перевод)."
    resp["next"] = ("Остались непереведённые блоки: translate.py extract %s" % args.job) if left else ("Всё переведено: translate.py build %s" % args.job)
    core.out(resp)


def cmd_glossary(args) -> None:
    jdir = core.job_dir(args.job)
    path = jdir / "tr" / "glossary.json"
    glossary = core.read_json(path, {})
    if args.json or args.file:
        data = core.load_payload(args, "словарь терминов")
        if not isinstance(data, dict):
            core.fail("Словарь — объект {термин: перевод}.")
        for k, v in data.items():
            k = str(k).strip()
            if len(k) < 2:
                continue
            if not isinstance(v, str) or not v.strip():
                glossary.pop(k, None)
            else:
                glossary[k[:80]] = v.strip()[:120]
        core.write_json(path, glossary)
    resp = {"ok": True, "glossary": glossary, "terms": len(glossary),
            "legend": "Значение — основная форма; краткие формы для узких подписей укажите в скобках через запятую: "
                      "{\"EVs\": \"электромобили (ЭМ)\", \"data centre\": \"ЦОД (центр обработки данных)\"}. put примет любую из форм, "
                      "а в подписи-ярлыке подставит подходящую сам."}
    weak = ["%s: %s" % (k, "; ".join(_calques(v))) for k, v in glossary.items() if _calques(v)]
    if weak:
        resp["warnings"] = weak[:20]
        resp["note"] = "В словаре кальки — замените их русскими словами (повторный glossary с тем же ключом перезаписывает перевод)."
    core.out(resp)


def _pages_pending_ocr(meta: dict) -> list[int]:
    return [p["n"] for p in meta.get("page_info", []) if p.get("kind") in ("scan", "broken", "mixed") and not p.get("ocr")]


def cmd_status(args) -> None:
    pymupdf = core.require_pymupdf()
    jdir = core.job_dir(args.job)
    store = load_units(pymupdf, jdir, core.Deadline(200))
    tr = _load_tr(jdir)
    meta = core.read_json(jdir / "meta.json", {})
    per_page = {}
    for u in store["units"]:
        if u["translate"]:
            a, b = per_page.get(u["page"], (0, 0))
            per_page[u["page"]] = (a + 1, b + (1 if u["id"] in tr else 0))
    todo = [p for p, (a, b) in sorted(per_page.items()) if b < a]
    total = sum(a for a, _ in per_page.values())
    done = sum(b for _, b in per_page.values())
    resp = {
        "ok": True, "pages_total": meta.get("pages_total"), "pages_indexed": store["pages_done"],
        "units_total": total, "units_translated": done,
        "pages_with_untranslated": todo[:80],
        "pages_without_text": [p["n"] for p in meta.get("page_info", [])
                               if p.get("kind") in ("scan", "broken") and not p.get("ocr")][:60],
        "pages_pending_ocr": _pages_pending_ocr(meta)[:60],
        "pages_ocr": [p["n"] for p in meta.get("page_info", []) if p.get("ocr")][:60],
        "translation_pdf": str(core.output_paths(jdir)["translation_pdf"]) if core.output_paths(jdir)["translation_pdf"].is_file() else None,
        "unresolved_warnings": [{"id": k, "problems": v} for k, v in core.read_json(jdir / "tr" / "warnings.json", {}).items()][:30],
    }
    if store.get("migrated"):
        resp["resegmented"] = dict(store["migrated"], note="Навык обновился и режет страницы на блоки точнее (целые абзацы, подписи, "
                                   "наклонный текст). Совпавшие переводы перенесены, id блоков новые; остальное доперевести: translate.py extract.")
    core.out(resp)


def _expand_rect(u: dict, others: list[dict], page_rect, text_left: float, text_right: float) -> tuple[list[float], str]:
    x0, y0, x1, y1 = u["bbox"]
    h = y1 - y0
    align = u["align"]
    single = u["n_lines"] == 1

    def v_overlap(o) -> bool:
        return min(y1, o["bbox"][3]) - max(y0, o["bbox"][1]) > 0.3 * h

    if single:
        right_nb = [o["bbox"][0] for o in others if o["bbox"][0] >= x1 - 1 and v_overlap(o)]
        left_nb = [o["bbox"][2] for o in others if o["bbox"][2] <= x0 + 1 and v_overlap(o)]
        gap_right = (min(right_nb) - x1) if right_nb else None
        hugging = gap_right is not None and gap_right < 3 * u["size"] and not left_nb and x0 > page_rect.width * 0.35
        if align == "right" or (align == "left" and hugging):
            align = "right"
            limit = (max(left_nb) + 8) if left_nb else text_left
            x0 = min(x0, max(limit, x0 - 0.8 * (x1 - x0)))
        elif align == "left":
            limit = (min(right_nb) - 8) if right_nb else text_right
            x1 = max(x1, limit)

    if align == "center" and u["n_lines"] <= 4:
        right_nb = [o["bbox"][0] for o in others if o["bbox"][0] >= x1 - 1 and v_overlap(o)]
        left_nb = [o["bbox"][2] for o in others if o["bbox"][2] <= x0 + 1 and v_overlap(o)]
        room_l = (x0 - max(left_nb)) / 2 - 1.5 if left_nb else 0.4 * (x1 - x0)
        room_r = (min(right_nb) - x1) / 2 - 1.5 if right_nb else 0.4 * (x1 - x0)
        grow = max(0.0, min(room_l, room_r, 0.6 * (x1 - x0)))
        x0, x1 = x0 - grow, x1 + grow

    floor = page_rect.y1 - 8
    mid = (y0 + y1) / 2
    for o in others:
        ox0, oy0, ox1, _oy1 = o["bbox"]
        if oy0 > mid and min(x1, ox1) - max(x0, ox0) > 2:
            gap = oy0 - y1
            floor = min(floor, oy0 - max(1.5, 0.35 * gap) if gap > 0 else y1)
    line_h = u["size"] * u["pitch"]
    if single and u["size"] < 12:
        cap = 0.25 * u["size"]
    else:
        cap = max(line_h * 1.5, 0.3 * h)
    extra = max(0.0, min(floor - y1, cap))
    return [x0, y0 - 0.5, x1 + 1.0, y1 + extra], align


def _rot_plan(page_units_: list[dict]) -> dict:
    plan: dict = {}
    rots = [u for u in page_units_ if u.get("rot")]
    for u in rots:
        mates = [v for v in rots if abs(v["rot"][0] - u["rot"][0]) < 0.05 and abs(v["rot"][1] - u["rot"][1]) < 0.05
                 and abs(v["size"] - u["size"]) < 0.6]
        length = lambda v: ((v["p1"][0] - v["p0"][0]) ** 2 + (v["p1"][1] - v["p0"][1]) ** 2) ** 0.5  # noqa: E731
        if len(mates) < 2:
            plan[u["id"]] = ("center", length(u) * 1.15)
            continue
        def spread(key):  # noqa: E306
            xs = [v[key][0] for v in mates]; ys = [v[key][1] for v in mates]
            return min(max(xs) - min(xs), max(ys) - min(ys))
        anchor = "end" if spread("p1") < spread("p0") else "start"
        plan[u["id"]] = (anchor, max(length(v) for v in mates) * 1.08)
    return plan


def _per_line(u: dict, rect: list[float]) -> int:
    return max(1, int((rect[2] - rect[0]) / (0.56 * u["size"] * 0.85)))


def _capacity(u: dict, rect: list[float]) -> int:
    size = u["size"] * 0.85
    per_line = max(1.0, (rect[2] - rect[0]) / (0.56 * size))
    lines = max(1, int((rect[3] - rect[1] + 0.6) // (size * u["pitch"])))
    return max(3, int(per_line * lines * 0.97))


_TAG_RE = re.compile(r"</?(?:b|i|sup)>", re.I)
GLUE = ("\x00", None, False)


def _strip_tags(text: str) -> str:
    return _TAG_RE.sub("", text)


class Typesetter:

    SCALES = [1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45, 0.4, 0.35, 0.3]

    def __init__(self, pymupdf):
        self.mu = pymupdf
        self.fonts = {
            (False, False): pymupdf.Font("helv"), (True, False): pymupdf.Font("hebo"),
            (False, True): pymupdf.Font("heit"), (True, True): pymupdf.Font("hebi"),
        }
        self.fallback = pymupdf.Font("cjk")
        self.fix = {id(self.fonts[(False, True)]): {"т": (-0.18, 0.47)},
                    id(self.fonts[(True, True)]): {"т": (-0.158, 0.50)}}

    def _pieces(self, text: str, key: tuple, sup: bool = False) -> list[tuple]:
        font = self.fonts[key]
        out, cur, cur_fb = [], "", False
        for ch in text:
            fb = not font.has_glyph(ord(ch)) and ch != core.NBSP
            if fb != cur_fb and cur:
                out.append((cur, self.fallback if cur_fb else font, sup))
                cur = ""
            cur_fb = fb
            cur += ch
        if cur:
            out.append((cur, self.fallback if cur_fb else font, sup))
        fix = self.fix.get(id(font))
        if fix:
            split = []
            for t, f, sp in out:
                if f is font and any(ch in fix for ch in t):
                    split.extend((part, f, sp) for part in re.split("(%s)" % "|".join(map(re.escape, fix)), t) if part)
                else:
                    split.append((t, f, sp))
            out = split
        return out

    SUP_SCALE, SUP_RAISE = 0.62, 0.33

    def adv(self, text: str, font, size: float, sup: bool = False) -> float:
        if font is None:
            return 0.0
        if sup:
            size *= self.SUP_SCALE
        fix = self.fix.get(id(font))
        if fix and text in fix:
            return fix[text][1] * size
        return font.text_length(text, size)

    def put(self, tw, x: float, y: float, text: str, font, size: float, sup: bool = False) -> float:
        if font is None:
            return x
        if sup:
            y -= self.SUP_RAISE * size
            size *= self.SUP_SCALE
        fix = self.fix.get(id(font))
        dx = fix[text][0] * size if fix and text in fix else 0.0
        tw.append((x + dx, y), text, font=font, fontsize=size)
        return x + self.adv(text, font, size)

    def chunks(self, ru: str, bold: bool, italic: bool) -> list[list[tuple]]:
        ru = ru.replace("\u202f", core.NBSP).replace("₽", "руб.")
        chunks: list[list[tuple]] = []
        cur: list[tuple] = []
        b, i, sup, pos = bold, italic, False, 0
        for m in list(_TAG_RE.finditer(ru)) + [None]:
            seg = ru[pos:m.start()] if m else ru[pos:]
            parts = re.split(r"( +)", seg)
            for part in parts:
                if not part:
                    continue
                if part.isspace() and core.NBSP not in part:
                    if cur:
                        chunks.append(cur)
                        cur = []
                else:
                    cur.extend(self._pieces(part, (b, i), sup))
            if m:
                tag = m.group(0).lower()
                on = not tag.startswith("</")
                if "sup" in tag:
                    sup = on
                elif "b" in tag:
                    b = on or bold
                else:
                    i = on or italic
                pos = m.end()
        if cur:
            chunks.append(cur)
        return chunks

    def _w(self, chunk: list[tuple], size: float) -> float:
        return sum(self.adv(text, font, size, sup) for text, font, sup in chunk)

    @staticmethod
    def _split_hyphen(chunk: list[tuple]) -> list[list[tuple]] | None:
        out, cur = [], []
        for text, font, sup in chunk:
            if font is None:
                continue
            parts = re.split(r"(?<=[^\W\d_][-‑])(?=[^\W\d_])", text)
            for k, part in enumerate(parts):
                if k:
                    out.append(cur)
                    cur = [GLUE]
                cur.append((part, font, sup))
        out.append(cur)
        return out if len(out) > 1 else None

    def attempts(self, max_scale: float = 1.0) -> list[tuple[float, bool]]:
        scales = [sc for sc in self.SCALES if sc <= max_scale + 1e-6]
        return [(sc, False) for sc in scales if sc >= 0.75] + [(sc, True) for sc in scales]

    def wrap(self, chunks: list, size: float, max_w: float, hyphen: bool = True) -> tuple[list, bool]:
        space = self.fonts[(False, False)].text_length(" ", size)
        lines, cur, cur_w, overflow = [], [], 0.0, False
        queue = list(chunks)
        while queue:
            ch = queue.pop(0)
            w = self._w(ch, size)
            glue = bool(ch) and ch[0] is GLUE
            if w > max_w + 0.5:
                sub = self._split_hyphen(ch) if hyphen else None
                if sub:
                    queue[0:0] = sub
                    continue
                overflow = True
            gap = 0.0 if (glue or not cur) else space
            if cur and cur_w + gap + w > max_w + 0.5:
                lines.append((cur, cur_w))
                cur, cur_w, gap = [], 0.0, 0.0
            cur_w += gap + w
            cur.append(ch)
        if cur:
            lines.append((cur, cur_w))
        return lines, overflow

    def fit(self, rect, ru: str, u: dict) -> float:
        font0 = self.fonts[(False, False)]
        chunks = self.chunks(ru, u["bold"], u["italic"])
        for scale, hyphen in self.attempts():
            size = u["size"] * scale
            lines, overflow = self.wrap(chunks, size, rect.width, hyphen)
            need = (len(lines) - 1) * size * u["pitch"] + (font0.ascender - font0.descender) * size
            if need <= rect.height + 0.6 and not overflow:
                return scale
        return self.SCALES[-1]

    def draw(self, page, rect, ru: str, u: dict, align: str, max_scale: float = 1.0) -> float:
        font0 = self.fonts[(False, False)]
        asc, desc = font0.ascender, font0.descender
        chunks = self.chunks(ru, u["bold"], u["italic"])
        if not chunks:
            return 1.0
        chosen = None
        for scale, hyphen in self.attempts(max_scale):
            size = u["size"] * scale
            lines, overflow = self.wrap(chunks, size, rect.width, hyphen)
            need = (len(lines) - 1) * size * u["pitch"] + (asc - desc) * size
            if (need <= rect.height + 0.6 and not overflow) or (scale == self.SCALES[-1] and hyphen):
                chosen = (scale, size, lines)
                break
        scale, size, lines = chosen
        space = font0.text_length(" ", size)
        color = tuple(int(u["color"][k:k + 2], 16) / 255 for k in (1, 3, 5))
        tw = self.mu.TextWriter(page.rect)
        y = rect.y0 + asc * size
        for line, line_w in lines:
            if align == "center":
                x = rect.x0 + (rect.width - line_w) / 2
            elif align == "right":
                x = rect.x1 - line_w
            else:
                x = rect.x0
            for n, chunk in enumerate(line):
                if n and not (chunk and chunk[0] is GLUE):
                    x += space
                for text, font, sup in chunk:
                    x = self.put(tw, x, y, text, font, size, sup)
            y += size * u["pitch"]
        tw.write_text(page, color=color)
        return scale


def _draw_rotated(pymupdf, ts: Typesetter, page, ru: str, u: dict, anchor: str, max_len: float) -> float:
    import math
    text = re.sub(r"\s+", " ", _strip_tags(ru)).strip()
    pieces = ts._pieces(text, (u["bold"], u["italic"]))
    scale, size, width = 1.0, u["size"], 0.0
    for scale in ts.SCALES:
        size = u["size"] * scale
        width = sum(ts.adv(t, font, size, sp) for t, font, sp in pieces)
        if width <= max_len:
            break
    dx, dy = u["rot"]
    if anchor == "end":
        sx, sy = u["p1"][0] - dx * width, u["p1"][1] - dy * width
    elif anchor == "start":
        sx, sy = u["p0"]
    else:
        mx, my = (u["p0"][0] + u["p1"][0]) / 2, (u["p0"][1] + u["p1"][1]) / 2
        sx, sy = mx - dx * width / 2, my - dy * width / 2
    color = tuple(int(u["color"][k:k + 2], 16) / 255 for k in (1, 3, 5))
    tw = pymupdf.TextWriter(page.rect)
    x = sx
    for t, font, sp in pieces:
        x = ts.put(tw, x, sy, t, font, size, sp)
    angle = math.degrees(math.atan2(dy, dx))
    tw.write_text(page, color=color, morph=(pymupdf.Point(sx, sy), pymupdf.Matrix(ROT_SIGN * angle)))
    return scale


ROT_SIGN = -1.0


def _paint_units(pymupdf, page, units: list[dict]) -> None:
    shape = page.new_shape()
    flat_any = False
    for u in units:
        for item in u["paint"]:
            quad = _inflate(item["quad"], 0.4)
            strip = item.get("strip")
            if strip and len(strip) >= 2:
                xs = [p[0] for p in quad]; ys = [p[1] for p in quad]
                rect = pymupdf.Rect(min(xs), min(ys), max(xs), max(ys))
                try:
                    samples = bytes(v for px in strip for v in px)
                    pix = pymupdf.Pixmap(pymupdf.csRGB, len(strip), 1, samples, False)
                    page.insert_image(rect, pixmap=pix, keep_proportion=False, overlay=True)
                    continue
                except Exception:
                    pass
            fill = tuple(int(item.get("bg", "#ffffff")[k:k + 2], 16) / 255 for k in (1, 3, 5))
            shape.draw_polyline([pymupdf.Point(*p) for p in quad])
            shape.finish(color=None, fill=fill, width=0, closePath=True)
            flat_any = True
    if flat_any:
        shape.commit()


def _inflate(quad: list, pad: float, pad_n: float | None = None) -> list:
    import math
    cx = sum(p[0] for p in quad) / 4; cy = sum(p[1] for p in quad) / 4
    ax, ay = quad[1][0] - quad[0][0], quad[1][1] - quad[0][1]
    ln = math.hypot(ax, ay) or 1.0
    dx, dy = ax / ln, ay / ln
    nx, ny = -dy, dx
    if pad_n is None:
        h = max(abs((quad[2][0] - quad[1][0]) * nx + (quad[2][1] - quad[1][1]) * ny), 1.0)
        pad_n = max(pad, 0.2 * h)
    out = []
    for px, py in quad:
        ox, oy = px - cx, py - cy
        a = ox * dx + oy * dy; b = ox * nx + oy * ny
        a += pad if a >= 0 else -pad
        b += pad_n if b >= 0 else -pad_n
        out.append((cx + a * dx + b * nx, cy + a * dy + b * ny))
    return out


def build_page(pymupdf, ts: Typesetter, page, units: list[dict], tr: dict) -> list[dict]:
    if page.rotation:
        page.remove_rotation()
    todo = [u for u in units if u["id"] in tr]
    report: list[dict] = []
    if not todo:
        return report
    for u in todo:
        if u.get("ocr"):
            continue
        for lb in u["lines"]:
            hh = lb[3] - lb[1]
            r = pymupdf.Rect(lb[0] - 0.5, lb[1] + 0.18 * hh, lb[2] + 0.5, lb[3] - 0.18 * hh)
            page.add_redact_annot(r, fill=False, cross_out=False)
        for cb in u.get("chars", []):
            if cb[2] - cb[0] < 0.4 or cb[3] - cb[1] < 0.4:
                continue
            mx, my = 0.22 * (cb[2] - cb[0]), 0.22 * (cb[3] - cb[1])
            page.add_redact_annot(pymupdf.Rect(cb[0] + mx, cb[1] + my, cb[2] - mx, cb[3] - my), fill=False, cross_out=False)
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
    painted = [u for u in todo if u.get("paint")]
    if painted:
        _paint_units(pymupdf, page, painted)
    flat = [u for u in units if not u.get("rot")]
    text_right = max([u["bbox"][2] for u in flat] + [page.rect.x1 * 0.6])
    text_left = min([u["bbox"][0] for u in flat] + [page.rect.x1 * 0.4])
    rot_plan = _rot_plan(units)
    for u in todo:
        if u.get("rot"):
            anchor, max_len = rot_plan.get(u["id"], ("center", 40.0))
            sc = _draw_rotated(pymupdf, ts, page, tr[u["id"]], u, anchor, max_len)
            if sc < 0.8:
                n = len(_strip_tags(tr[u["id"]]))
                report.append({"id": u["id"], "scale": round(sc, 2), "ru_chars": n,
                               "target_chars": max(3, min(n - 1, int(max_len / (0.56 * u["size"] * 0.85))))})
    todo = [u for u in todo if not u.get("rot")]
    plan = []
    for u in todo:
        box, align = _expand_rect(u, [o for o in flat if o is not u], page.rect, text_left, text_right)
        rect = pymupdf.Rect(*box)
        plan.append((u, rect, align, ts.fit(rect, tr[u["id"]], u)))
    group_scale: dict = {}
    for u, _rect, _align, sc in plan:
        if u["n_lines"] > 1 and sc >= 0.75:
            key = (round(u["size"], 1), u["bold"])
            group_scale[key] = min(group_scale.get(key, 1.0), sc)
    for u, rect, align, sc in plan:
        cap = group_scale.get((round(u["size"], 1), u["bold"]), 1.0) if u["n_lines"] > 1 else 1.0
        scale = ts.draw(page, rect, tr[u["id"]], u, align, max_scale=min(sc, cap))
        if sc < 0.8:
            n = len(_strip_tags(tr[u["id"]]))
            report.append({"id": u["id"], "scale": round(sc, 2), "ru_chars": n,
                           "target_chars": min(n - 1, _capacity(u, [rect.x0, rect.y0, rect.x1, rect.y1]))})
    return report


def _edge_colors(pymupdf, page):
    try:
        pix = page.get_pixmap(dpi=12, alpha=False)
    except Exception:
        return {}
    w, h = pix.width, pix.height
    if w < 4 or h < 4:
        return {}
    xs = [int(w * k / 6) for k in range(1, 6)]
    ys = [int(h * k / 6) for k in range(1, 6)]
    edges = {"top": [(x, 1) for x in xs], "bottom": [(x, h - 2) for x in xs],
             "left": [(1, y) for y in ys], "right": [(w - 2, y) for y in ys]}
    out = {}
    for name, pts in edges.items():
        cols = [pix.pixel(x, y)[:3] for x, y in pts]
        dark = [c for c in cols if min(c) < 235]
        if len(dark) >= 4:
            out[name] = tuple(sum(c[i] for c in cols) / len(cols) / 255 for i in range(3))
    return out


def cmd_build(args) -> None:
    pymupdf = core.require_pymupdf()
    jdir = core.job_dir(args.job)
    deadline = core.Deadline(220)
    store = load_units(pymupdf, jdir, deadline)
    meta = core.read_json(jdir / "meta.json", {})
    total = int(meta.get("pages_total", 0))
    if store["pages_done"] < total:
        core.out({"ok": True, "done": False, "next": "Разбор документа не закончен: повторите translate.py build."})
    tr = _load_tr(jdir)
    missing = [u["id"] for u in store["units"] if u["translate"] and u["id"] not in tr]
    if missing and not args.allow_missing:
        pages = sorted({int(m[1:].split("u")[0]) for m in missing})
        core.fail("Не переведено блоков: %d (страницы: %s)." % (len(missing), ", ".join(map(str, pages[:25]))),
                  "Допереведите: translate.py extract %s --pages %d-%d. Если пользователь согласен на частичный перевод — добавьте --allow-missing."
                  % (args.job, pages[0], pages[-1]))

    by_page: dict[int, list[dict]] = {}
    for u in store["units"]:
        by_page.setdefault(u["page"], []).append(u)

    tr_dir = jdir / "tr"
    work_path, prog_path, fit_path = tr_dir / "work.pdf", tr_dir / "progress.json", tr_dir / "fit.json"
    progress = core.read_json(prog_path, {}) if work_path.is_file() else {}
    fit_all = core.read_json(fit_path, {}) if progress else {}
    src = pymupdf.open(jdir / "source.pdf")
    work = pymupdf.open(work_path) if progress else pymupdf.open(jdir / "source.pdf")

    ts = Typesetter(pymupdf)
    interrupted = False
    for pno in range(1, total + 1):
        units = by_page.get(pno, [])
        sig = hashlib.sha256(repr([(u["id"], tr.get(u["id"])) for u in units]).encode("utf-8")).hexdigest()[:16]
        if progress.get(str(pno)) == sig:
            continue
        if str(pno) in progress:
            work.delete_page(pno - 1)
            work.insert_pdf(src, from_page=pno - 1, to_page=pno - 1, start_at=pno - 1)
        fit_all[str(pno)] = build_page(pymupdf, ts, work[pno - 1], units, tr)
        progress[str(pno)] = sig
        if deadline.expired():
            interrupted = pno < total
            break
    tmp_path = tr_dir / "work.tmp.pdf"
    work.save(tmp_path, garbage=1, deflate=True)
    work.close()
    os.replace(tmp_path, work_path)
    core.write_json(prog_path, progress)
    core.write_json(fit_path, fit_all)
    if interrupted:
        core.out({"ok": True, "done": False, "pages_ready": len(progress), "pages_total": total,
                  "next": "Время вызова на исходе: повторите translate.py build — сборка продолжится со следующей страницы."})

    if deadline.elapsed() > 110:
        core.out({"ok": True, "done": False, "pages_ready": len(progress), "pages_total": total,
                  "next": "Страницы готовы, осталась финальная сборка файла: повторите translate.py build."})

    work = pymupdf.open(work_path)
    banded = 0
    if args.paper == "a4":
        out_doc = pymupdf.open()
        for i in range(work.page_count):
            r = work[i].rect
            W, H = (A4[1], A4[0]) if r.width > r.height else A4
            k = min(W / r.width, H / r.height)
            w, h = r.width * k, r.height * k
            same_shape = abs(W / H - r.width / r.height) < 0.01
            edges = {} if same_shape else _edge_colors(pymupdf, work[i])
            banded += 1 if edges else 0
            page = out_doc.new_page(width=W, height=H)
            x_pad, y_pad = (W - w) / 2, (H - h) / 2
            if y_pad > 0.5:
                if "top" in edges:
                    page.draw_rect(pymupdf.Rect(0, 0, W, y_pad + 1), color=None, fill=edges["top"])
                if "bottom" in edges:
                    page.draw_rect(pymupdf.Rect(0, H - y_pad - 1, W, H), color=None, fill=edges["bottom"])
            if x_pad > 0.5:
                if "left" in edges:
                    page.draw_rect(pymupdf.Rect(0, 0, x_pad + 1, H), color=None, fill=edges["left"])
                if "right" in edges:
                    page.draw_rect(pymupdf.Rect(W - x_pad - 1, 0, W, H), color=None, fill=edges["right"])
            page.show_pdf_page(pymupdf.Rect(x_pad, y_pad, x_pad + w, y_pad + h), work, i)
    else:
        out_doc = work
    title = (meta.get("pdf_title") or meta.get("source_name") or "").strip()
    out_doc.set_metadata({"title": (title + " — перевод на русский").strip(" —"), "producer": core.SKILL_NAME})
    out_dir = jdir / "out"
    out_dir.mkdir(exist_ok=True)
    pdf_path = core.output_paths(jdir)["translation_pdf"]
    for legacy in (out_dir / "translation_ru.pdf",):
        if legacy.is_file() and legacy != pdf_path:
            legacy.unlink()
    try:
        out_doc.subset_fonts()
    except Exception:
        pass
    heavy = work_path.stat().st_size > 150_000_000
    out_doc.save(pdf_path, garbage=1 if heavy else 4, deflate=True)

    tight = [dict(x, page=int(p)) for p, rep in fit_all.items() for x in rep]
    tight.sort(key=lambda x: x["scale"])
    resp = {
        "ok": True, "done": True, "pdf": str(pdf_path), "file_name": pdf_path.name, "pages": total, "paper": args.paper,
        "units_translated": sum(1 for u in store["units"] if u["id"] in tr),
        "units_missing": len(missing),
        "pages_without_text": [p["n"] for p in meta.get("page_info", [])
                               if p.get("kind") in ("scan", "broken") and not p.get("ocr")][:60],
        "pages_ocr": [p["n"] for p in meta.get("page_info", []) if p.get("ocr")][:60],
        "tight_units": tight[:25], "tight_total": len(tight),
    }
    if banded:
        resp["paper_note"] = ("Исходные страницы не формата A4, и у %d из них фон «в обрез»: на листе A4 они получили поля в цвет кромки. "
                              "Если пользователю важнее вид, чем формат для печати, соберите с --paper source — страницы останутся исходного размера." % banded)
    issues = core.read_json(jdir / "tr" / "warnings.json", {})
    open_issues = [{"id": k, "problems": v} for k, v in issues.items() if k in tr]
    if open_issues:
        resp["unresolved_warnings"] = open_issues[:30]
        resp["unresolved_total"] = len(open_issues)
        resp["quality"] = "check_required"
    if resp["units_translated"] == 0:
        resp["warnings"] = ["В документе не нашлось текста для перевода (скан без распознавания, пустые страницы или текст уже на русском): "
                            "файл собран без изменений. Для сканов сначала pdf.py ocr."]
    elif resp["pages_without_text"]:
        resp.setdefault("warnings", []).append(
            "Страницы %s — сканы без распознавания, скопированы как есть. Чтобы перевести и их: pdf.py ocr %s, затем extract/put/build."
            % (resp["pages_without_text"][:20], args.job))
    if resp["pages_ocr"]:
        resp["ocr_note"] = ("Страницы %s переведены поверх картинки: исходные надписи закрашены цветом фона, русский текст набран сверху. "
                            "На пёстром фоне это заметно — посмотрите их через pdf.py render --translated и предупредите пользователя."
                            % resp["pages_ocr"][:20])
    if tight:
        resp["note"] = ("tight_units — блоки, где русский текст пришлось заметно уменьшить (scale < 0,8). "
                        "Сократите перевод примерно до target_chars знаков без потери смысла, сдайте через put и соберите снова. "
                        "Блоки со scale ≥ 0,65 обычно читаются нормально; ниже — исправьте обязательно.")
    if open_issues:
        resp["next"] = ("Сначала разберите unresolved_warnings: это замечания put, которые остались неисправленными (числа, непереведённые блоки, термины). "
                        "Исправьте блоки повторным put и соберите снова; если замечание ложное — скажите об этом пользователю при сдаче.")
    else:
        check = (resp["pages_ocr"][:3] or list(range(1, min(total, 3) + 1)))
        resp["next"] = ("Проверьте 2–3 страницы глазами: pdf.py render %s --pages %s --translated (если инструмент просмотра "
                        "доступен). Затем отдайте PDF пользователю под именем file_name: скопируйте его без изменений в папку файлов "
                        "пользователя (в ГигаАгенте — /data/user/Deliverables/, создайте её при необходимости) и отправьте копию — "
                        "новые версии платформы не прикладывают файлы из папки навыка; если скопировать нельзя — отправьте напрямую."
                        % (args.job, ",".join(map(str, check))))
    core.out(resp)


def main() -> None:
    core.setup_stdio()
    ap = core.JsonArgumentParser(prog="translate.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("extract"); p.add_argument("job"); p.add_argument("--pages"); p.add_argument("--all", action="store_true"); p.set_defaults(fn=cmd_extract)
    p = sub.add_parser("put"); p.add_argument("job"); p.add_argument("--json"); p.add_argument("--file"); p.set_defaults(fn=cmd_put)
    p = sub.add_parser("glossary"); p.add_argument("job"); p.add_argument("--json"); p.add_argument("--file"); p.set_defaults(fn=cmd_glossary)
    p = sub.add_parser("status"); p.add_argument("job"); p.set_defaults(fn=cmd_status)
    p = sub.add_parser("build"); p.add_argument("job"); p.add_argument("--paper", choices=["a4", "source"], default="a4")
    p.add_argument("--allow-missing", action="store_true"); p.set_defaults(fn=cmd_build)
    args = ap.parse_args()
    if not getattr(args, "fn", None):
        core.fail("Не указана команда.", "Доступно: extract, put, glossary, status, build.")
    args.fn(args)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        core.fail("Внутренняя ошибка translate.py: %s: %s" % (type(e).__name__, e))
