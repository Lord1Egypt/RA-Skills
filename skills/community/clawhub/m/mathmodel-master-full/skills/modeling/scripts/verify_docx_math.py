#!/usr/bin/env python3
"""Check whether a DOCX contains real Word equation objects.

This rejects shallow OMML where a plain code-like string is wrapped in
``m:oMath`` without actual math structure, such as ``t_ij`` or ``sum_k``.
"""

import argparse
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
}

LATEX_COMMAND_RE = re.compile(
    r"\\(?:frac|sum|int|prod|sqrt|alpha|beta|gamma|lambda|mu|sigma|theta|begin|end|left|right)\b"
)
CODELIKE_MATH_RE = re.compile(
    r"(?:[A-Za-z]\w*_[A-Za-z0-9]+|[A-Za-z]\w*\^[A-Za-z0-9]+|\bsum_[A-Za-z0-9]+|\bmin_[A-Za-z0-9]+|\bmax_[A-Za-z0-9]+|\|\|)"
)
STRUCTURAL_MATH_TAGS = {
    "f",
    "sSub",
    "sSup",
    "sSubSup",
    "nary",
    "d",
    "rad",
    "func",
    "limLow",
    "limUpp",
    "m",
    "eqArr",
    "bar",
    "acc",
    "groupChr",
    "borderBox",
}


def read_document_xml(docx_path: Path) -> str:
    with zipfile.ZipFile(docx_path) as zf:
        try:
            return zf.read("word/document.xml").decode("utf-8")
        except KeyError as exc:
            raise RuntimeError("word/document.xml not found; file may not be a valid DOCX") from exc


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def node_text(node: ET.Element) -> str:
    return "".join(child.text or "" for child in node.iter() if local_name(child.tag) == "t")


def has_structural_math(node: ET.Element) -> bool:
    return any(local_name(child.tag) in STRUCTURAL_MATH_TAGS for child in node.iter())


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify DOCX math objects.")
    parser.add_argument("docx", help="Path to .docx file")
    parser.add_argument("--min-equations", type=int, default=1, help="Minimum OMML equations expected")
    parser.add_argument("--allow-shallow", action="store_true", help="Allow simple OMML equations without structural math tags")
    args = parser.parse_args()

    docx_path = Path(args.docx)
    if not docx_path.exists():
        print(f"ERROR: file not found: {docx_path}", file=sys.stderr)
        return 2

    xml = read_document_xml(docx_path)
    root = ET.fromstring(xml)

    equations = root.findall(".//m:oMath", NS)
    text_nodes = [node.text or "" for node in root.findall(".//w:t", NS)]
    plain_text = "\n".join(text_nodes)
    math_texts = [node_text(node) for node in equations]
    math_plain_text = "\n".join(math_texts)
    latex_hits = sorted(set(LATEX_COMMAND_RE.findall(plain_text)))
    math_latex_hits = sorted(set(LATEX_COMMAND_RE.findall(math_plain_text)))
    code_like_math = [text for text in math_texts if CODELIKE_MATH_RE.search(text)]
    shallow_equations = [
        text for node, text in zip(equations, math_texts)
        if text.strip() and not has_structural_math(node)
    ]

    print(f"docx: {docx_path}")
    print(f"omml_equation_nodes: {len(equations)}")
    print(f"raw_latex_command_hits: {', '.join(latex_hits) if latex_hits else 'none'}")
    print(f"math_latex_command_hits: {', '.join(math_latex_hits) if math_latex_hits else 'none'}")
    print(f"code_like_math_texts: {len(code_like_math)}")
    print(f"shallow_omml_equations: {len(shallow_equations)}")

    failed = False
    if len(equations) < args.min_equations:
        print(f"ERROR: expected at least {args.min_equations} Word equation object(s).", file=sys.stderr)
        failed = True
    if latex_hits:
        print("ERROR: raw LaTeX commands appear in normal text nodes.", file=sys.stderr)
        failed = True
    if math_latex_hits:
        print("ERROR: raw LaTeX commands appear inside math text nodes.", file=sys.stderr)
        failed = True
    if code_like_math:
        examples = "; ".join(text[:80] for text in code_like_math[:3])
        print(f"ERROR: code-like math text appears inside equation objects: {examples}", file=sys.stderr)
        failed = True
    if shallow_equations and not args.allow_shallow:
        examples = "; ".join(text[:80] for text in shallow_equations[:3])
        print(f"ERROR: shallow OMML equation(s) lack real math structure: {examples}", file=sys.stderr)
        failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
