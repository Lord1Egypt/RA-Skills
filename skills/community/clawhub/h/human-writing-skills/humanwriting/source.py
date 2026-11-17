from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .reference import sample_reference


DEFAULT_SOURCE_BUDGET = 16000
MIN_SOURCE_BUDGET = 1000


@dataclass(frozen=True)
class SourcePack:
    active: bool
    block: str
    source_names: tuple[str, ...]
    sampled_characters: int


def build_source_pack(
    paths: list[str] | None = None,
    budget: int = DEFAULT_SOURCE_BUDGET,
) -> SourcePack:
    source_paths = [Path(path) for path in dict.fromkeys(paths or [])]
    if not source_paths:
        return SourcePack(False, "", (), 0)
    if budget < MIN_SOURCE_BUDGET:
        raise ValueError(f"Source budget must be at least {MIN_SOURCE_BUDGET} characters.")

    per_source_budget, remainder = divmod(budget, len(source_paths))
    samples: list[tuple[str, str]] = []
    for index, path in enumerate(source_paths):
        content = path.read_text(encoding="utf-8").strip()
        if not content:
            raise ValueError(f"Source file is empty: {path}")
        source_budget = per_source_budget + (1 if index < remainder else 0)
        samples.append((path.name, sample_reference(content, source_budget)))

    lines = [
        "# Supplied Factual Sources",
        "",
        "Use these files as factual evidence for source grounding.",
        "Do not imitate their prose unless the same material was separately supplied as a style reference.",
        "Do not treat absence from this sampled pack as proof that a claim is false.",
    ]
    for name, sample in samples:
        lines.extend(["", f"## Source: {name}", "", sample])

    return SourcePack(
        active=True,
        block="\n".join(lines),
        source_names=tuple(name for name, _ in samples),
        sampled_characters=sum(len(sample) for _, sample in samples),
    )
