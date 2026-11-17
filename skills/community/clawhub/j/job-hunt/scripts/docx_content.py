"""Reject visible Markdown/LaTeX source in Word output, without rewriting facts.

Inspect paragraph text across runs, including tables, text boxes and page furniture.
Native Word equations use m:t, not w:t, and are deliberately left alone.
"""
from __future__ import annotations

import pathlib
import re
import xml.etree.ElementTree as ET
import zipfile


_W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
_PART = re.compile(r"word/(?:document|header\d*|footer\d*|footnotes|endnotes)\.xml$")
_PATTERNS = (
    ("Markdown emphasis", re.compile(r"(?<!\w)(?:\*\*(?=\S).+?(?<=\S)\*\*|__(?=\S).+?(?<=\S)__)(?!\w)")),
    ("Markdown italics", re.compile(r"(?<![\w*])\*(?![\s*])[^*\n]+(?<!\s)\*(?![\w*])|(?<![\w_])_(?![\s_])[^_\n]+(?<!\s)_(?![\w_])")),
    ("Markdown code", re.compile(r"`+[^`\n]+`+")),
    ("Markdown link", re.compile(r"!?\[[^\]\n]+\]\([^\n]+\)")),
    ("Markdown block", re.compile(r"^ {0,3}(?:#{1,6}\s+\S|[-*+]\s+\S|>\s+\S|`{3,}|~{3,})", re.M)),
    ("Markdown table", re.compile(r"^\s*\|?\s*:?-{3,}:?\s*\|\s*:?-{3,}:?", re.M)),
    ("LaTeX math", re.compile(r"\\\([\s\S]+?\\\)|\\\[[\s\S]+?\\\]|\$\$[\s\S]+?\$\$")),
    ("LaTeX command", re.compile(r"\\(?:text|textrm|textbf|textit|mathrm|mathbf|mathit|operatorname|frac|sqrt)\s*\{|\\(?:times|cdot|pm|leq?|geq?|neq|alpha|beta|gamma|delta|Delta|theta|sigma|sum|prod|int|infty|ldots)\b(?![\\/])")),
)
_INLINE_MATH = re.compile(r"(?<![\\$])\$(?!\$)([^\n$]+)(?<!\\)\$(?!\$)")


def markup_findings(text):
    """Conservative source-syntax checks; currency and code identifiers are prose."""
    findings = []
    for label, pattern in _PATTERNS:
        for match in pattern.finditer(text):
            # Python dunder names are identifiers, not unrendered bold text.
            if re.fullmatch(r"__[a-z][a-z0-9_]*__", match.group()):
                continue
            findings.append(f"{label}: {match.group()[:100]!r}")
    for match in _INLINE_MATH.finditer(text):
        formula = match.group(1)
        # Do not interpret "$100 and $200" or a plain price as a formula.
        if re.search(r"\\[A-Za-z]+|[\^_{}]|[A-Za-z0-9]\s*[=+*/]\s*[A-Za-z0-9]", formula):
            findings.append(f"LaTeX inline math: {match.group()[:100]!r}")
    return list(dict.fromkeys(findings))


def _xml_findings(parts):
    findings = []
    for name, xml in parts:
        root = ET.fromstring(xml)
        for number, paragraph in enumerate(root.iter(_W + "p"), 1):
            text = "".join(node.text or "" if node.tag == _W + "t" else
                           "\n" if node.tag in {_W + "br", _W + "cr"} else
                           "\t" if node.tag == _W + "tab" else ""
                           for node in paragraph.iter())
            for finding in markup_findings(text):
                findings.append(f"DOCX_MARKUP: {name} paragraph {number}: {finding}")
    return findings


class DocxMarkupError(ValueError):
    pass


def save_clean_docx(doc, out_path):
    """Check the actual Word text before saving; leave prior files untouched on failure."""
    parts = [(str(part.partname).lstrip("/"), part.blob)
             for part in doc.part.package.parts
             if _PART.fullmatch(str(part.partname).lstrip("/"))]
    findings = _xml_findings(parts)
    if findings:
        raise DocxMarkupError("\n".join(findings) +
                              "\nRepair the tailored source using plain text or native Word formatting; "
                              "re-render and review before delivery. Do not reuse an older export.")
    doc.save(str(out_path))


def docx_findings(path):
    """Inspect final bytes too: hand-edited or externally authored files can bypass renderers."""
    path = pathlib.Path(path)
    try:
        with zipfile.ZipFile(path) as archive:
            names = [name for name in archive.namelist() if _PART.fullmatch(name)]
            if "word/document.xml" not in names:
                return [f"DOCX_UNREADABLE: {path.name}: missing word/document.xml"]
            return [f"{path.name}: {finding}" for finding in
                    _xml_findings((name, archive.read(name)) for name in names)]
    except (OSError, zipfile.BadZipFile, ET.ParseError, RuntimeError) as exc:
        return [f"DOCX_UNREADABLE: {path.name}: {exc}"]
