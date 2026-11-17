from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from .compiler import read_optional
from .detection import has_directed_interaction
from .reference import build_reference_pack, sample_reference
from .source import DEFAULT_SOURCE_BUDGET, build_source_pack
from .skills import list_style_skills, load_skill
from .statistics import StyleStatistics, analyze_style_statistics, format_style_statistics


DEFAULT_CHUNK_SIZE = 8000
DEFAULT_OVERLAP_SIZE = 600
DEFAULT_CONTEXT_BUDGET = 6000
DEFAULT_BASELINE_BUDGET = 4000
MIN_CHUNK_SIZE = 2000
NARRATIVE_STYLES = {"fiction", "webnovel"}
SERIOUS_STYLES = {"academic-paper", "formal-document", "news-report"}
AGENT_MODES = {"standard", "deep"}
DIALOGUE_PATTERN = re.compile(r"[\"“‘「『].{1,240}?[\"”’」』]", re.DOTALL)
BOOK_CHAPTER_PATTERN = re.compile(
    r"(?im)^[ \t]*(?:#{1,3}[ \t]*)?(?:第[零一二三四五六七八九十百千万\d]+[章节回]|chapter[ \t]+\d+)"
)
RECEIPT_STATUS_PATTERN = re.compile(
    r"(?im)^\s*(?:[-*]\s*)?Coverage\s*:\s*(complete|blocked)\b"
)
RECEIPT_UNCHECKED_PATTERN = re.compile(
    r"(?im)^\s*(?:[-*]\s*)?Unchecked or blocked material\s*:\s*(.+?)\s*$"
)
SPLIT_PATTERNS = (
    re.compile(r"\n\s*\n"),
    re.compile(r"(?<=[。！？!?])(?:[\"”’」』】）)])?"),
    re.compile(r"\n"),
)


@dataclass(frozen=True)
class TextChunk:
    index: int
    start: int
    end: int
    lead_start: int
    lead_in: str
    body: str


@dataclass(frozen=True)
class ChunkDiagnostic:
    index: int
    start: int
    end: int
    character_count: int
    average_sentence_length: float
    sentence_length_cv: float
    paragraph_length_cv: float | None
    mattr: float | None
    transition_density_per_1000: float
    candidate_drift: tuple[str, ...]

    def to_dict(self) -> dict:
        data = asdict(self)
        data["candidate_drift"] = list(self.candidate_drift)
        return data


@dataclass(frozen=True)
class AgentTask:
    """One independently runnable review task with an expected report receipt."""

    task_id: str
    kind: str
    prompt: str
    report: str
    depends_on: tuple[str, ...] = ()
    chunk_index: int | None = None
    required_before_reconciliation: bool = True

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "kind": self.kind,
            "prompt": self.prompt,
            "report": self.report,
            "depends_on": list(self.depends_on),
            "chunk_index": self.chunk_index,
            "required_before_reconciliation": self.required_before_reconciliation,
        }


def _preferred_split(text: str, start: int, target: int) -> int:
    if target >= len(text):
        return len(text)
    floor = start + max(1, (target - start) // 2)
    search_start = max(floor, target - 1600)
    for pattern in SPLIT_PATTERNS:
        candidates = [match.end() for match in pattern.finditer(text, search_start, target)]
        if candidates:
            return candidates[-1]
    return target


def split_long_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP_SIZE,
) -> list[TextChunk]:
    if chunk_size < MIN_CHUNK_SIZE:
        raise ValueError(f"Chunk size must be at least {MIN_CHUNK_SIZE} characters.")
    if overlap < 0:
        raise ValueError("Overlap must be zero or greater.")
    if overlap >= chunk_size // 2:
        raise ValueError("Overlap must be smaller than half the chunk size.")
    if not text:
        raise ValueError("Long-form audit requires a non-empty draft.")

    chunks: list[TextChunk] = []
    start = 0
    while start < len(text):
        end = _preferred_split(text, start, min(len(text), start + chunk_size))
        if end <= start:
            end = min(len(text), start + chunk_size)
        lead_start = max(0, start - overlap)
        chunks.append(
            TextChunk(
                index=len(chunks) + 1,
                start=start,
                end=end,
                lead_start=lead_start,
                lead_in=text[lead_start:start],
                body=text[start:end],
            )
        )
        start = end
    return chunks


def _sample_paths(paths: list[str] | None, budget: int) -> tuple[str, tuple[str, ...]]:
    unique_paths = [Path(path) for path in dict.fromkeys(paths or [])]
    if not unique_paths:
        return "", ()
    per_source, remainder = divmod(budget, len(unique_paths))
    samples: list[str] = []
    names: list[str] = []
    for index, path in enumerate(unique_paths):
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            raise ValueError(f"Reference file is empty: {path}")
        source_budget = per_source + (1 if index < remainder else 0)
        samples.append(sample_reference(text, source_budget))
        names.append(path.name)
    return "\n\n".join(samples), tuple(names)


def _change_ratio(value: float, baseline: float) -> float | None:
    if baseline == 0:
        return None
    return value / baseline


def _diagnose_chunk(
    chunk: TextChunk,
    baseline: StyleStatistics,
    style: str,
) -> tuple[StyleStatistics, ChunkDiagnostic]:
    report = analyze_style_statistics(chunk.body, style=style)
    flags: list[str] = []
    sentence_ratio = _change_ratio(report.average_sentence_length, baseline.average_sentence_length)
    if sentence_ratio is not None and (sentence_ratio < 0.65 or sentence_ratio > 1.55):
        flags.append("average sentence length differs materially from the baseline")
    if abs(report.sentence_length_cv - baseline.sentence_length_cv) > 0.25:
        flags.append("sentence-length variation differs materially from the baseline")
    if report.paragraph_length_cv is not None and baseline.paragraph_length_cv is not None:
        if abs(report.paragraph_length_cv - baseline.paragraph_length_cv) > 0.3:
            flags.append("paragraph-weight variation differs materially from the baseline")
    if report.mattr is not None and baseline.mattr is not None:
        if abs(report.mattr - baseline.mattr) > 0.15:
            flags.append("lexical diversity differs materially from the baseline")
    if abs(
        report.transition_density_per_1000 - baseline.transition_density_per_1000
    ) > 12:
        flags.append("explicit-transition density differs materially from the baseline")
    diagnostic = ChunkDiagnostic(
        index=chunk.index,
        start=chunk.start,
        end=chunk.end,
        character_count=len(chunk.body),
        average_sentence_length=report.average_sentence_length,
        sentence_length_cv=report.sentence_length_cv,
        paragraph_length_cv=report.paragraph_length_cv,
        mattr=report.mattr,
        transition_density_per_1000=report.transition_density_per_1000,
        candidate_drift=tuple(flags),
    )
    return report, diagnostic


def _module_block(name: str) -> str:
    return f"# Audit Module: {name}\n\n{load_skill(name).content}"


def _coverage_receipt(task_id: str, chunk: TextChunk | None = None) -> str:
    scope = (
        f"audited body `{chunk.start}:{chunk.end}`" if chunk else "the assigned package stage"
    )
    return (
        "# Coverage Receipt\n\n"
        f"- Task ID: `{task_id}`\n"
        f"- Scope: {scope}\n"
        "- Coverage: complete / blocked\n"
        "- Units checked: list paragraph, section, claim, or dialogue-turn identifiers\n"
        "- Confirmed findings: count and locations\n"
        "- Unchecked or blocked material: none, or explain exactly why\n"
    )


def _write_agent_plan(output: Path, tasks: list[AgentTask], mode: str) -> None:
    plan = {
        "schema": 1,
        "mode": mode,
        "instructions": (
            "Run tasks in dependency order. Tasks that share only the baseline dependency "
            "may run in parallel in fresh model sessions. Save each response at its expected "
            "report path. Run reconciliation only after every required report is present."
        ),
        "tasks": [task.to_dict() for task in tasks],
    }
    (output / "agent-plan.json").write_text(
        json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def validate_long_form_report(task: dict, report: str) -> str | None:
    """Return a precise receipt error, or ``None`` when a report can be reconciled."""

    task_id = task.get("task_id", "unknown")
    normalized = report.strip()
    if len(normalized) < 80:
        return "report is too short"
    if "Coverage Receipt" not in normalized:
        return "Coverage Receipt heading is missing"
    if task_id not in normalized:
        return "task ID is not echoed in the receipt"
    status = RECEIPT_STATUS_PATTERN.search(normalized)
    if not status:
        return "coverage status must explicitly be complete or blocked"
    if status.group(1).lower() != "complete":
        return "coverage is blocked"
    unchecked = RECEIPT_UNCHECKED_PATTERN.search(normalized)
    if not unchecked:
        return "unchecked or blocked material line is missing"
    if unchecked.group(1).strip().lower().rstrip(".") not in {"none", "n/a"}:
        return "receipt declares unchecked or blocked material"
    return None


def verify_long_form_package(package_dir: str) -> dict:
    """Check that external reviewers returned a non-empty receipt for every planned task."""

    from .audit_storage import load_plan, package_path

    package, plan, tasks = load_plan(package_dir)

    complete: list[str] = []
    missing: list[str] = []
    invalid: list[str] = []
    required_tasks = [task for task in tasks if task.get("required_before_reconciliation", True)]
    for task in required_tasks:
        task_id = task.get("task_id", "unknown")
        report_value = task.get("report")
        if not isinstance(report_value, str):
            invalid.append(f"{task_id}: no report path")
            continue
        report_path = package_path(package, report_value, "report path")
        if not report_path.is_file():
            missing.append(f"{task_id}: {report_value}")
            continue
        report = report_path.read_text(encoding="utf-8")
        receipt_error = validate_long_form_report(task, report)
        if receipt_error:
            invalid.append(f"{task_id}: {receipt_error}")
            continue
        complete.append(task_id)

    return {
        "package": str(package),
        "mode": plan.get("mode", "unknown"),
        "planned": len(required_tasks),
        "deferred": [
            task.get("task_id", "unknown")
            for task in tasks
            if not task.get("required_before_reconciliation", True)
        ],
        "complete": complete,
        "missing": missing,
        "invalid": invalid,
        "ready_for_reconciliation": not missing and not invalid,
    }


def format_long_form_verification(report: dict, output_format: str = "markdown") -> str:
    if output_format == "json":
        return json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    lines = [
        "# Long-Form Audit Coverage",
        "",
        f"- Package: `{report['package']}`",
        f"- Agent mode: `{report['mode']}`",
        f"- Planned tasks: `{report['planned']}`",
        f"- Complete receipts: `{len(report['complete'])}`",
        f"- Ready for reconciliation: `{'yes' if report['ready_for_reconciliation'] else 'no'}`",
        "",
    ]
    for label, entries in (("Missing", report["missing"]), ("Invalid", report["invalid"])):
        lines.append(f"## {label}")
        lines.append("")
        lines.extend(f"- {entry}" for entry in entries)
        if not entries:
            lines.append("- none")
        lines.append("")
    return "\n".join(lines)


def _base_prompt_sections(style: str) -> list[str]:
    style_skill = load_skill(style)
    return [
        f"# Selected Style: {style}",
        style_skill.content,
        _module_block("long-form-style-consistency"),
    ]


def _format_diagnostics(
    baseline: StyleStatistics,
    diagnostics: list[ChunkDiagnostic],
) -> str:
    rows = [
        "# Cross-Chunk Style Diagnostics",
        "",
        "These distributional differences are review leads, not proof of a defect or authorship.",
        "Topic, scene function, quoted material, and deliberate character development may explain them.",
        "",
        "## Baseline",
        "",
        format_style_statistics(baseline, "markdown").strip(),
        "",
        "## Chunks",
        "",
        "| Chunk | Characters | Avg sentence | Sentence CV | Paragraph CV | MATTR | Transitions/1000 | Candidate drift |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for item in diagnostics:
        paragraph_cv = "n/a" if item.paragraph_length_cv is None else str(item.paragraph_length_cv)
        mattr = "n/a" if item.mattr is None else str(item.mattr)
        flags = "; ".join(item.candidate_drift) or "none from deterministic thresholds"
        rows.append(
            f"| {item.index} | {item.character_count} | {item.average_sentence_length} | "
            f"{item.sentence_length_cv} | {paragraph_cv} | {mattr} | "
            f"{item.transition_density_per_1000} | {flags} |"
        )
    return "\n".join(rows) + "\n"


def write_long_form_audit(
    draft_path: str,
    output_dir: str,
    style: str,
    context_path: str | None = None,
    reference_paths: list[str] | None = None,
    reference_style: str | None = None,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP_SIZE,
    baseline_chunk: int = 1,
    context_budget: int = DEFAULT_CONTEXT_BUDGET,
    baseline_budget: int = DEFAULT_BASELINE_BUDGET,
    source_paths: list[str] | None = None,
    source_budget: int = DEFAULT_SOURCE_BUDGET,
    agent_mode: str = "standard",
    translationese: bool = False,
    book_level: bool = False,
) -> tuple[Path, list[TextChunk]]:
    if style not in list_style_skills():
        raise ValueError(f"Unknown style '{style}'.")
    if context_budget < 1000:
        raise ValueError("Context budget must be at least 1000 characters.")
    if baseline_budget < 1000:
        raise ValueError("Baseline budget must be at least 1000 characters.")
    if agent_mode not in AGENT_MODES:
        raise ValueError(f"Agent mode must be one of: {', '.join(sorted(AGENT_MODES))}.")
    if book_level and style not in NARRATIVE_STYLES:
        raise ValueError("Whole-book architecture review is limited to fiction and webnovels.")

    draft = Path(draft_path).read_text(encoding="utf-8")
    if not draft.strip():
        raise ValueError("Long-form audit requires a non-empty --draft file.")
    chapter_matches = list(BOOK_CHAPTER_PATTERN.finditer(draft))
    chapter_count = len(chapter_matches)
    if book_level and chapter_count < 3:
        raise ValueError("Whole-book architecture review requires at least three identifiable chapter headings.")
    chunks = split_long_text(draft, chunk_size=chunk_size, overlap=overlap)
    chapter_index = [
        {
            "index": index + 1,
            "heading": match.group(0).strip(),
            "start": match.start(),
            "end": chapter_matches[index + 1].start() if index + 1 < chapter_count else len(draft),
            "chunks": [
                chunk.index for chunk in chunks
                if chunk.start < (chapter_matches[index + 1].start() if index + 1 < chapter_count else len(draft))
                and chunk.end > match.start()
            ],
        }
        for index, match in enumerate(chapter_matches)
    ] if book_level else []
    if not 1 <= baseline_chunk <= len(chunks):
        raise ValueError(f"Baseline chunk must be between 1 and {len(chunks)}.")

    context = read_optional(context_path)
    context_sample = sample_reference(context, context_budget) if context else ""
    reference_sample, reference_names = _sample_paths(reference_paths, baseline_budget)
    reference_pack = build_reference_pack(
        reference_paths,
        reference_style,
        budget=baseline_budget,
    )
    source_pack = build_source_pack(source_paths, source_budget)
    selected_baseline = chunks[baseline_chunk - 1]
    baseline_text = reference_sample or sample_reference(selected_baseline.body, baseline_budget)
    baseline_source = (
        f"explicit reference files: {', '.join(reference_names)}"
        if reference_names
        else f"manuscript chunk {baseline_chunk} (candidate baseline; confirm before repair)"
    )
    if reference_style and not reference_names:
        baseline_source += " plus explicit style direction"
    baseline_stats = analyze_style_statistics(baseline_text, style=style)

    reports: list[StyleStatistics] = []
    diagnostics: list[ChunkDiagnostic] = []
    for chunk in chunks:
        report, diagnostic = _diagnose_chunk(chunk, baseline_stats, style)
        reports.append(report)
        diagnostics.append(diagnostic)

    output = Path(output_dir)
    if output.exists() and any(output.iterdir()):
        raise ValueError(
            "Long-form audit output directory must be empty to avoid stale chunk prompts."
        )
    output.mkdir(parents=True, exist_ok=True)
    (output / "reports").mkdir()
    agent_tasks: list[AgentTask] = []
    diagnostic_text = _format_diagnostics(baseline_stats, diagnostics)
    (output / "00-style-drift.md").write_text(diagnostic_text, encoding="utf-8")
    diagnostic_json = {
        "disclaimer": "Distributional editing diagnostics, not authorship evidence.",
        "style": style,
        "baseline_source": baseline_source,
        "baseline": baseline_stats.to_dict(),
        "chunks": [item.to_dict() for item in diagnostics],
    }
    (output / "00-style-drift.json").write_text(
        json.dumps(diagnostic_json, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    shared_sections = _base_prompt_sections(style)
    if translationese:
        shared_sections.append(_module_block("translationese-audit"))
    if style in NARRATIVE_STYLES and context:
        shared_sections.append(_module_block("character-consistency-audit"))
    if style in SERIOUS_STYLES:
        shared_sections.append(_module_block("protected-content"))
    baseline_evidence = reference_pack.block if reference_pack.active else (
        "# Candidate Baseline Excerpt\n\n" + baseline_text
    )
    source_evidence = source_pack.block if source_pack.active else ""
    if context_sample:
        context_block = (
            "# Outline / Continuity Authority\n\n"
            "Treat this as canonical for facts, character settings, terminology, and claim boundaries as applicable. "
            "A later explicit change gate may update it.\n\n"
            + context_sample
        )
    else:
        context_block = (
            "# Outline / Continuity Authority\n\n"
            "No outline or continuity ledger was supplied. Treat inferred character traits as provisional, not canon."
        )

    baseline_prompt = "\n\n".join(
        [
            "# Long-Form Baseline Extraction",
            "Build a compact, evidence-backed style contract for later chunk audits. "
            "Do not rewrite the manuscript in this pass. Separate stable voice from topic- or scene-specific variation.",
            *shared_sections,
            context_block,
            baseline_evidence,
            "# Baseline Statistics\n\n" + format_style_statistics(baseline_stats).strip(),
            "# Required Output\n\n"
            "Return: stable style anchors; permitted range; character cards supported by the outline; "
            "speaker voice anchors; deliberate evolution gates; serious-document terminology and claim-scope rules; "
            "and uncertain items that must not be treated as canon. Keep the result compact enough to reuse in every chunk pass.",
            _coverage_receipt("baseline"),
        ]
    ) + "\n"
    (output / "00-baseline-prompt.md").write_text(baseline_prompt, encoding="utf-8")
    agent_tasks.append(
        AgentTask(
            task_id="baseline",
            kind="baseline",
            prompt="00-baseline-prompt.md",
            report="reports/00-baseline-report.md",
        )
    )

    for chunk, report in zip(chunks, reports):
        chunk_sections = list(shared_sections)
        interaction_active = style in NARRATIVE_STYLES and (
            DIALOGUE_PATTERN.search(chunk.body) or has_directed_interaction(chunk.body)
        )
        if interaction_active:
            chunk_sections.append(_module_block("dialogue-voice-audit"))
        lead_in = chunk.lead_in or "[No prior lead-in: this is the first chunk.]"
        task_id = f"chunk-{chunk.index:04d}-core"
        prompt = "\n\n".join(
            [
                f"# Long-Form Chunk Audit {chunk.index}/{len(chunks)}",
                "Audit only the numbered body below. The lead-in is read-only continuity context: "
                "do not report or rewrite a problem located only in that lead-in. Compare against the approved baseline and outline, "
                "but allow evidence-backed shifts caused by viewpoint, section function, time, pressure, or character development.",
                *chunk_sections,
                context_block,
                baseline_evidence,
                "# Baseline Statistics\n\n" + format_style_statistics(baseline_stats).strip(),
                "# Current Chunk Statistics\n\n" + format_style_statistics(report).strip(),
                f"# Read-Only Lead-In ({chunk.lead_start}:{chunk.start})\n\n{lead_in}",
                f"# Audited Body ({chunk.start}:{chunk.end})\n\n{chunk.body}",
                "# Required Output\n\n"
                "Locate evidence by body character offset or a short quotation. Separate confirmed drift, plausible intentional variation, "
                "and insufficient evidence. For fiction, compare each character with outline-backed goals, knowledge, relationships, "
                "behavioral limits, and speaker voice; require an on-page change gate before accepting a contradiction. For serious text, "
                "preserve facts, figures, quotations, terminology, attribution, uncertainty, and conclusion scope. Recommend the smallest local repair, "
                "then emit a compact state-and-voice delta for the next chunk. Do not normalize every sentence or character into one average voice.",
                _coverage_receipt(task_id, chunk),
            ]
        ) + "\n"
        prompt_name = f"{chunk.index:04d}-chunk-audit.md"
        (output / prompt_name).write_text(prompt, encoding="utf-8")
        agent_tasks.append(
            AgentTask(
                task_id=task_id,
                kind="core-chunk-audit",
                prompt=prompt_name,
                report=f"reports/{chunk.index:04d}-core-report.md",
                depends_on=("baseline",),
                chunk_index=chunk.index,
            )
        )

        if agent_mode == "deep":
            prose_task_id = f"chunk-{chunk.index:04d}-prose"
            prose_prompt_name = f"{chunk.index:04d}-prose-audit.md"
            prose_prompt = "\n\n".join(
                [
                    f"# Deep Prose Audit {chunk.index}/{len(chunks)}",
                    "Read every paragraph in the audited body. Do not rewrite it wholesale. Check for formulaic contrast, chained parallelism, "
                    "empty transition, generic abstraction, repetitive paragraph closure, and lost scene or argument progress. "
                    "Treat a natural local variation as valid unless repetition makes it a structural habit.",
                    _module_block("ai-trace-rubric"),
                    _module_block("formulaic-structure-audit"),
                    _module_block("prose-progress-audit"),
                    f"# Read-Only Lead-In ({chunk.lead_start}:{chunk.start})\n\n{lead_in}",
                    f"# Audited Body ({chunk.start}:{chunk.end})\n\n{chunk.body}",
                    "# Required Output\n\n"
                    "Return a paragraph coverage table (`P1`, `P2`, ...), then only confirmed findings with a quotation, location, "
                    "and smallest repair direction. A clear paragraph must still appear in the coverage table.",
                    _coverage_receipt(prose_task_id, chunk),
                ]
            ) + "\n"
            (output / prose_prompt_name).write_text(prose_prompt, encoding="utf-8")
            agent_tasks.append(
                AgentTask(
                    task_id=prose_task_id,
                    kind="deep-prose-audit",
                    prompt=prose_prompt_name,
                    report=f"reports/{chunk.index:04d}-prose-report.md",
                    depends_on=("baseline",),
                    chunk_index=chunk.index,
                )
            )

            if interaction_active:
                dialogue_task_id = f"chunk-{chunk.index:04d}-dialogue"
                dialogue_prompt_name = f"{chunk.index:04d}-dialogue-audit.md"
                dialogue_prompt = "\n\n".join(
                    [
                        f"# Deep Dialogue Audit {chunk.index}/{len(chunks)}",
                        "Audit every directed spoken or wordless interaction in the body. "
                        "Map initiator, affected recipient, separate speech/action obligations, uptake, and changed state. "
                        "Check both directions and implied completion before flagging a gap. "
                        "If the response may fall beyond the chunk, report a pending boundary check for reconciliation, not a confirmed omission. "
                        "Do not demand a gesture after every line; flag a gap only when a consequential turn is abandoned or a beat is decorative.",
                        _module_block("dialogue-voice-audit"),
                        _module_block("dialogue-performance-audit"),
                        context_block,
                        f"# Audited Body ({chunk.start}:{chunk.end})\n\n{chunk.body}",
                        "# Required Output\n\n"
                        "List every interaction-bearing paragraph or turn range you inspected, including wordless actions. Separate confirmed response, voice, knowledge, "
                        "or performance failures from deliberate evasion and silence.",
                        _coverage_receipt(dialogue_task_id, chunk),
                    ]
                ) + "\n"
                (output / dialogue_prompt_name).write_text(dialogue_prompt, encoding="utf-8")
                agent_tasks.append(
                    AgentTask(
                        task_id=dialogue_task_id,
                        kind="deep-dialogue-audit",
                        prompt=dialogue_prompt_name,
                        report=f"reports/{chunk.index:04d}-dialogue-report.md",
                        depends_on=("baseline",),
                        chunk_index=chunk.index,
                    )
                )

            if style in SERIOUS_STYLES and source_evidence:
                evidence_task_id = f"chunk-{chunk.index:04d}-evidence"
                evidence_prompt_name = f"{chunk.index:04d}-evidence-audit.md"
                evidence_prompt = "\n\n".join(
                    [
                        f"# Deep Evidence Audit {chunk.index}/{len(chunks)}",
                        "Audit every factual claim, attribution, numerical statement, and conclusion-scope statement in the body against the supplied sources. "
                        "Absence from the sampled sources is uncertainty, not disproof. Do not invent citations or repair a fact by guessing.",
                        _module_block("source-grounding"),
                        _module_block("protected-content"),
                        source_evidence,
                        f"# Audited Body ({chunk.start}:{chunk.end})\n\n{chunk.body}",
                        "# Required Output\n\n"
                        "Return a claim coverage table with source support, uncertainty, or mismatch. Keep terminology, figures, quotations, "
                        "attribution, and conclusion scope exact.",
                        _coverage_receipt(evidence_task_id, chunk),
                    ]
                ) + "\n"
                (output / evidence_prompt_name).write_text(evidence_prompt, encoding="utf-8")
                agent_tasks.append(
                    AgentTask(
                        task_id=evidence_task_id,
                        kind="deep-evidence-audit",
                        prompt=evidence_prompt_name,
                        report=f"reports/{chunk.index:04d}-evidence-report.md",
                        depends_on=("baseline",),
                        chunk_index=chunk.index,
                    )
                )

    if book_level:
        (output / "00-chapter-map.json").write_text(
            json.dumps(chapter_index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        architecture_dependencies = tuple(task.task_id for task in agent_tasks)
        architecture_prompt = "\n\n".join(
            [
                "# Whole-Book Story Architecture Review",
                "Read `00-chapter-map.json`, the canonical outline, the completed baseline report, and every core and specialist chunk report in agent-plan.json. "
                "This pass compares chapter functions across the complete work, not just adjacent prose. "
                "If evidence is absent from reports, request precise manuscript spans rather than inventing them.",
                _module_block("story-architecture-audit"),
                context_block,
                "# Chapter Index\n\n" + json.dumps(chapter_index, ensure_ascii=False, indent=2),
                "# Required Output\n\nReturn a chapter-function table covering every chapter, cited cross-chapter patterns, "
                "intentional variation, unresolved source-span requests, and a minimal structural repair plan.",
                _coverage_receipt("book-architecture"),
            ]
        ) + "\n"
        (output / "9000-book-architecture-prompt.md").write_text(architecture_prompt, encoding="utf-8")
        agent_tasks.append(AgentTask(
            task_id="book-architecture",
            kind="whole-book-architecture-audit",
            prompt="9000-book-architecture-prompt.md",
            report="reports/9000-book-architecture-report.md",
            depends_on=architecture_dependencies,
        ))

    reconcile_prompt = "\n\n".join(
        [
            "# Long-Form Cross-Chunk Reconciliation",
            "Use the approved baseline report, `00-style-drift.md`, `agent-plan.json`, and every required completed report under `reports/`. "
            "Do not reconcile while `verify-chunk-audit` reports missing or invalid receipts. "
            "Do not infer a global defect from one statistical outlier. Require quoted or located evidence from at least two relevant blocks, "
            "unless one block directly contradicts the canonical outline.",
            _module_block("long-form-style-consistency"),
            "Use the completed whole-book architecture report as structural evidence when one was requested. "
            "Do not infer that every local pattern is a global flaw.",
            context_block,
            diagnostic_text.strip(),
            "# Required Output\n\n"
            "Produce: a ranked cross-chunk drift table; recurring narrator-style changes; per-character dialogue and behavior conflicts; "
            "valid development or section-function changes; a minimal repair sequence; and ledger updates. Resolve facts and character canon before style, "
            "then voice, rhythm, and surface wording. Re-audit neighboring blocks after structural repairs.",
            "Resolve pending interaction boundary checks against the next relevant block: "
            "identify the recipient and every unresolved speech/action obligation. Preserve "
            "supported delayed or implied uptake; do not turn a chunk boundary into a missing reaction.",
            _coverage_receipt("reconcile"),
        ]
    ) + "\n"
    (output / "9999-reconcile-prompt.md").write_text(reconcile_prompt, encoding="utf-8")
    agent_tasks.append(
        AgentTask(
            task_id="reconcile",
            kind="cross-chunk-reconciliation",
            prompt="9999-reconcile-prompt.md",
            report="reports/9999-reconcile-report.md",
            depends_on=tuple(task.task_id for task in agent_tasks),
            required_before_reconciliation=False,
        )
    )

    manifest = {
        "draft": str(Path(draft_path)),
        "style": style,
        "chunk_size": chunk_size,
        "lead_in_overlap": overlap,
        "baseline_source": baseline_source,
        "context_supplied": bool(context),
        "source_names": list(source_pack.source_names),
        "agent_mode": agent_mode,
        "translationese_review": translationese,
        "book_level_review": book_level,
        "identified_chapters": chapter_count,
        "chunks": [
            {
                "index": chunk.index,
                "start": chunk.start,
                "end": chunk.end,
                "lead_start": chunk.lead_start,
                "body_characters": len(chunk.body),
                "lead_in_characters": len(chunk.lead_in),
                "prompt": f"{chunk.index:04d}-chunk-audit.md",
            }
            for chunk in chunks
        ],
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    _write_agent_plan(output, agent_tasks, agent_mode)

    guide = "\n".join(
        [
            "# Long-Form Chunk Audit Package",
            "",
            f"- Draft style: `{style}`",
            f"- Unique audit chunks: `{len(chunks)}`",
            f"- Baseline source: {baseline_source}",
            f"- Outline / continuity context: `{'supplied' if context else 'not supplied'}`",
            f"- Factual source files: `{len(source_pack.source_names)}`",
            f"- Agent mode: `{agent_mode}`",
            f"- Translationese review: `{'enabled' if translationese else 'not requested'}`",
            f"- Whole-book architecture review: `{'enabled' if book_level else 'not requested'}`",
            "",
            "1. Run `00-baseline-prompt.md` first and save its response as `reports/00-baseline-report.md`.",
            "2. Run every task listed in `agent-plan.json` whose only dependency is `baseline`; they may run in parallel in fresh sessions.",
            "3. Save each response at its planned report path. Every response must retain its Coverage Receipt; the lead-in is context only, so adjacent blocks are not double-counted.",
            "4. If enabled, run `9000-book-architecture-prompt.md` after all chunk reports and save its report.",
            "5. Run `human-writing-skills verify-chunk-audit --package-dir <this-directory>` before reconciliation. Fix missing or invalid receipts first.",
            "6. Run `9999-reconcile-prompt.md`, save the final report, then apply repairs from canon and meaning to character state, voice, rhythm, and surface wording. Re-audit affected neighbors.",
            "",
            "`00-style-drift.md` is a deterministic triage map. Its outliers are review leads, not automatic defects.",
            "For fiction, an outline or continuity ledger is required for authoritative character-setting checks.",
            "For reports, use the outline/context file for terminology, claim scope, section purpose, and source boundaries.",
            "`standard` writes one complete task per chunk. `deep` adds paragraph-by-paragraph prose tasks, interaction tasks only where dialogue or directed actions occur, and evidence tasks only for serious documents with explicit `--source` files.",
            "",
        ]
    )
    (output / "README.md").write_text(guide, encoding="utf-8")
    return output, chunks
