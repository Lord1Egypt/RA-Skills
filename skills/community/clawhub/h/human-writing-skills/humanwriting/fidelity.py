from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from difflib import SequenceMatcher
from pathlib import Path

from .protection import ProtectionReport, compare_protected_content, extract_protected_items


CLAIM_END = re.compile(r"[。！？!?；;]|(?<!\d)\.(?!\d)|\n+")
SIGNALS = {
    "negation": re.compile(r"不|未|无|没有|并非|否认|\b(?:not|no|never|without)\b|\b(?:non|ne|pas|sem|não|sin|não|kein)\b|ない|ず|ليس|لم|لا", re.I),
    "uncertainty": re.compile(r"可能|或许|也许|疑似|尚不确定|\b(?:may|might|could|perhaps|possible|possibly|peut|pourrait|quizá|podría|pode|talvez)\b|かもしれない|可能性|قد|ربما", re.I),
    "scope": re.compile(r"仅|只|部分|全部|所有|\b(?:only|some|all|solely|limited to|seulement|uniquement|solo|apenas|somente)\b|のみ|だけ|فقط|جميع", re.I),
    "attribution": re.compile(r"据|表示|称|报告称|\b(?:according to|reported|said|selon|según|segundo)\b|によると|によれば|بحسب|وفق", re.I),
}
ACTOR = re.compile(r"[A-Za-zＡ-Ｚ][组組]|(?:group|groupe|grupo)\s+[A-Za-zＡ-Ｚ]|第[一二三四五六七八九十\d]+组", re.I)


@dataclass(frozen=True)
class FidelityFinding:
    kind: str
    source_start: int | None
    candidate_start: int | None
    source_line: int | None
    candidate_line: int | None
    source_excerpt: str
    candidate_excerpt: str
    detail: str


@dataclass(frozen=True)
class FidelityReport:
    status: str
    literal: ProtectionReport
    findings: tuple[FidelityFinding, ...]
    disclaimer: str = (
        "Only identical text is verified automatically. Changed prose needs a claim-by-claim "
        "human or model review; matching numbers and citations cannot prove semantic fidelity."
    )

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "literal": self.literal.to_dict(),
            "findings": [asdict(item) for item in self.findings],
            "disclaimer": self.disclaimer,
        }


def _claims(text: str) -> list[tuple[int, str]]:
    claims: list[tuple[int, str]] = []
    start = 0
    for match in CLAIM_END.finditer(text):
        part = text[start : match.end()]
        if part.strip():
            claims.append((start, part))
        start = match.end()
    if text[start:].strip():
        claims.append((start, text[start:]))
    return claims


def _line(text: str, start: int | None) -> int | None:
    return text.count("\n", 0, start) + 1 if start is not None else None


def _excerpt(value: str) -> str:
    return " ".join(value.split())[:240]


def compare_fidelity(source: str, candidate: str, terms: list[str] | None = None) -> FidelityReport:
    literal = compare_protected_content(source, candidate, terms)
    if source == candidate:
        return FidelityReport("pass-exact", literal, ())

    source_claims = _claims(source)
    candidate_claims = _claims(candidate)
    findings: list[FidelityFinding] = []
    matcher = SequenceMatcher(
        None,
        [part.strip() for _, part in source_claims],
        [part.strip() for _, part in candidate_claims],
        autojunk=False,
    )
    for tag, a, b, c, d in matcher.get_opcodes():
        if tag == "equal":
            continue
        left = "".join(part for _, part in source_claims[a:b])
        right = "".join(part for _, part in candidate_claims[c:d])
        source_start = source_claims[a][0] if a < b else None
        candidate_start = candidate_claims[c][0] if c < d else None
        findings.append(FidelityFinding(
            "changed-claim-span", source_start, candidate_start,
            _line(source, source_start), _line(candidate, candidate_start),
            _excerpt(left), _excerpt(right),
            "Meaning is unverified; compare actor, polarity, uncertainty, scope, attribution, and source support.",
        ))

    shared_anchors = {
        item.value for item in extract_protected_items(source, terms)
        if item.kind in {"number", "citation", "explicit-term"}
    } & {
        item.value for item in extract_protected_items(candidate, terms)
        if item.kind in {"number", "citation", "explicit-term"}
    }
    for anchor in sorted(shared_anchors):
        source_matches = [(start, part) for start, part in source_claims if anchor in part]
        candidate_matches = [(start, part) for start, part in candidate_claims if anchor in part]
        if len(source_matches) != 1 or len(candidate_matches) != 1:
            continue
        source_start, left = source_matches[0]
        candidate_start, right = candidate_matches[0]
        if left == right:
            continue
        changes = [
            name for name, pattern in SIGNALS.items()
            if {match.group(0).casefold() for match in pattern.finditer(left)}
            != {match.group(0).casefold() for match in pattern.finditer(right)}
        ]
        left_actors = set(ACTOR.findall(left))
        right_actors = set(ACTOR.findall(right))
        if left_actors != right_actors and (left_actors or right_actors):
            changes.append("actor")
        if changes:
            findings.append(FidelityFinding(
                "anchored-signal-change", source_start, candidate_start,
                _line(source, source_start), _line(candidate, candidate_start),
                _excerpt(left), _excerpt(right),
                f"Shared anchor {anchor!r} has changed cues: {', '.join(changes)}. Verify the claim manually.",
            ))

    status = "needs-review" if literal.ok else "fail-literal"
    return FidelityReport(status, literal, tuple(findings))


def compare_fidelity_files(source_path: str, candidate_path: str, terms: list[str] | None = None) -> FidelityReport:
    return compare_fidelity(
        Path(source_path).read_text(encoding="utf-8"),
        Path(candidate_path).read_text(encoding="utf-8"),
        terms,
    )


def format_fidelity_report(report: FidelityReport, output_format: str = "markdown") -> str:
    if output_format == "json":
        return json.dumps(report.to_dict(), ensure_ascii=False, indent=2) + "\n"
    lines = [
        "# Rewrite Fidelity Verification", "", f"- Status: `{report.status}`",
        f"- Literal check: `{'pass' if report.literal.ok else 'fail'}`",
        f"- Claim spans requiring review: `{sum(item.kind == 'changed-claim-span' for item in report.findings)}`",
        "- Matching protected tokens do not establish unchanged meaning.", "",
    ]
    for item in report.findings:
        lines.extend([
            f"## {item.kind}: source line {item.source_line or '-'}, candidate line {item.candidate_line or '-'}",
            f"- Source offset: `{item.source_start}`; candidate offset: `{item.candidate_start}`",
            f"- Before: {item.source_excerpt or '[omitted]'}",
            f"- After: {item.candidate_excerpt or '[omitted]'}",
            f"- Review: {item.detail}", "",
        ])
    if not report.literal.ok:
        lines.append("Protected literal differences are also present; run `verify` for the itemized list.\n")
    lines.append(report.disclaimer)
    return "\n".join(lines) + "\n"
