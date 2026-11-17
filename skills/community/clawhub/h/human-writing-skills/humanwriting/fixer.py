from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class SafeEdit:
    rule_id: str
    start: int
    end: int
    before: str
    after: str
    reason: str


@dataclass(frozen=True)
class FixReport:
    source: str
    edits: tuple[SafeEdit, ...]
    candidate: str
    applied: bool = False
    disclaimer: str = (
        "Only deterministic mechanical edits are proposed. Semantic structures, "
        "claims, comparisons, numbers, and character voice require contextual review."
    )

    def to_dict(self) -> dict:
        result = asdict(self)
        result["edits"] = [asdict(edit) for edit in self.edits]
        return result


SAFE_REPLACEMENTS = (
    (
        "FIX_CHAT001",
        re.compile(
            r"(?:(?:希望这对你有所帮助|如有其他问题，请随时(?:告诉我|提问)|"
            r"如果你愿意，我可以继续[^。！？!?]*)[。！？!?]?|"
            r"I hope this helps!?|Feel free to ask[^.!?]*[.!?]?|"
            r"Let me know if you(?:'d| would) like[^.!?]*[.!?]?)",
            re.IGNORECASE,
        ),
        "",
        "Remove assistant-to-user residue from finished prose.",
    ),
    (
        "FIX_FILLER001",
        re.compile(r"(?:值得注意的是|需要指出的是)[，,：:]?\s*"),
        "",
        "Remove a throat-clearing announcement while preserving the following claim.",
    ),
    (
        "FIX_FILLER002",
        re.compile(r"\b(?:it is important to note that|it is worth noting that)\s+", re.IGNORECASE),
        "",
        "State the following claim directly.",
    ),
    (
        "FIX_FILLER003",
        re.compile(r"(?:不可否认(?:的是)?|毋庸置疑(?:的是)?)[，,：:]?\s*"),
        "",
        "Remove pseudo-objective throat-clearing while preserving the following claim.",
    ),
    (
        "FIX_WORDY001",
        re.compile(r"\bin order to\b", re.IGNORECASE),
        "to",
        "Use the shorter equivalent without changing meaning.",
    ),
    (
        "FIX_WORDY002",
        re.compile(r"\bdue to the fact that\b", re.IGNORECASE),
        "because",
        "Use the direct causal connector.",
    ),
    (
        "FIX_WORDY003",
        re.compile(r"\b(?:it is undeniable that|it is obvious that)\s+", re.IGNORECASE),
        "",
        "State the following claim directly.",
    ),
)


def build_fix_report(text: str, source: str = "<memory>") -> FixReport:
    edits: list[SafeEdit] = []
    occupied: list[tuple[int, int]] = []
    for rule_id, pattern, replacement, reason in SAFE_REPLACEMENTS:
        for match in pattern.finditer(text):
            if any(match.start() < end and match.end() > start for start, end in occupied):
                continue
            edits.append(
                SafeEdit(
                    rule_id=rule_id,
                    start=match.start(),
                    end=match.end(),
                    before=match.group(0),
                    after=replacement,
                    reason=reason,
                )
            )
            occupied.append((match.start(), match.end()))
    edits.sort(key=lambda edit: edit.start)
    candidate = text
    for edit in reversed(edits):
        candidate = candidate[: edit.start] + edit.after + candidate[edit.end :]
    return FixReport(source=source, edits=tuple(edits), candidate=candidate)


def fix_file(
    path: str,
    output_path: str | None = None,
    apply: bool = False,
) -> FixReport:
    source = Path(path)
    report = build_fix_report(source.read_text(encoding="utf-8"), source=source.name)
    destination = source if apply else Path(output_path) if output_path else None
    if destination is not None:
        destination.write_text(report.candidate, encoding="utf-8")
    return FixReport(
        source=report.source,
        edits=report.edits,
        candidate=report.candidate,
        applied=destination is not None,
    )


def format_fix_report(report: FixReport, output_format: str = "markdown") -> str:
    if output_format == "json":
        return json.dumps(report.to_dict(), ensure_ascii=False, indent=2) + "\n"
    lines = [
        "# Conservative Fix Preview",
        "",
        f"- Source: `{report.source}`",
        f"- Safe edits: `{len(report.edits)}`",
        f"- Written: `{'yes' if report.applied else 'no'}`",
        f"- Disclaimer: {report.disclaimer}",
        "",
        "| Rule | Span | Before | After | Reason |",
        "| --- | --- | --- | --- | --- |",
    ]
    for edit in report.edits:
        before = edit.before.replace("|", "\\|").replace("\n", " ")
        after = edit.after.replace("|", "\\|").replace("\n", " ") or "(delete)"
        lines.append(
            f"| `{edit.rule_id}` | `{edit.start}:{edit.end}` | {before} | {after} | {edit.reason} |"
        )
    lines.extend(["", "## Candidate", "", report.candidate])
    return "\n".join(lines).rstrip() + "\n"
