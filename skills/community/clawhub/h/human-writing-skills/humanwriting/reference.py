from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


DEFAULT_REFERENCE_BUDGET = 12000
MIN_REFERENCE_BUDGET = 1000
STYLE_REQUEST_PATTERNS = [
    re.compile(
        r"(?:参考|模仿|贴近|沿用|按照|按).{0,40}?(?:文风|风格|笔调|语气|写法|叙述)",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:in the style of|match .{0,30}?(?:style|voice)|reference .{0,30}?(?:style|voice)|"
        r"follow .{0,30}?(?:style|voice))",
        re.IGNORECASE,
    ),
]


@dataclass(frozen=True)
class ReferencePack:
    active: bool
    trigger: str
    block: str
    source_names: tuple[str, ...]
    sampled_characters: int


def find_style_request(text: str | None) -> str:
    if not text:
        return ""
    for pattern in STYLE_REQUEST_PATTERNS:
        match = pattern.search(text)
        if match:
            return match.group(0).strip()
    return ""


def sample_reference(text: str, budget: int) -> str:
    text = text.strip()
    if len(text) <= budget:
        return text
    marker = "\n\n[... middle sample ...]\n\n"
    if budget <= len(marker) * 2 + 3:
        return text[:budget]
    segment = max(1, (budget - len(marker) * 2) // 3)
    middle_start = max(0, len(text) // 2 - segment // 2)
    sample = (
        text[:segment]
        + marker
        + text[middle_start : middle_start + segment]
        + marker
        + text[-segment:]
    )
    return sample[:budget]


def build_reference_pack(
    paths: list[str] | None = None,
    style_hint: str | None = None,
    task: str | None = None,
    budget: int = DEFAULT_REFERENCE_BUDGET,
) -> ReferencePack:
    task_hint = find_style_request(task)
    explicit_hint = (style_hint or "").strip() or task_hint
    source_paths = [Path(path) for path in dict.fromkeys(paths or [])]
    if not source_paths and not explicit_hint:
        return ReferencePack(False, "", "", (), 0)
    if budget < MIN_REFERENCE_BUDGET:
        raise ValueError(f"Reference budget must be at least {MIN_REFERENCE_BUDGET} characters.")

    samples: list[tuple[str, str]] = []
    if source_paths:
        per_source_budget, remainder = divmod(budget, len(source_paths))
        for index, path in enumerate(source_paths):
            text = path.read_text(encoding="utf-8").strip()
            if not text:
                raise ValueError(f"Reference file is empty: {path}")
            source_budget = per_source_budget + (1 if index < remainder else 0)
            samples.append((path.name, sample_reference(text, source_budget)))

    triggers = []
    if samples:
        triggers.append("reference file input")
    if style_hint and style_hint.strip():
        triggers.append("explicit --reference-style input")
    elif task_hint:
        triggers.append(f"explicit task wording: {task_hint}")

    lines = [
        "# Reference Style Material",
        "",
        f"Activation reason: {'; '.join(triggers)}.",
        "Use this material to infer transferable style features only.",
        "Project context remains the authority for facts, plot, relationships, and world rules.",
        "Do not copy distinctive phrases, signature metaphors, names, events, or conclusions.",
    ]
    if explicit_hint:
        lines.extend(["", "## Explicit Style Direction", "", explicit_hint])
    for name, sample in samples:
        lines.extend(["", f"## Reference: {name}", "", sample])

    block = "\n".join(lines).strip()
    return ReferencePack(
        active=True,
        trigger="; ".join(triggers),
        block=block,
        source_names=tuple(name for name, _ in samples),
        sampled_characters=sum(len(sample) for _, sample in samples),
    )
