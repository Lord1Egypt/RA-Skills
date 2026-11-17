#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
localization-release-copilot :: deterministic extract + locale-aware diff.

Reads a SOURCE draft and one or more TARGET-language versions, extracts
numbers (locale-normalized), proper nouns, source attributions, and optional
glossary terms, then reports what the target dropped or changed.

The checker is LOCALE-AWARE: 8.3亿 == 830M, 117亿 == 11.7B, 1.5亿 == 150M
are treated as EQUIVALENT, not mismatches.

Outputs 01-extracted-claims.json (consumed by the LLM diff-matrix step).
"""
import argparse
import json
import re
import sys

# ---- magnitude normalization -------------------------------------------------
ZH_UNIT = {"亿": 1e8, "万": 1e4}
EN_UNIT = {"billion": 1e9, "b": 1e9, "million": 1e6, "m": 1e6,
           "thousand": 1e3, "k": 1e3, "亿": 1e8, "万": 1e4}


def extract_numbers(text):
    """Return list of dicts: raw, canonical (float), unit, span."""
    out = []
    # ZH: digits + optional space + 亿/万
    for m in re.finditer(r"(\d+(?:\.\d+)?)\s*(亿|万)", text):
        val = float(m.group(1)) * ZH_UNIT[m.group(2)]
        out.append({"raw": m.group(0), "canonical": val,
                    "unit": m.group(2), "lang": "zh"})
    # EN: optional $ + digits + optional space + B/M/K or words
    for m in re.finditer(r"(?:\$\s*)?(\d+(?:\.\d+)?)\s*(billion|million|thousand|b|m|k)\b",
                         text, re.IGNORECASE):
        unit = m.group(2).lower()
        val = float(m.group(1)) * EN_UNIT[unit]
        out.append({"raw": m.group(0), "canonical": val,
                    "unit": m.group(2), "lang": "en"})
    # plain integers / decimals that look like magnitudes (>=1000) or with %
    for m in re.finditer(r"(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)\s*%", text):
        out.append({"raw": m.group(0), "canonical": float(m.group(1).replace(",", "")),
                    "unit": "%", "lang": "any"})
    return out


def num_match(src_val, tgt_vals, rel_tol=0.02, abs_tol=1.0):
    for tv in tgt_vals:
        if abs(src_val - tv) <= max(abs_tol, rel_tol * max(abs(src_val), abs(tv))):
            return True
    return False


def extract_attributions(text):
    """Heuristic (org, year) tuples. Works for ZH '（Org, 2024）' and EN 'Org (2024)'."""
    tuples = []
    # ZH full-width or half-width paren with a year
    for m in re.finditer(r"[（(]([^（）()]{2,40}?),?\s*((?:19|20)\d{2})[）)]", text):
        org = m.group(1).strip()
        year = m.group(2)
        if org:
            tuples.append({"org": org, "year": year, "raw": m.group(0)})
    # EN: Capitalized Org immediately preceding a year in parens
    for m in re.finditer(r"([A-Z][A-Za-z0-9 .&]{2,30}?)\s*\(((?:19|20)\d{2})\)", text):
        tuples.append({"org": m.group(1).strip(), "year": m.group(2),
                       "raw": m.group(0)})
    # bare year tokens (to detect year presence even without org capture)
    years = re.findall(r"(?:19|20)\d{2}", text)
    return tuples, sorted(set(years))


def extract_entities(text):
    """Heuristic proper nouns: quoted phrases + Capitalized sequences (EN) + 【】/引号 terms (ZH)."""
    ents = set()
    # quoted / bracketed
    for m in re.finditer(r"[“\"'『【]([^”\"'』】]{2,40})[”\"'』】]", text):
        ents.add(m.group(1).strip())
    # EN capitalized sequences (2+ words, filter common sentence starts handled loosely)
    for m in re.finditer(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z0-9]+){1,4})\b", text):
        ents.add(m.group(1).strip())
    return sorted(ents)


def check_glossary(src, tgt, glossary):
    rows = []
    for g in glossary:
        st = g.get("source_term", "")
        tt = g.get("target_term", "")
        mand = g.get("mandatory", False)
        rows.append({
            "source_term": st,
            "target_term": tt,
            "mandatory": mand,
            "source_present": (st in src) if st else None,
            "target_present": (tt in tgt) if tt else None,
            "violation": bool(mand and tt and tt not in tgt),
        })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--targets", nargs="+", required=True)
    ap.add_argument("--labels", nargs="+", default=None)
    ap.add_argument("--glossary", default=None, help="optional JSON file of term pairs")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    def read(p):
        with open(p, encoding="utf-8") as f:
            return f.read()

    src = read(args.source)
    src_nums = extract_numbers(src)
    src_attr, src_years = extract_attributions(src)
    src_ents = extract_entities(src)

    glossary = []
    if args.glossary:
        glossary = json.load(open(args.glossary, encoding="utf-8"))

    files = {}
    number_diffs = []
    attr_diffs = []
    gloss_rows = []

    for i, tp in enumerate(args.targets):
        label = (args.labels[i] if args.labels and i < len(args.labels)
                 else f"target_{i+1}")
        tgt = read(tp)
        tgt_nums = extract_numbers(tgt)
        tgt_attr, tgt_years = extract_attributions(tgt)
        tgt_ents = extract_entities(tgt)
        tgt_vals = [n["canonical"] for n in tgt_nums]

        # number diff: source numbers not represented in target
        for sn in src_nums:
            if not num_match(sn["canonical"], tgt_vals):
                number_diffs.append({
                    "dimension": "number",
                    "source_raw": sn["raw"],
                    "source_canonical": sn["canonical"],
                    "target_label": label,
                    "target_found": False,
                    "note": "source number not found (locale-normalized) in target",
                })
        # attribution diff: org AND year must both survive; dropping either is P1
        for sa in src_attr:
            org_ok = sa["org"] in tgt
            year_ok = sa["year"] in tgt_years
            if not (org_ok and year_ok):
                attr_diffs.append({
                    "dimension": "attribution",
                    "source_raw": sa["raw"],
                    "target_label": label,
                    "org_found": org_ok,
                    "year_found": year_ok,
                    "note": ("source attribution fully missing in target"
                             if not org_ok and not year_ok else
                             "attribution partially missing — org may be a translated"
                             " form; LLM diff step must verify before flagging P1"),
                })
        if glossary:
            gloss_rows.extend([
                {**r, "target_label": label} for r in check_glossary(src, tgt, glossary)
            ])

        files[label] = {
            "path": tp,
            "numbers": tgt_nums,
            "attributions": tgt_attr,
            "years_present": tgt_years,
            "entities_count": len(tgt_ents),
        }

    result = {
        "source": {
            "path": args.source,
            "numbers": src_nums,
            "attributions": src_attr,
            "years_present": src_years,
            "entities": src_ents,
        },
        "targets": files,
        "number_diffs": number_diffs,
        "attribution_diffs": attr_diffs,
        "glossary_compliance": gloss_rows,
        "meta": {
            "locale_aware": True,
            "equivalent_examples": ["8.3亿==830M", "117亿==11.7B", "1.5亿==150M"],
        },
    }
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"wrote {args.output}")
    print(f"  source numbers: {len(src_nums)}  target files: {len(args.targets)}")
    print(f"  number diffs: {len(number_diffs)}  attribution diffs: {len(attr_diffs)}  "
          f"glossary violations: {sum(1 for r in gloss_rows if r.get('violation'))}")


if __name__ == "__main__":
    main()
