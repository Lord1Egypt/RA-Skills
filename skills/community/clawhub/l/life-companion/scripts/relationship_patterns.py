#!/usr/bin/env python3
"""
relationship_patterns.py — DETERMINISTIC cross-event pattern facts over the
relationship incidents the companion has already logged.

Why this exists: the relationships module names patterns ("this pursue-withdraw
loop again") as a reflective lens. That lens is only honest if it rests on the
*actual* record, not an impression. This script reads the per-person incident log
(`state/modules/relationships.yaml`, written by `companion.py cache --module
relationships`) and returns COUNTS AND DATES — a real base-rate — so the reading can
say "3 of your last 4 logged incidents share this tag" instead of guessing.

Honesty rules baked in (this is the computed layer; interpretation happens above it):
  * It only tallies tags YOU already logged (each incident's `lens`, plus the
    person-level `patterns`). It invents no new label and diagnoses nothing.
  * A pattern requires a tag shared by >= MIN_PATTERN_INCIDENTS (2) incidents.
    ONE incident is never a pattern — it is returned as `insufficient`, explicitly.
  * Synonym matching is literal (normalized token equality). "pursue-withdraw" and
    "一个追一个退" won't auto-merge; the reading connects those, not the script.
  * No perspective, no advice, no valence — just structure over the log.

Usage:
  python3 relationship_patterns.py [--home DIR] [--person NAME] --format json|text
  python3 relationship_patterns.py --selftest
"""
import argparse
import datetime
import json
import os
import re
import sys


if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _deps import ensure as _ensure  # noqa: E402

yaml = _ensure("PyYAML", "yaml")

MIN_PATTERN_INCIDENTS = 2   # a tag shared by fewer than this is NOT a pattern
_SPLIT = re.compile(r"[+/,;、，；]|\band\b|\+|&", re.IGNORECASE)


def home_dir(explicit=None):
    return os.path.abspath(
        explicit or os.environ.get("COMPANION_HOME") or os.path.expanduser("~/.companion")
    )


def _cache_path(home):
    return os.path.join(home, "state", "modules", "relationships.yaml")


def load_people(home, cache=None):
    """Return the {name: record} dict from the relationships cache (or {})."""
    if cache is None:
        path = _cache_path(home)
        if not os.path.exists(path):
            return {}
        with open(path, encoding="utf-8") as f:
            cache = yaml.safe_load(f) or {}
    return (cache or {}).get("people", {}) or {}


def _norm_tag(s):
    return re.sub(r"\s+", " ", str(s).strip().lower())


def _lens_tags(lens):
    """Split one incident's `lens` string into normalized tags. '' -> []."""
    if not lens:
        return []
    return [t for t in (_norm_tag(x) for x in _SPLIT.split(str(lens))) if t]


def _parse_date(s):
    try:
        return datetime.date.fromisoformat(str(s)[:10])
    except (ValueError, TypeError):
        return None


def _cadence(dates):
    """dates: sorted list of date objects. Returns cadence facts (gaps in days)."""
    if len(dates) < 2:
        return {"median_gap_days": None, "gaps": [], "trend": "n/a",
                "trend_note": "需要至少两条带日期的记录才能看间隔。"}
    gaps = [(dates[i + 1] - dates[i]).days for i in range(len(dates) - 1)]
    sg = sorted(gaps)
    n = len(sg)
    median = sg[n // 2] if n % 2 else (sg[n // 2 - 1] + sg[n // 2]) / 2.0
    trend, note = "steady", "间隔大致平稳。"
    if len(gaps) >= 3:  # need >=4 incidents to compare halves
        half = len(gaps) // 2
        first = sum(gaps[:half]) / half
        last = sum(gaps[half:]) / (len(gaps) - half)
        if last < first * 0.6:
            trend, note = "accelerating", "近期两次之间的间隔在变短(更密集了)。"
        elif last > first * 1.67:
            trend, note = "spacing-out", "近期间隔在拉长(变稀疏了)。"
    return {"median_gap_days": round(median, 1), "gaps": gaps, "trend": trend,
            "trend_note": note}


def _person_facts(rec):
    rec = rec or {}
    incidents = rec.get("incidents")
    # tolerate a hand-edited YAML where incidents is missing, null, or not a list of
    # dicts — a companion must not crash on a malformed store; skip junk entries.
    incidents = [i for i in incidents if isinstance(i, dict)] if isinstance(incidents, list) else []
    n = len(incidents)
    # tally lens tags across incidents, keeping the dates each appeared on
    tag_dates = {}
    for inc in incidents:
        d = inc.get("date")
        for tag in set(_lens_tags(inc.get("lens"))):  # set: one incident counts a tag once
            tag_dates.setdefault(tag, []).append(d)
    recurring = [{"tag": t, "count": len(ds), "dates": [x for x in ds if x]}
                 for t, ds in tag_dates.items() if len(ds) >= MIN_PATTERN_INCIDENTS]
    recurring.sort(key=lambda r: (-r["count"], r["tag"]))
    one_off = sorted(t for t, ds in tag_dates.items() if len(ds) < MIN_PATTERN_INCIDENTS)

    dates = sorted(d for d in (_parse_date(i.get("date")) for i in incidents) if d)
    span = None
    days_since = None
    if dates:
        span = {"first": dates[0].isoformat(), "last": dates[-1].isoformat(),
                "days": (dates[-1] - dates[0]).days}
        days_since = (datetime.date.today() - dates[-1]).days

    # honest confidence + base-rate sentence
    if n < MIN_PATTERN_INCIDENTS:
        conf = "insufficient"
        base = (f"只有 {n} 条记录 —— 不足以称为'模式',这只是{'一次' if n==1 else '零星'}事件。"
                "多记几次再看是否重复。")
    elif recurring and recurring[0]["count"] >= 3:
        conf = "pattern-level"
        top = recurring[0]
        base = (f"{n} 条记录中,『{top['tag']}』出现在 {top['count']} 次 —— "
                "这是日志里真实重复的主题(不是印象)。")
    else:
        conf = "tentative"
        if recurring:
            top = recurring[0]
            base = (f"『{top['tag']}』出现 {top['count']} 次(共 {n} 条)—— 是初步重复,"
                    "还偏薄;再多一两次才好确认。")
        else:
            base = f"{n} 条记录,暂无重复的标签 —— 更像各自独立的事件,而非单一模式。"

    return {
        "relationship": rec.get("relationship"),
        "incident_count": n,
        "date_span": span,
        "days_since_last": days_since,
        "recurring_lenses": recurring,          # count >= 2, base-rate present
        "one_off_lenses": one_off,              # appeared once
        "logged_patterns": rec.get("patterns") or [],
        "logged_tendencies": rec.get("tendencies") or [],
        "cadence": _cadence(dates),
        "confidence": conf,
        "base_rate_note": base,
    }


def scan(people, only=None):
    """people: {name: record}. Returns the full computed-facts payload."""
    out_people = {}
    # cross-person: which lens tags recur across >=2 DIFFERENT people
    tag_people = {}
    for name, rec in (people or {}).items():
        if only and name != only:
            continue
        facts = _person_facts(rec)
        out_people[name] = facts
        seen = set()
        incs = (rec or {}).get("incidents")
        for inc in (incs if isinstance(incs, list) else []):
            if isinstance(inc, dict):
                for tag in _lens_tags(inc.get("lens")):
                    seen.add(tag)
        for tag in seen:
            tag_people.setdefault(tag, set()).add(name)

    cross = [{"tag": t, "people": sorted(ps), "person_count": len(ps)}
             for t, ps in tag_people.items() if len(ps) >= 2]
    cross.sort(key=lambda c: (-c["person_count"], c["tag"]))

    return {
        "system": "relationship pattern scan (deterministic over logged incidents)",
        "as_of": datetime.date.today().isoformat(),
        "people": out_people,
        "cross_person_patterns": cross,
        "notes": ("只统计你已经记下的标签(每条 incident 的 lens + 人物层的 patterns);"
                  "不诊断、不新造标签。重复 >=2 次才算模式,1 次永远不算。同义词(如"
                  "『pursue-withdraw』与『一个追一个退』)不会自动合并——那是解读层的事。"),
    }


# --------------------------------------------------------------------- text view
def _text(r):
    L = [f"关系模式扫描（{r['as_of']} · 基于已记录事件的客观统计）"]
    if not r["people"]:
        L.append("  （还没有记录任何关系事件——先记几次，模式才谈得上。）")
        return "\n".join(L)
    for name, f in r["people"].items():
        head = f"\n▸ {name}" + (f"（{f['relationship']}）" if f.get("relationship") else "")
        L.append(head + f" · {f['incident_count']} 条记录 · 置信度：{f['confidence']}")
        if f["date_span"]:
            L.append(f"    跨度 {f['date_span']['first']}→{f['date_span']['last']}"
                     f"（{f['date_span']['days']} 天）· 距上次 {f['days_since_last']} 天")
        if f["recurring_lenses"]:
            L.append("    重复出现的标签（真实 base-rate）:")
            for rl in f["recurring_lenses"]:
                L.append(f"      · {rl['tag']} ×{rl['count']}")
        if f["cadence"]["median_gap_days"] is not None:
            L.append(f"    间隔中位数 {f['cadence']['median_gap_days']} 天 · {f['cadence']['trend_note']}")
        L.append("    " + f["base_rate_note"])
    if r["cross_person_patterns"]:
        L.append("\n跨对象重复的标签（同一模式出现在多个关系里）:")
        for c in r["cross_person_patterns"]:
            L.append(f"  · {c['tag']} —— {'、'.join(c['people'])}")
    L.append("\n" + r["notes"])
    return "\n".join(L)


# --------------------------------------------------------------------- selftest
def _selftest():
    ok = True

    def check(name, cond):
        nonlocal ok
        ok = ok and cond
        print(("  PASS " if cond else "  FAIL ") + name)

    check("lens split", _lens_tags("pursue-withdraw + defensiveness")
          == ["pursue-withdraw", "defensiveness"])
    check("lens split cjk sep", _lens_tags("回避、指责") == ["回避", "指责"])
    check("empty lens -> []", _lens_tags("") == [] and _lens_tags(None) == [])

    people = {
        "A": {"relationship": "girlfriend", "patterns": ["pursue-withdraw"],
              "tendencies": ["她焦虑偏高"],
              "incidents": [
                  {"date": "2026-05-01", "gist": "x", "lens": "pursue-withdraw + defensiveness"},
                  {"date": "2026-05-20", "gist": "y", "lens": "pursue-withdraw"},
                  {"date": "2026-06-02", "gist": "z", "lens": "pursue-withdraw + criticism"},
              ]},
        "B": {"relationship": "ex",
              "incidents": [{"date": "2026-01-10", "gist": "q", "lens": "pursue-withdraw"}]},
        "C": {"relationship": "friend", "incidents": []},
    }
    r = scan(people)
    a = r["people"]["A"]
    check("A counts 3", a["incident_count"] == 3)
    check("A recurring pursue-withdraw ×3",
          any(x["tag"] == "pursue-withdraw" and x["count"] == 3 for x in a["recurring_lenses"]))
    check("A one-offs are defensiveness+criticism",
          set(a["one_off_lenses"]) == {"defensiveness", "criticism"})
    check("A confidence pattern-level", a["confidence"] == "pattern-level")
    check("A span days 32", a["date_span"]["days"] == 32)
    check("A cadence has median", a["cadence"]["median_gap_days"] is not None)

    b = r["people"]["B"]
    check("B single incident -> insufficient", b["confidence"] == "insufficient")
    check("B no recurring (1 incident never a pattern)", b["recurring_lenses"] == [])
    check("B base-rate says too few", "不足以称为" in b["base_rate_note"])

    c = r["people"]["C"]
    check("C empty -> insufficient", c["confidence"] == "insufficient" and c["incident_count"] == 0)

    check("cross-person pursue-withdraw spans A & B",
          any(x["tag"] == "pursue-withdraw" and set(x["people"]) == {"A", "B"}
              for x in r["cross_person_patterns"]))

    # a 2-incident tentative case
    people2 = {"D": {"incidents": [
        {"date": "2026-03-01", "lens": "criticism"},
        {"date": "2026-03-15", "lens": "criticism"}]}}
    d = scan(people2)["people"]["D"]
    check("D 2x same tag -> tentative", d["confidence"] == "tentative")

    # --person filter
    only = scan(people, only="A")
    check("--person filter keeps only A", list(only["people"].keys()) == ["A"])

    # malformed store must degrade, never crash (companion robustness)
    malformed = {"N": None, "L": {"incidents": None}, "D": {"incidents": {"x": 1}},
                 "J": {"incidents": [None, "junk", {"lens": "criticism"}]}}
    try:
        rm = scan(malformed)
        check("malformed records don't crash", len(rm["people"]) == 4)
        check("junk incidents skipped, valid one kept",
              rm["people"]["J"]["incident_count"] == 1)
    except Exception:
        check("malformed records don't crash", False)

    print("SELFTEST:", "OK" if ok else "FAILURES")
    return ok


def main():
    ap = argparse.ArgumentParser(description="Deterministic relationship pattern facts")
    ap.add_argument("--home", default=None, help="override COMPANION_HOME")
    ap.add_argument("--person", default=None, help="scan only this tracked person")
    ap.add_argument("--format", choices=["json", "text"], default="json")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        raise SystemExit(0 if _selftest() else 1)
    home = home_dir(args.home)
    # Revoking relationships consent has to stop this read too. The records are about
    # someone else, and a "revoked" category that still gets analysed isn't revoked.
    consent = {}
    consent_path = os.path.join(home, "consent.yaml")
    if os.path.exists(consent_path):
        with open(consent_path, encoding="utf-8") as f:
            consent = yaml.safe_load(f) or {}
    entry = consent.get("relationships") if isinstance(consent, dict) else None
    if not (isinstance(entry, dict) and entry.get("granted") is True):   # a hand edit grants nothing
        refusal = {"ok": False,
                   "error": ("consent.relationships is not granted — relationship records "
                             "are withheld"),
                   "_next": ("Ask first: `companion.py consent --set relationships=yes` "
                             "restores access to anything stored; `companion.py forget "
                             "--relationships` deletes it.")}
        print(json.dumps(refusal, ensure_ascii=False, indent=2) if args.format == "json"
              else f"{refusal['error']}\n{refusal['_next']}")
        raise SystemExit(3)
    people = load_people(home)
    r = scan(people, only=args.person)
    print(_text(r) if args.format == "text" else json.dumps(r, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
