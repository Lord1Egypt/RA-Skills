#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from pathlib import Path

from _common import parse_frontmatter, save_json, sectionized_lines, unique_preserve, write_text

INLINE_MATH_RE = re.compile(r"\$(?!\$)(.+?)(?<!\\)\$")
DISPLAY_MATH_RE = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
BRACKET_MATH_RE = re.compile(r"\\\[(.+?)\\\]", re.DOTALL)
GREEK = {
    r"\alpha", r"\beta", r"\gamma", r"\delta", r"\epsilon", r"\varepsilon", r"\zeta",
    r"\eta", r"\theta", r"\vartheta", r"\iota", r"\kappa", r"\lambda", r"\mu", r"\nu",
    r"\xi", r"\pi", r"\varpi", r"\rho", r"\sigma", r"\tau", r"\upsilon", r"\phi",
    r"\varphi", r"\chi", r"\psi", r"\omega", r"\Gamma", r"\Delta", r"\Theta", r"\Lambda",
    r"\Xi", r"\Pi", r"\Sigma", r"\Phi", r"\Psi", r"\Omega"
}
STOP = {
    "min", "max", "log", "exp", "sin", "cos", "tan", "det", "tr", "diag", "rank", "argmin",
    "argmax", "where", "text", "left", "right", "mathbf", "mathbb", "mathcal", "mathrm", "hat",
    "tilde", "bar", "frac", "sum", "prod", "int", "lim", "sup", "inf", "quad", "qquad"
}
DEFINITION_PATTERNS = [
    re.compile(r"\b(?P<sym>\\?[A-Za-z][A-Za-z0-9_{}^\\]*)\s+(?:denotes|is|are)\s+(?P<meaning>[^.;:]{3,120})", re.I),
    re.compile(r"\blet\s+(?P<sym>\\?[A-Za-z][A-Za-z0-9_{}^\\]*)\s+be\s+(?P<meaning>[^.;:]{3,120})", re.I),
    re.compile(r"\bdefine\s+(?P<sym>\\?[A-Za-z][A-Za-z0-9_{}^\\]*)\s+as\s+(?P<meaning>[^.;:]{3,120})", re.I),
    re.compile(r"\bfor\s+(?:each|every)\s+(?P<sym>\\?[A-Za-z][A-Za-z0-9_{}^\\]*)\s*,\s*(?P<meaning>[^.;:]{3,120})", re.I),
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Heuristically extract a notation table from paper markdown or text.")
    p.add_argument("input", help="Input markdown or plain-text file")
    p.add_argument("--output", default="", help="Markdown table output path")
    p.add_argument("--json-output", default="", help="Optional JSON output path")
    p.add_argument("--max-symbols", type=int, default=40, help="Maximum number of symbols to keep")
    p.add_argument("--min-count", type=int, default=2, help="Minimum symbol frequency to keep unless defined in prose")
    return p.parse_args()


def extract_math_blocks(text: str) -> list[str]:
    blocks = []
    blocks.extend(DISPLAY_MATH_RE.findall(text))
    blocks.extend(BRACKET_MATH_RE.findall(text))
    blocks.extend(INLINE_MATH_RE.findall(text))
    return blocks


def normalize_symbol(sym: str) -> str:
    sym = sym.strip()
    sym = re.sub(r"\\left|\\right", "", sym)
    sym = re.sub(r"\s+", "", sym)
    return sym


def candidate_symbols(expr: str) -> list[str]:
    out = []
    greek = re.findall(r"\\[A-Za-z]+", expr)
    out.extend([g for g in greek if g in GREEK])
    out.extend(re.findall(r"\b[A-Za-z](?:_[A-Za-z0-9]+|\^[A-Za-z0-9]+|_[{][^}]+[}]|\^[{][^}]+[}])?\b", expr))
    out.extend(re.findall(r"\b[A-Z][A-Z0-9]*\b", expr))
    cleaned = []
    for s in out:
        s = normalize_symbol(s)
        if not s:
            continue
        bare = s.lstrip("\\").split("_")[0].split("^")[0]
        if bare.lower() in STOP:
            continue
        if len(bare) == 1 and bare in {"e", "i"}:
            continue
        cleaned.append(s)
    return cleaned


def extract_definitions(text: str) -> dict[str, str]:
    meanings: dict[str, str] = {}
    for pat in DEFINITION_PATTERNS:
        for m in pat.finditer(text):
            sym = normalize_symbol(m.group("sym"))
            meaning = m.group("meaning").strip().rstrip(",")
            if sym and sym not in meanings and len(meaning.split()) >= 2:
                meanings[sym] = meaning
    return meanings


def first_section_for_symbol(md: str, symbols: list[str]) -> dict[str, str]:
    locations: dict[str, str] = {}
    lowered = {s: re.escape(s) for s in symbols}
    for sec, body in sectionized_lines(md):
        for sym in symbols:
            if sym in locations:
                continue
            pat = lowered[sym]
            if re.search(pat, body):
                locations[sym] = sec
    return locations


def build_table(md: str, max_symbols: int, min_count: int) -> tuple[list[dict], str]:
    blocks = extract_math_blocks(md)
    counts = Counter()
    for block in blocks:
        counts.update(candidate_symbols(block))

    meanings = extract_definitions(md)
    all_symbols = unique_preserve(list(meanings.keys()) + [s for s, c in counts.most_common() if c >= min_count])
    all_symbols = all_symbols[:max_symbols]
    sections = first_section_for_symbol(md, all_symbols)

    rows = []
    for sym in all_symbols:
        rows.append(
            {
                "symbol": sym,
                "meaning": meanings.get(sym, ""),
                "type_shape_domain": "",
                "units_scale": "",
                "first_appears_where": sections.get(sym, ""),
                "mentions": counts.get(sym, 0),
            }
        )

    md_lines = [
        "| Symbol | Meaning | Type / shape / domain | Units / scale | First appears where |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        md_lines.append(
            f"| {row['symbol']} | {row['meaning']} | {row['type_shape_domain']} | {row['units_scale']} | {row['first_appears_where']} |"
        )
    return rows, "\n".join(md_lines) + "\n"


def main() -> None:
    args = parse_args()
    md = Path(args.input).read_text(encoding="utf-8")
    _, md = parse_frontmatter(md)
    rows, table_md = build_table(md, max_symbols=args.max_symbols, min_count=args.min_count)

    if args.output:
        write_text(args.output, table_md)
    else:
        print(table_md)

    if args.json_output:
        save_json(args.json_output, {"notation_rows": rows})


if __name__ == "__main__":
    main()
