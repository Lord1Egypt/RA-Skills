#!/usr/bin/env python3
"""Deterministic lint hints for static prompt benchmarking."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


EXAMPLE_HEADINGS = re.compile(
    r"(?im)^\s*(?:#{1,6}\s*)?(?:example|examples|示例|例子|case|cases)"
    r"(?:\s*\d+)?\s*[:：]?"
)
INPUT_OUTPUT_PAIR = re.compile(
    r"(?is)(?:\binput\b|输入)\s*[:：].{0,2000}?(?:\boutput\b|输出)\s*[:：]"
)
PLACEHOLDER_PATTERNS = {
    "double_brace": re.compile(r"\{\{\s*[\w.-]+\s*\}\}"),
    "single_brace": re.compile(r"(?<![\{$])\{\s*[A-Za-z_][\w.-]*\s*\}(?!\})"),
    "dollar": re.compile(r"\$\{[\w.-]+\}"),
}


def issue(
    code: str,
    severity: str,
    message: str,
    evidence: str | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "code": code,
        "severity": severity,
        "message": message,
    }
    if evidence:
        result["evidence"] = evidence[:240]
    return result


def count_examples(text: str) -> dict[str, int]:
    heading_count = len(EXAMPLE_HEADINGS.findall(text))
    pair_count = len(INPUT_OUTPUT_PAIR.findall(text))
    conversation_pairs = min(
        len(re.findall(r"(?im)^\s*(?:user|用户)\s*[:：]", text)),
        len(re.findall(r"(?im)^\s*(?:assistant|助手)\s*[:：]", text)),
    )
    estimated = max(heading_count, pair_count, conversation_pairs)
    return {
        "estimated": estimated,
        "headings": heading_count,
        "input_output_pairs": pair_count,
        "conversation_pairs": conversation_pairs,
    }


def parse_fences(text: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Parse Markdown fenced blocks and return blocks plus structural findings."""
    findings: list[dict[str, Any]] = []
    blocks: list[dict[str, Any]] = []
    active: dict[str, Any] | None = None
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if not match:
            if active is not None:
                active["lines"].append(line)
            continue
        fence, suffix = match.groups()
        marker = fence[0]
        if active is None:
            active = {
                "marker": marker,
                "length": len(fence),
                "info": suffix.strip(),
                "start_line": line_number,
                "lines": [],
            }
            continue
        is_close = marker == active["marker"] and len(fence) >= active["length"] and not suffix.strip()
        if is_close:
            active["content"] = "\n".join(active.pop("lines"))
            active["end_line"] = line_number
            blocks.append(active)
            active = None
        else:
            active["lines"].append(line)
    if active is not None:
        findings.append(
            issue(
                "unbalanced-code-fence",
                "major",
                f"Code fence opened at line {active['start_line']} is not closed.",
            )
        )
        active["content"] = "\n".join(active.pop("lines"))
        active["end_line"] = None
        blocks.append(active)
    return blocks, findings


def lint_fences(text: str) -> list[dict[str, Any]]:
    return parse_fences(text)[1]


def lint_xml(text: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    # Ignore fenced and inline code while checking structural tags.
    blocks, _ = parse_fences(text)
    lines = text.splitlines()
    for block in reversed(blocks):
        start = block["start_line"] - 1
        end = block["end_line"] or len(lines)
        lines[start:end] = [""] * (end - start)
    text = "\n".join(lines)
    text = re.sub(r"`[^`\n]+`", "", text)
    tag_re = re.compile(r"<(/?)([A-Za-z][\w:.-]*)(?:\s[^<>]*?)?(/?)>")
    stack: list[str] = []
    ignored = {"br", "hr", "img", "input", "meta", "link"}
    for match in tag_re.finditer(text):
        closing, name, self_closing = match.groups()
        lower = name.lower()
        if lower in ignored or self_closing:
            continue
        if not closing:
            stack.append(name)
        elif not stack or stack[-1] != name:
            findings.append(
                issue(
                    "xml-nesting",
                    "major",
                    f"XML-like closing tag </{name}> does not match the current open tag.",
                    match.group(0),
                )
            )
        else:
            stack.pop()
    if stack:
        findings.append(
            issue(
                "xml-unclosed",
                "major",
                "XML-like tags appear unclosed.",
                ", ".join(stack[-5:]),
            )
        )
    return findings


def lint_json_blocks(text: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    blocks, _ = parse_fences(text)
    json_blocks = [
        block
        for block in blocks
        if block["info"] and block["info"].split(None, 1)[0].lower() == "json"
    ]
    for index, block in enumerate(json_blocks, start=1):
        try:
            json.loads(block["content"])
        except json.JSONDecodeError as exc:
            findings.append(
                issue(
                    "invalid-json-example",
                    "major",
                    f"JSON code block {index} is not parseable: {exc.msg} at line {exc.lineno}, column {exc.colno}.",
                    block["content"].strip(),
                )
            )
    return findings


def lint_conflicts(text: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    strict_json = re.search(
        r"(?is)(?:only\s+(?:output|return)|(?:output|return)\s+only|仅输出|只输出)"
        r".{0,30}?(?:valid\s+)?json|"
        r"(?:json).{0,30}(?:不要|不得|without|no)\s*(?:额外|additional|explanation|解释|text|文本)",
        text,
    )
    explanation = None
    explanation_pattern = re.compile(r"(?i)(?:explain|explanation|reasoning|解释|说明|理由|分析过程)")
    negative_pattern = re.compile(
        r"(?i)(?:do\s+not|don't|must\s+not|without|no|不要|不得|禁止|无需|不需要).{0,30}$"
    )
    for candidate in explanation_pattern.finditer(text):
        prefix = text[max(0, candidate.start() - 40) : candidate.start()]
        if not negative_pattern.search(prefix):
            explanation = candidate
            break
    if strict_json and explanation:
        excerpt_start = min(strict_json.start(), explanation.start())
        excerpt_end = min(len(text), max(strict_json.end(), explanation.end()) + 100)
        findings.append(
            issue(
                "possible-json-text-conflict",
                "moderate",
                "Possible conflict between JSON-only output and a request for explanatory text. Confirm whether explanations belong inside the JSON schema.",
                text[excerpt_start:excerpt_end].strip(),
            )
        )
    return findings


def lint_placeholders(text: str) -> tuple[dict[str, int], list[dict[str, Any]]]:
    counts = {name: len(pattern.findall(text)) for name, pattern in PLACEHOLDER_PATTERNS.items()}
    opening_tags = re.findall(r"<([A-Z][A-Z0-9_-]*)>", text)
    closing_tags = set(re.findall(r"</([A-Z][A-Z0-9_-]*)>", text))
    counts["angle"] = sum(1 for name in opening_tags if name not in closing_tags)
    active = [name for name, count in counts.items() if count]
    findings: list[dict[str, Any]] = []
    if len(active) > 1:
        findings.append(
            issue(
                "mixed-placeholders",
                "minor",
                f"Multiple placeholder syntaxes detected: {', '.join(active)}. Confirm that each syntax is intentional.",
            )
        )
    return counts, findings


def lint_text(text: str) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    findings.extend(lint_fences(text))
    findings.extend(lint_xml(text))
    findings.extend(lint_json_blocks(text))
    findings.extend(lint_conflicts(text))
    placeholders, placeholder_findings = lint_placeholders(text)
    findings.extend(placeholder_findings)

    repeated_lines: list[str] = []
    seen: set[str] = set()
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if len(line) < 30:
            continue
        normalized = re.sub(r"\s+", " ", line).lower()
        if normalized in seen and line not in repeated_lines:
            repeated_lines.append(line)
        seen.add(normalized)
    if repeated_lines:
        findings.append(
            issue(
                "duplicate-lines",
                "minor",
                f"{len(repeated_lines)} repeated substantial line(s) detected.",
                repeated_lines[0],
            )
        )

    return {
        "benchmark_type": "static_lint",
        "characters": len(text),
        "words_approx": len(re.findall(r"\S+", text)),
        "lines": len(text.splitlines()),
        "examples": count_examples(text),
        "placeholders": placeholders,
        "findings": findings,
        "finding_counts": {
            severity: sum(1 for item in findings if item["severity"] == severity)
            for severity in ("critical", "major", "moderate", "minor")
        },
        "note": "Heuristic findings require semantic confirmation; this is not a complete benchmark score.",
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Static Prompt Lint",
        "",
        f"- Characters: {report['characters']}",
        f"- Lines: {report['lines']}",
        f"- Estimated examples: {report['examples']['estimated']}",
        f"- Findings: {len(report['findings'])}",
        "",
    ]
    if not report["findings"]:
        lines.append("No deterministic lint findings. Semantic evaluation is still required.")
    else:
        for finding in report["findings"]:
            lines.extend(
                [
                    f"## [{finding['severity'].upper()}] {finding['code']}",
                    "",
                    finding["message"],
                ]
            )
            if finding.get("evidence"):
                lines.extend(["", f"Evidence: `{finding['evidence']}`"])
            lines.append("")
    lines.append(f"> {report['note']}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Prompt file path, or - for stdin")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.input == "-":
        text = sys.stdin.read()
    else:
        try:
            text = Path(args.input).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
    report = lint_text(text)
    if args.format == "markdown":
        print(render_markdown(report))
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
