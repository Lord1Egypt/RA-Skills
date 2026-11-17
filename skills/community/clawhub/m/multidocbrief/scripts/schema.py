"""
Приведение ответа модели к схеме analysis.json и последняя страховка перед вёрсткой.

Локальные модели редко держат схему идеально: «Исходные факты» приходят строками вместо
объектов {text, refs}, ссылки вписаны прямо в текст («… [D2, стр. 3]»), «уверенность» —
«Высокая (два источника)», шаги рассуждения — одной строкой с нумерацией, поля названы
по-русски или вложены не туда. normalize_analysis() принимает всё это и возвращает JSON
строго по схеме, ничего не выдумывая: только переупаковка того, что модель уже написала.

autofix() — последняя страховка, когда исправления моделью не помогли: обрезка по лимитам
на границе предложения/слова, удаление ссылок на несуществующие документы, ограничение числа
пунктов. Используется, чтобы записка была выпущена всегда, а оставшиеся замечания —
показаны пользователю, а не уронили прогон.
"""
from __future__ import annotations

import copy
import json
import re

CONF_WORDS = (("выс", "высокая"), ("high", "высокая"), ("сред", "средняя"), ("med", "средняя"),
              ("moder", "средняя"), ("умерен", "средняя"), ("низ", "низкая"), ("low", "низкая"),
              ("гипот", "низкая"))
_UNIT_WORDS = r"(?:страница|страницы|стр\.?|с\.|слайд|слайды|лист|рис\.?|рисунок)"
# ссылка на источник: D2 · стр. 3 | D2, стр 3 | Д2 слайд 4 | D5
REF_TOKEN = re.compile(r"(?<![A-Za-zА-Яа-я0-9])[DДdд]\s?(\d{1,3})(?:\s*[·,.:\-–—]?\s*(" + _UNIT_WORDS +
                       r")\s*(\d+(?:[-–]\d+)?|«[^»]{1,40}»|\"[^\"]{1,40}\"|[\w\-]+))?(?![\w])")
# ссылки в скобках в конце/внутри текста: «… [D2 · стр. 3; D4]» или «(D1, слайд 2)»
REF_GROUP = re.compile(r"\s*[\[(]\s*((?:источник[и]?:?\s*)?[DДdд]\s?\d{1,3}[^\])]{0,80})[\])]", re.I)
_BULLET = re.compile(r"^\s*(?:[-•▪*·]+|\d{1,2}[.)]|[a-zа-я][.)])\s+", re.I)
_MD = re.compile(r"\*\*|__|`")


def _txt(v) -> str:
    """Любое значение → строка (числа, списки строк, объекты с полем text)."""
    if v is None:
        return ""
    if isinstance(v, str):
        return _MD.sub("", v).strip()
    if isinstance(v, bool):
        return ""
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, list):
        return " ".join(t for t in (_txt(x) for x in v) if t)
    if isinstance(v, dict):
        for k in ("text", "текст", "value", "content", "fact", "факт", "step", "шаг", "description", "описание"):
            if k in v:
                return _txt(v[k])
        return " ".join(t for t in (_txt(x) for x in v.values()) if t)
    return str(v).strip()


def _items(v) -> list:
    """Список пунктов: список как есть; строка — по строкам/нумерации; объект — его значения."""
    if v is None or v == "":
        return []
    if isinstance(v, list):
        return [x for x in v if x not in (None, "", [], {})]
    if isinstance(v, dict):
        vals = list(v.values())
        return vals if all(isinstance(x, (str, dict)) for x in vals) and len(vals) > 1 else [v]
    if isinstance(v, str):
        lines = [ln for ln in re.split(r"\n+|;\s*(?=\d{1,2}[.)]\s)|(?<=[.!?])\s+(?=\d{1,2}[.)]\s)", v) if ln.strip()]
        return lines or [v]
    return [v]


def _get(d: dict, *keys, default=None):
    """Значение по первому найденному ключу (без учёта регистра и пробелов/подчёркиваний).
    JSON, вложенный строкой ('{"text": …}'), разворачивается.
    """
    if not isinstance(d, dict):
        return default
    norm = {}
    for k, v in d.items():
        norm.setdefault(re.sub(r"[\s_\-]+", "", str(k).lower()), v)
    for k in keys:
        v = d.get(k)
        if v in (None, "", [], {}):
            v = norm.get(re.sub(r"[\s_\-]+", "", k.lower()))
        if v in (None, "", [], {}):
            continue
        if isinstance(v, str) and v.lstrip()[:1] in ("{", "["):
            try:
                v = json.loads(v)
            except ValueError:
                pass
        return v
    return default


def canon_ref(doc: str, unit: str | None = None, num: str | None = None) -> str:
    ref = f"D{int(doc)}"
    if unit and num:
        u = unit.lower()
        if u.startswith(("стр", "с.")):
            ref += f" · стр. {num}"
        elif u.startswith("слайд"):
            ref += f" · слайд {num}"
        elif u.startswith("рис"):
            ref += f" · рис. {num}"
        elif u.startswith("лист"):
            sheet = num.strip('«»"')
            ref += f" · лист «{sheet}»"
    return ref


def parse_refs(v) -> list[str]:
    """«D2, стр. 3; Д4» / ["D2 · стр. 3"] / [{"doc": "D2", "page": 3}] → ["D2 · стр. 3", "D4"]."""
    out: list[str] = []
    if v is None:
        return out
    if isinstance(v, dict):
        doc = _txt(_get(v, "doc", "id", "document", "документ", "source", "ref"))
        page = _txt(_get(v, "page", "стр", "страница"))
        slide = _txt(_get(v, "slide", "слайд"))
        m = re.search(r"\d+", doc)
        if m:
            out.append(canon_ref(m.group(0), "стр" if page else "слайд" if slide else None, page or slide or None))
        return out
    if isinstance(v, list):
        for x in v:
            out += parse_refs(x)
        return list(dict.fromkeys(out))
    for m in REF_TOKEN.finditer(str(v)):
        out.append(canon_ref(m.group(1), m.group(2), m.group(3)))
    return list(dict.fromkeys(out))


def split_text_refs(text: str) -> tuple[str, list[str]]:
    """Вынимает ссылки в скобках из текста: «Выручка 12 млрд [D4, стр. 2]» → («Выручка 12 млрд», ["D4 · стр. 2"])."""
    refs: list[str] = []

    def take(m):
        found = parse_refs(m.group(1))
        if found:
            refs.extend(found)
            return ""
        return m.group(0)

    clean = REF_GROUP.sub(take, text)
    clean = re.sub(r"\s{2,}", " ", clean).strip(" ;,")
    return clean, list(dict.fromkeys(refs))


def _norm_conf(raw: str) -> tuple[str, str]:
    """«Высокая (два источника)» → ("высокая", "два источника")."""
    low = raw.lower().strip()
    level = ""
    for key, val in CONF_WORDS:
        if low.startswith(key) or re.match(rf"^\W*{key}", low):
            level = val
            break
    if not level:
        for key, val in CONF_WORDS:
            if key in low[:20]:
                level = val
                break
    reason = ""
    m = re.match(r"^\s*\S+\s*(?:[—–\-:(,]\s*)(.+?)\)?\s*$", raw)
    if level and m:
        reason = m.group(1).strip(" .)")
    return level, reason


def normalize_analysis(data) -> dict:
    """Ответ модели (любой степени «кривизны») → dict строго по схеме analysis.json."""
    if isinstance(data, list) and data and isinstance(data[0], dict):
        data = data[0]
    if not isinstance(data, dict):
        data = {}
    # обёртка {"записка": {...}} / {"analysis": {...}}
    if not _get(data, "topics", "топики", "темы"):
        for v in data.values():
            if isinstance(v, dict) and _get(v, "topics", "топики", "темы"):
                data = {**data, **v}
                break
    meta_in = data.get("meta") if isinstance(data.get("meta"), dict) else {}
    meta = {k: v for k, v in meta_in.items() if isinstance(v, (str, int, float))}
    meta["title"] = _txt(_get(meta_in, "title", "заголовок") or _get(data, "title", "заголовок"))
    for k in ("focus", "date", "doc_type", "prepared_for", "footer_note"):
        if k in meta:
            meta[k] = _txt(meta[k])

    ov_in = _get(data, "overall", "общий_вывод", "общий вывод", "summary", default={})
    if not isinstance(ov_in, dict):
        ov_in = {"text": ov_in}
    kp_raw = _get(ov_in, "key_points", "keypoints", "тезисы", "points", "conditions", "условия") or []
    overall = {"text": _txt(_get(ov_in, "text", "текст", "conclusion", "вывод", "summary")),
               "key_points": [t for t in (_BULLET.sub("", _txt(x)) for x in _items(kp_raw)) if t]}

    topics_in = _get(data, "topics", "топики", "темы", default=[])
    if isinstance(topics_in, dict):
        topics_in = list(topics_in.values()) if all(isinstance(x, dict) for x in topics_in.values()) else [topics_in]
    topics = []
    for t in topics_in if isinstance(topics_in, list) else []:
        if isinstance(t, str):
            t = {"title": t}
        if not isinstance(t, dict):
            continue
        lg = _get(t, "logic", "логика", "логика_решения", "логика решения", default={})
        if not isinstance(lg, dict):
            lg = {"reasoning": lg}
        src = {**t, **lg}  # поля логики иногда кладут прямо в топик
        ev_out = []
        for e in _items(_get(src, "evidence", "facts", "факты", "исходные_факты", "исходные факты", default=[])):
            if isinstance(e, dict):
                text = _txt(_get(e, "text", "текст", "fact", "факт", "statement", "content"))
                refs = parse_refs(_get(e, "refs", "ref", "sources", "source", "источники", "источник"))
            else:
                text, refs = _txt(e), []
            text = _BULLET.sub("", text)
            text, inline = split_text_refs(text)
            refs = list(dict.fromkeys(refs + inline))
            if text:
                ev_out.append({"text": text, "refs": refs})
        reasoning = [t2 for t2 in (_BULLET.sub("", _txt(x)) for x in
                                   _items(_get(src, "reasoning", "steps", "ход_рассуждения", "ход рассуждения",
                                               "рассуждение", default=[]))) if t2]
        conf_raw = _txt(_get(src, "confidence", "уверенность", "confidence_level"))
        level, reason_inline = _norm_conf(conf_raw) if conf_raw else ("", "")
        logic = {
            "evidence": ev_out,
            "reasoning": reasoning,
            "conclusion": _txt(_get(src, "conclusion", "вывод", "итог")),
            "confidence": level or conf_raw.lower(),
            "confidence_reason": _txt(_get(src, "confidence_reason", "reason", "обоснование", "почему"))
            or reason_inline,
        }
        caveats = _txt(_get(src, "caveats", "оговорки", "limitations", "ограничения", "risks_of_conclusion"))
        if caveats:
            logic["caveats"] = caveats
        topics.append({"title": _BULLET.sub("", _txt(_get(t, "title", "name", "тема", "заголовок", "topic"))),
                       "summary": _txt(_get(t, "summary", "сводка", "описание", "description")),
                       "logic": logic})
    out = {"meta": meta, "overall": overall, "topics": topics}
    if isinstance(data.get("sources"), list):
        out["sources"] = [s for s in data["sources"] if isinstance(s, dict)]
    return out


# ======================================================================= последняя страховка
def _cut(text: str, limit: int) -> str:
    """Обрезка по границе предложения, иначе слова; многоточие — только если резали посреди фразы."""
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    head = text[:limit]
    end = max(head.rfind(". "), head.rfind("! "), head.rfind("? "), head.rfind("; "))
    if end >= limit * 0.6:
        return head[: end + 1].strip()
    sp = head[:limit - 1].rfind(" ")
    return (head[:sp] if sp > limit * 0.5 else head[:limit - 1]).rstrip(" ,;:—–-") + "…"


def autofix(data: dict, limits: dict, known_ids: set | None = None, doc_units: dict | None = None,
            shrink: float = 1.0) -> dict:
    """Детерминированно доводит записку до схемы. Ничего не придумывает: только режет и чистит."""
    a = copy.deepcopy(normalize_analysis(data))
    L = {k: (int(v * shrink) if isinstance(v, int) and not k.endswith(("_min", "_max")) else v)
         for k, v in limits.items()}
    a["meta"]["title"] = _cut(a["meta"].get("title") or "Аналитическая записка", L["title"])
    if a["meta"].get("focus"):
        a["meta"]["focus"] = _cut(a["meta"]["focus"], limits["focus"])
    ov = a["overall"]
    ov["text"] = _cut(ov["text"], L["overall.text"])
    ov["key_points"] = [_cut(k, L["overall.key_point"]) for k in ov["key_points"][: L["overall.key_points_max"]]]
    topics, seen = [], set()
    for t in a["topics"]:
        lg0 = t["logic"]
        if not (t["summary"] or lg0["evidence"] or lg0["conclusion"]) or t["title"].lower() in seen:
            continue
        seen.add(t["title"].lower())
        t["title"] = _cut(t["title"] or "Тема", L["topic.title"])
        t["summary"] = _cut(t["summary"], L["topic.summary"])
        lg = t["logic"]
        ev = lg["evidence"][: L["items_max"]]
        per = max(60, min(L["evidence.item"], L["evidence.total"] // max(1, len(ev))))
        for e in ev:
            e["text"] = _cut(e["text"], per)
            good = []
            for r in e["refs"]:
                m = re.match(r"D(\d+)", r)
                if not m or (known_ids is not None and f"D{m.group(1)}" not in known_ids):
                    continue
                doc = f"D{m.group(1)}"
                u = re.search(r"(стр\.|слайд)\s*(\d+)", r)
                if u and doc_units and doc in doc_units and int(u.group(2)) > int(doc_units[doc][1]):
                    r = doc  # номер страницы вне документа — оставляем ссылку на документ
                good.append(r)
            e["refs"] = list(dict.fromkeys(good))
        lg["evidence"] = ev
        rs = lg["reasoning"][: L["items_max"]]
        per = max(60, min(L["reasoning.step"], L["reasoning.total"] // max(1, len(rs))))
        lg["reasoning"] = [_cut(s, per) for s in rs]
        lg["conclusion"] = _cut(lg["conclusion"], L["conclusion"])
        if lg["confidence"] not in ("высокая", "средняя", "низкая"):
            lg["confidence"] = "средняя"
        lg["confidence_reason"] = _cut(lg["confidence_reason"], L["confidence_reason"])
        if lg.get("caveats"):
            lg["caveats"] = _cut(lg["caveats"], L["caveats"])
        topics.append(t)
    a["topics"] = topics[: L["topics_max"]]
    if isinstance(data, dict) and isinstance(data.get("sources"), list):
        a["sources"] = data["sources"]
    return a


def blocking_errors(data: dict) -> list[str]:
    """Без чего записку нельзя сверстать вовсе (всё остальное — замечания)."""
    a = normalize_analysis(data)
    errs = []
    if not a["overall"]["text"]:
        errs.append("нет общего вывода (overall.text)")
    filled = [t for t in a["topics"] if t["summary"] or t["logic"]["evidence"] or t["logic"]["conclusion"]]
    if not filled:  # пустые топики autofix отбрасывает; без единого содержательного топика записки нет
        errs.append("нет ни одного содержательного топика (topics)")
    return errs
