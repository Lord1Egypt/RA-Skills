#!/usr/bin/env python3
"""
Term Normalization Checker — paper-polisher v1.0.0
Check non-standard medical terminology against authority databases.

Usage:
    python3 term_check.py <input_file>
    python3 term_check.py <input_file> --output report.json
    python3 term_check.py <input_file> --auto-fix
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

LOCAL_JSON = Path(__file__).parent.parent / "data" / "terminology.json"

@dataclass
class TermIssue:
    original: str
    standard: str
    source: str
    position: int  # char offset
    context: str   # surrounding text snippet
    en_name: str = ""

@dataclass
class TermReport:
    file: str = ""
    total_issues: int = 0
    standardization_rate: float = 0.0  # percentage of terms that ARE standard
    issues: list = field(default_factory=list)
    summary: str = ""


def load_terminology() -> dict:
    """Load terms from local terminology.json (portable, no external dependencies)."""
    terms = {}
    
    if not LOCAL_JSON.exists():
        print(f"Error: terminology data not found at {LOCAL_JSON}", file=sys.stderr)
        return terms
    
    try:
        with open(LOCAL_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            cn_name = item["cn"]
            entry = {"standard": cn_name, "en": item.get("en", ""), "source": item.get("source", "")}
            terms[cn_name.lower()] = entry
            for alias in item.get("aliases", []):
                alias = alias.strip()
                if alias and len(alias) >= 2 and alias.lower() != cn_name.lower():
                    terms[alias.lower()] = entry
        print(f"Loaded {len(set(e['standard'] for e in terms.values()))} terms from local JSON", file=sys.stderr)
    except Exception as e:
        print(f"Error: Failed to load terminology: {e}", file=sys.stderr)
    
    return terms


def check_terms(text: str, terms_db: dict) -> TermReport:
    """Check text against terminology database by searching for all known terms."""
    
    if not terms_db:
        return TermReport(summary="术语库为空，无法检查。")
    
    # Get unique standard terms
    standard_terms = {}
    for key, entry in terms_db.items():
        std = entry["standard"]
        if std not in standard_terms:
            standard_terms[std] = entry
    
    issues = []
    standard_count = 0
    checked_positions = set()  # Avoid overlapping matches
    
    # Sort by length (longest first) to prefer longer matches
    sorted_terms = sorted(standard_terms.items(), key=lambda x: len(x[0]), reverse=True)
    
    for std_name, entry in sorted_terms:
        # Search for standard name in text
        positions = [m.start() for m in re.finditer(re.escape(std_name), text)]
        if positions:
            for pos in positions:
                # Check if this position is already covered by a longer match
                end = pos + len(std_name)
                if any(s <= pos < e or s < end <= e for s, e in checked_positions):
                    continue
                checked_positions.add((pos, end))
                standard_count += 1
    
    # Now search for non-standard names (aliases/short forms)
    for alias_lower, entry in terms_db.items():
        std_name = entry["standard"]
        if alias_lower == std_name.lower():
            continue  # Skip standard names (already counted)
        
        # Search for alias in text
        for m in re.finditer(re.escape(alias_lower), text, re.IGNORECASE):
            pos = m.start()
            end = pos + len(alias_lower)
            if any(s <= pos < e or s < end <= e for s, e in checked_positions):
                continue
            checked_positions.add((pos, end))
            
            context_start = max(0, pos - 15)
            context_end = min(len(text), end + 15)
            issues.append(TermIssue(
                original=text[pos:end],
                standard=std_name,
                source=entry["source"],
                position=pos,
                context=text[context_start:context_end],
                en_name=entry.get("en", "")
            ))
    
    total_known = standard_count + len(issues)
    rate = (standard_count / total_known * 100) if total_known > 0 else 0
    
    # Build summary
    if not issues:
        summary = f"✅ 术语检查通过。检测到 {standard_count} 个标准术语，无非标准用法。"
    else:
        lines = [f"发现 {len(issues)} 处非标准术语（标准率 {rate:.1f}%）："]
        for i, issue in enumerate(issues, 1):
            lines.append(f"  {i}. \"{issue.original}\" → 标准名: \"{issue.standard}\"（{issue.source}）")
            if issue.en_name:
                lines.append(f"     英文: {issue.en_name}")
        summary = "\n".join(lines)
    
    return TermReport(
        total_issues=len(issues),
        standardization_rate=round(rate, 1),
        issues=[asdict(i) for i in issues],
        summary=summary
    )


def auto_fix(text: str, issues: list) -> str:
    """Auto-replace non-standard terms with standard ones.
    
    Uses position-based replacement to avoid substring collisions:
    1. Sort issues by length (longest first)
    2. Find all match positions
    3. Replace from end to start to preserve indices
    4. Skip any matches that overlap with already-replaced regions
    """
    if not issues:
        return text
    
    # Sort by original length descending (longest match first)
    sorted_issues = sorted(issues, key=lambda x: len(x["original"]), reverse=True)
    
    # Collect all replacement regions: (start, end, standard)
    regions = []
    for issue in sorted_issues:
        original = issue["original"]
        standard = issue["standard"]
        start = 0
        while True:
            pos = text.find(original, start)
            if pos == -1:
                break
            # Check no overlap with existing regions
            end = pos + len(original)
            overlaps = any(not (end <= r[0] or pos >= r[1]) for r in regions)
            if not overlaps:
                regions.append((pos, end, standard))
            start = pos + 1
    
    # Sort regions by position descending (replace from end to preserve indices)
    regions.sort(key=lambda r: r[0], reverse=True)
    
    # Apply replacements
    result = text
    for start, end, standard in regions:
        result = result[:start] + standard + result[end:]
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Term Normalization Checker")
    parser.add_argument("input", help="Input text file")
    parser.add_argument("--output", help="Output JSON report file")
    parser.add_argument("--auto-fix", action="store_true", help="Auto-fix and output corrected text")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()

    terms_db = load_terminology()
    report = check_terms(text, terms_db)
    report.file = args.input

    if args.auto_fix and report.issues:
        fixed = auto_fix(text, report.issues)
        # Fixed text always goes to *_fixed.txt
        base = Path(args.input)
        fix_path = str(base.with_stem(base.stem + "_fixed"))
        with open(fix_path, "w", encoding="utf-8") as f:
            f.write(fixed)
        print(f"Auto-fixed {len(report.issues)} terms → {fix_path}")
    
    output_dict = asdict(report)
    
    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output_dict, f, ensure_ascii=False, indent=2)
        print(f"Report saved to {args.output}", file=sys.stderr)
    else:
        print(report.summary)


if __name__ == "__main__":
    main()
