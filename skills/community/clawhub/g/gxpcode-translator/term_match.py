#!/usr/bin/env python3
"""
Gxpcode-translator: term matching via Aho-Corasick automaton.
Loads Gxpcode-dict.csv, builds automaton, scans text, outputs JSON.

Usage:
  python term_match.py "text to match"                 # from argument, stdout JSON
  echo "text" | python term_match.py                    # from stdin, stdout JSON
  python term_match.py --output result.json "text"      # write JSON to file (UTF-8, bypasses pipe encoding)
  echo "text" | python term_match.py --output out.json  # from stdin, write to file
"""

import csv, io, json, sys
from pathlib import Path

# Fix Windows GBK encoding: redirect stdout to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import ahocorasick

SKILL_DIR = Path(__file__).resolve().parent
CONFIG_PATH = SKILL_DIR / "config.json"


def get_dict_path():
    """Read dict_path from config.json, fallback to Gxpcode-dict.csv."""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8-sig") as f:
            cfg = json.load(f)
        path = cfg.get("dict_path", "Gxpcode-dict.csv")
        # Resolve relative paths against skill dir
        p = Path(path)
        if not p.is_absolute():
            p = SKILL_DIR / p
        return p
    return SKILL_DIR / "Gxpcode-dict.csv"


DICT_PATH = get_dict_path()


def _normalize_ws(s):
    """Collapse all whitespace to single spaces (handles CSV double-space entries)."""
    return " ".join(s.strip().split())


def load_terms():
    """Load terms from Gxpcode-dict.csv, sorted by en length descending (long-word priority)."""
    terms = []
    with open(DICT_PATH, "r", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            en = _normalize_ws(row.get("en", ""))
            cn = row.get("cn", "").strip()
            if en:
                terms.append((en, cn))
    terms.sort(key=lambda x: len(x[0]), reverse=True)
    return terms


def build_automaton(terms):
    """Build ahocorasick.Automaton from term list.
    Returns (automaton, term_set_lower, cn_map_lower)."""
    A = ahocorasick.Automaton()
    for idx, (en, cn) in enumerate(terms):
        A.add_word(en.lower(), (idx, en, cn))
    A.make_automaton()
    term_set = set(t[0].lower() for t in terms)
    cn_map = {t[0].lower(): t[1] for t in terms}
    return A, term_set, cn_map


def quick_check(text, term_set):
    """Fast pre-check: does text contain ANY term substring?
    Avoids iterating the automaton unnecessarily."""
    lower = text.lower()
    return any(t in lower for t in term_set)


def find_matches(text, automaton, term_set, cn_map):
    """Scan text with AC automaton, return deduped matches (long-word priority)."""
    # Normalize input text whitespace (aligns with dict normalization)
    text = _normalize_ws(text)
    if not quick_check(text, term_set):
        return []

    # Collect all hits from automaton
    lower_text = text.lower()
    raw = []
    for end_idx, (idx, en, cn) in automaton.iter(lower_text):
        start = end_idx - len(en) + 1
        raw.append((start, end_idx, en, cn))

    # Sort by start ascending, then length descending (long-word priority)
    raw.sort(key=lambda x: (x[0], -(x[1] - x[0] + 1)))

    # Interval dedup: skip if overlaps with any already-covered interval
    matches = []
    covered = set()
    for s, e, en, cn in raw:
        if any(
            (cs <= s < ce) or (cs < e <= ce) or (s <= cs and e >= ce)
            for cs, ce in covered
        ):
            continue
        covered.add((s, e))
        matches.append((s, e, en, cn))

    # Restore left-to-right order
    matches.sort(key=lambda x: x[0])
    return matches


def apply_placeholders(text, matches):
    """Replace matches with {{T001}}, {{T002}}... working right-to-left."""
    result = text
    pmap = []
    for i, (s, e, en, cn) in enumerate(reversed(matches)):
        pid = f"{{{{T{i+1:03d}}}}}"
        pmap.append((pid, en, cn))
        result = result[:s] + pid + result[e+1:]
    pmap.reverse()
    return result, pmap


def main():
    args = sys.argv[1:]

    # Parse --output <path> if present
    output_path = None
    if "--output" in args:
        idx = args.index("--output")
        if idx + 1 < len(args):
            output_path = args[idx + 1]
            args = args[:idx] + args[idx + 2:]
        else:
            print(json.dumps({"error": "--output requires a file path"}, ensure_ascii=False))
            sys.exit(1)

    if args:
        text = _normalize_ws(" ".join(args))
    else:
        text = _normalize_ws(sys.stdin.read().strip())

    if not text:
        result = {"error": "no input text"}
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
        else:
            print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)

    if not DICT_PATH.exists():
        result = {
            "error": f"dict not found: {DICT_PATH}",
            "matches": [],
            "placeholder_text": text,
        }
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
        else:
            print(json.dumps(result, ensure_ascii=False))
        sys.exit(0)

    terms = load_terms()
    automaton, term_set, cn_map = build_automaton(terms)
    matches = find_matches(text, automaton, term_set, cn_map)

    placeholder_text = text
    pmap = []
    if matches:
        placeholder_text, pmap = apply_placeholders(text, matches)

    result = {
        "source_text": text,
        "placeholder_text": placeholder_text,
        "matches": [
            {"start": s, "end": e, "en": en, "cn": cn} for s, e, en, cn in matches
        ],
        "placeholder_map": [
            {"pid": pid, "en": en, "cn": cn} for pid, en, cn in pmap
        ],
        "match_count": len(matches),
    }

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
