#!/usr/bin/env python3
"""
Merge per-page translations into element-indexed JSON (translated.json).

Maps each paddleocr element 1:1 to its translation paragraph.
Handles cross-page continuations by detecting lowercase-start text elements
and inserting empty placeholders where the continuation was absorbed upstream.

Replaces the old translated.txt + split_paragraphs approach.
"""

import json, re, sys
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")


def is_continuation_el(el: dict) -> bool:
    """Detect if an element is a cross-page sentence continuation."""
    label = el.get("label", "")
    text = el.get("text", "").lstrip()
    if label in ("sec", "sub_sec", "sub_sub_sec", "title"):
        return False
    if text.startswith("<div") or text.startswith("<table"):
        return False
    # Text paragraph starting with lowercase → continuation from previous page
    if text and text[0].islower():
        return True
    return False


def split_page_translation(text: str) -> list:
    parts = [p.strip() for p in re.split(r"\n\s*\n|\n(?=#{1,3}\s)", text)]
    return [p for p in parts if p]


def backfill_continuations(elements: list) -> int:
    """Backfill empty continuation elements with parent element's Chinese translation.

    Scans empty-zh continuation elements in ascending index order (handles
    multi-hop chains). For each, walks backward to find the parent paragraph
    that was cut off mid-sentence (en doesn't end with '.'). If the parent
    has a non-empty zh, backfills it.
    """
    count = 0
    # Collect empty continuation elements, sorted ascending (chain-safe)
    empty = [
        i for i, el in enumerate(elements)
        if not el["zh"] and el.get("label") == "para"
    ]
    empty.sort()

    for idx in empty:
        parent = None
        for j in range(idx - 1, -1, -1):
            el = elements[j]
            if el.get("label") != "para":
                continue
            en = el["en"].strip()
            if not en:
                continue
            if en.endswith("."):
                continue  # complete sentence, not the parent
            parent = j
            break

        if parent is not None and elements[parent]["zh"]:
            elements[idx]["zh"] = elements[parent]["zh"]
            count += 1

    return count


def build_translated_json(elements_path: str, pages_dir: str, output_path: str):
    with open(elements_path, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    page_files = sorted(Path(pages_dir).glob("*_trans.md"))
    if not page_files:
        print(f"ERROR: No *_trans.md in {pages_dir}")
        sys.exit(1)

    # ── Integrity check (MANDATORY, cannot skip) ──
    total_pages = data.get("total_pages", len(data.get("pages", [])))
    existing_nums = set()
    empty_nums = []
    for pf in page_files:
        m = re.search(r'_p(\d+)_trans', pf.name)
        if m:
            pn = int(m.group(1))
            existing_nums.add(pn)
            if pf.stat().st_size < 10:
                empty_nums.append(pn)
    missing = sorted(set(range(1, total_pages + 1)) - existing_nums)
    all_bad = sorted(set(missing + empty_nums))
    if all_bad:
        print(f"INTEGRITY FAIL: {len(all_bad)} pages incomplete (missing={len(missing)}, empty={len(empty_nums)})")
        print(f"  Pages to retry: {all_bad}")
        retry_path = Path(output_path).parent / "_retry_pages.json"
        with open(retry_path, "w", encoding="utf-8") as f:
            json.dump(all_bad, f)
        print(f"  → _retry_pages.json written: {retry_path}")
        print(f"  → MAIN PROCESS: Read _retry_pages.json → re-spawn Agents for these pages → re-run merge")
        print(f"  → Max 2 retry rounds then report as unresolved.")
        sys.exit(2)
    print(f"Integrity PASS: {total_pages}/{total_pages} pages, all non-empty")

    # Load per-page translation paragraphs
    page_paras = {}
    for pf in page_files:
        m = re.search(r'_p(\d+)_trans', pf.name)
        if not m:
            continue
        pn = int(m.group(1))
        text = pf.read_text(encoding="utf-8-sig")
        page_paras[pn] = split_page_translation(text)

    output = []
    warnings = []
    global_idx = 0

    for page in data.get("pages", []):
        pn = page["page_number"]
        elements = page.get("elements", [])
        paras = page_paras.get(pn, [])

        # Identify continuation elements (text starts with lowercase)
        cont_indices = set()
        for i, el in enumerate(elements):
            if is_continuation_el(el):
                cont_indices.add(i)

        n_elem = len(elements)
        n_para = len(paras)
        gap = n_elem - n_para  # positive = paragraphs missing (continuations absorbed)
        para_i = 0
        remaining_gap = gap

        for i, el in enumerate(elements):
            label = el.get("label", "")
            en_text = el["text"]

            if i in cont_indices and remaining_gap > 0:
                # Continuation absorbed by previous page — insert empty placeholder
                zh_text = ""
                remaining_gap -= 1
                warnings.append({
                    "type": "continuation",
                    "idx": global_idx,
                    "page": pn,
                    "en": en_text[:80]
                })
            else:
                if para_i < n_para:
                    zh_text = paras[para_i]
                    para_i += 1
                else:
                    zh_text = ""
                    warnings.append({
                        "type": "missing",
                        "idx": global_idx,
                        "page": pn,
                        "en": en_text[:80]
                    })

            output.append({
                "index": global_idx,
                "en": en_text,
                "zh": zh_text,
                "label": label,
                "page": pn,
            })
            global_idx += 1

    # Post-process: backfill empty continuation elements with parent translation
    backfill_count = backfill_continuations(output)

    total = len(output)
    non_empty = sum(1 for o in output if o["zh"])
    print(f"Merged {total} elements, {non_empty} with translations ({total - non_empty} empty, {backfill_count} backfilled)")
    for w in warnings:
        t = w["type"]
        print(f"  [{t}] elem[{w['idx']}] p{w['page']}: \"{w['en']}\"")

    # ── Consolidated validation (④ element types + ⑤ table rows) ──
    from collections import defaultdict
    # ④ Element type distribution
    page_types_en = defaultdict(lambda: defaultdict(int))
    page_types_zh = defaultdict(lambda: defaultdict(int))
    for el in output:
        label = el.get("label", "unknown")
        p = el.get("page", 0)
        page_types_en[p][label] += 1
        if el["zh"].strip():
            page_types_zh[p][label] += 1
    type_issues = []
    for p in sorted(page_types_en.keys()):
        for label in page_types_en[p]:
            en_c = page_types_en[p][label]
            zh_c = page_types_zh[p][label]
            if en_c != zh_c:
                type_issues.append({"page": p, "label": label, "en_count": en_c, "zh_count": zh_c})
    # ⑤ Table row count
    row_issues = []
    for el in output:
        if el.get("label") in ("tab", "table"):
            en_tr = el["en"].count("<tr>")
            zh_tr = el["zh"].count("<tr>")
            if en_tr != zh_tr:
                row_issues.append({"index": el["index"], "page": el["page"], "en_rows": en_tr, "zh_rows": zh_tr})
    # Print & merge page lists
    fix_pages = set()
    if type_issues:
        print(f"\n⚠️  ELEMENT TYPE MISMATCH: {len(type_issues)} discrepancies")
        for ti in type_issues[:20]:
            print(f"  p{ti['page']} {ti['label']}: EN={ti['en_count']} ZH={ti['zh_count']}")
            fix_pages.add(ti["page"])
        if len(type_issues) > 20:
            print(f"  ... ({len(type_issues) - 20} more)")
    if row_issues:
        print(f"\n⚠️  TABLE ROW MISMATCH: {len(row_issues)} elements")
        for ri in row_issues:
            print(f"  elem[{ri['index']}] p{ri['page']}: EN={ri['en_rows']} rows, ZH={ri['zh_rows']} rows")
            fix_pages.add(ri["page"])
    # Write consolidated fix file
    if fix_pages:
        pages_sorted = sorted(fix_pages)
        fix_path = Path(output_path).parent / "_fix_pages.json"
        fix_data = {
            "pages_to_fix": pages_sorted,
            "type_mismatches": type_issues,
            "row_mismatches": row_issues
        }
        with open(fix_path, "w", encoding="utf-8") as f:
            json.dump(fix_data, f, ensure_ascii=False, indent=2)
        print(f"  → _fix_pages.json written: {fix_path}")
        print(f"  → Pages to fix: {pages_sorted}")
        return False  # repair loop needed
    else:
        print("✅ All validations passed (types + rows)")

    out = {
        "total_elements": total,
        "source_file": Path(elements_path).stem,
        "elements": output,
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"-> {output_path}")


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--elements", required=True)
    p.add_argument("--pages-dir", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    build_translated_json(args.elements, args.pages_dir, args.out)


if __name__ == "__main__":
    main()
