from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .compiler import FACTUAL_SOURCE_STYLES, compile_audit_prompt, read_optional
from .detection import PIPELINE_PROFILES, ProfileDecision, detect_audit_profiles
from .linter import format_lint_report, lint_file
from .original import build_original_pack
from .protection import detect_serious_document
from .reference import DEFAULT_REFERENCE_BUDGET, build_reference_pack
from .source import DEFAULT_SOURCE_BUDGET, build_source_pack
from .statistics import analyze_style_file, format_style_statistics


@dataclass(frozen=True)
class AuditStage:
    order: int
    profile: str
    reason: str
    prompt: str


def select_pipeline_profiles(
    draft: str,
    stages: list[str] | None = None,
    auto: bool = False,
    reference_active: bool = False,
    original_active: bool = False,
    context_active: bool = False,
    source_active: bool = False,
    serious_document: bool = False,
    context: str = "",
    source_eligible: bool | None = None,
) -> tuple[list[str], list[ProfileDecision]]:
    factual_sources_enabled = serious_document if source_eligible is None else source_eligible
    if stages:
        selected = list(dict.fromkeys(stages))
        unknown = set(selected) - set(PIPELINE_PROFILES)
        if unknown:
            raise ValueError(f"Unknown pipeline stage: {', '.join(sorted(unknown))}")
        if "style-match" in selected and not reference_active:
            raise ValueError("The style-match stage requires --reference or --reference-style.")
        if "fidelity" in selected and not original_active:
            raise ValueError("The fidelity stage requires --original with the pre-rewrite text.")
        if "preservation" in selected and not original_active:
            raise ValueError("The preservation stage requires --original with the pre-rewrite text.")
        if "capability" in selected and not context_active:
            raise ValueError("The capability stage requires --context with prior state or a continuity ledger.")
        if "sources" in selected and not source_active:
            raise ValueError("The sources stage requires one or more --source files.")
        if "sources" in selected and not factual_sources_enabled:
            raise ValueError("The sources stage requires a serious or explicitly factual self-media/argumentative document type.")
        decisions = []
        for profile in PIPELINE_PROFILES:
            is_selected = profile in selected
            reason = (
                "Explicitly selected by the user."
                if is_selected
                else "Not explicitly selected by the user."
            )
            if profile == "style-match" and not reference_active:
                reason = "No explicit reference material or style direction was supplied."
            if profile == "fidelity" and not original_active:
                reason = "No pre-rewrite --original file was supplied."
            if profile == "preservation" and not original_active:
                reason = "No pre-rewrite --original file was supplied."
            if profile == "capability" and not context_active:
                reason = "No prior-state --context file was supplied."
            if profile == "sources" and not source_active:
                reason = "No factual --source files were supplied."
            elif profile == "sources" and not factual_sources_enabled:
                reason = "No eligible factual document type was established."
            decisions.append(ProfileDecision(profile, is_selected, reason))
        return selected, decisions
    if auto:
        decisions = detect_audit_profiles(
            draft,
            reference_active=reference_active,
            original_active=original_active,
            context_active=context_active,
            source_active=source_active,
            serious_document=serious_document,
            source_eligible=factual_sources_enabled,
            context=context,
        )
        return [decision.profile for decision in decisions if decision.selected], decisions
    decisions = []
    selected = []
    for profile in PIPELINE_PROFILES:
        include = profile not in {
            "voice",
            "register",
            "capability",
            "serial",
            "world",
            "process",
            "momentum",
            "salience",
            "recurrence",
            "repetition",
            "texture",
            "ending",
            "sources",
            "fidelity",
            "preservation",
        }
        if profile == "style-match":
            include = reference_active
        if profile == "fidelity":
            include = original_active
        if profile == "sources":
            include = source_active and factual_sources_enabled
        if include:
            reason = "Included in the established broad pipeline."
        elif profile == "style-match":
            reason = "No explicit reference material or style direction was supplied."
        elif profile == "fidelity":
            reason = "An original was supplied." if original_active else "No pre-rewrite --original file was supplied."
        elif profile == "preservation":
            reason = "Optional high-cost source-to-rewrite voice comparison."
        elif profile == "sources" and not source_active:
            reason = "No factual --source files were supplied."
        elif profile == "sources":
            reason = "No eligible factual document type was established."
        elif profile == "repetition":
            reason = "Optional narrative-only repetition and exposition pass; use --auto or select it explicitly."
        else:
            reason = "Optional high-cost stage; use --auto or select it explicitly."
        decisions.append(ProfileDecision(profile, include, reason))
        if include:
            selected.append(profile)
    return selected, decisions


def build_audit_pipeline(
    draft_path: str,
    context_path: str | None = None,
    stages: list[str] | None = None,
    auto: bool = False,
    reference_paths: list[str] | None = None,
    reference_style: str | None = None,
    reference_budget: int = DEFAULT_REFERENCE_BUDGET,
    source_paths: list[str] | None = None,
    source_budget: int = DEFAULT_SOURCE_BUDGET,
    original_path: str | None = None,
    protect_content: bool = False,
    protect_terms: list[str] | None = None,
    document_type: str = "auto",
) -> tuple[list[AuditStage], list[ProfileDecision]]:
    draft = read_optional(draft_path)
    context = read_optional(context_path)
    context_active = bool(context)
    reference_pack = build_reference_pack(
        reference_paths,
        reference_style,
        budget=reference_budget,
    )
    source_pack = build_source_pack(source_paths, source_budget)
    original_pack = build_original_pack(original_path)
    serious_document, _ = detect_serious_document(draft, document_type=document_type)
    source_eligible = serious_document or document_type in FACTUAL_SOURCE_STYLES
    selected, decisions = select_pipeline_profiles(
        draft,
        stages=stages,
        auto=auto,
        reference_active=reference_pack.active,
        original_active=original_pack.active,
        context_active=context_active,
        source_active=source_pack.active,
        serious_document=serious_document,
        source_eligible=source_eligible,
        context=context,
    )
    reason_by_profile = {decision.profile: decision.reason for decision in decisions}
    auto_protection, _ = detect_serious_document(draft, document_type=document_type)
    protection_profile = None
    if auto_protection and selected:
        protection_profile = "proofread" if "proofread" in selected else selected[-1]
    pipeline = [
        AuditStage(
            order=index,
            profile=profile,
            reason=reason_by_profile[profile],
            prompt=compile_audit_prompt(
                draft_path,
                context_path=context_path,
                strict_continuity=False,
                profiles=[profile],
                reference_paths=reference_paths if profile == "style-match" else None,
                reference_style=reference_style if profile == "style-match" else None,
                reference_budget=reference_budget,
                source_paths=source_paths if profile == "sources" else None,
                source_budget=source_budget,
                original_path=original_path if profile in {"fidelity", "preservation"} else None,
                protect_content=protect_content,
                protect_terms=protect_terms,
                document_type=document_type,
                auto_protect=profile == protection_profile,
            ),
        )
        for index, profile in enumerate(selected, start=1)
    ]
    return pipeline, decisions


def write_audit_pipeline(
    draft_path: str,
    output_dir: str,
    context_path: str | None = None,
    stages: list[str] | None = None,
    auto: bool = False,
    reference_paths: list[str] | None = None,
    reference_style: str | None = None,
    reference_budget: int = DEFAULT_REFERENCE_BUDGET,
    source_paths: list[str] | None = None,
    source_budget: int = DEFAULT_SOURCE_BUDGET,
    original_path: str | None = None,
    protect_content: bool = False,
    protect_terms: list[str] | None = None,
    document_type: str = "auto",
    lint_style: str = "general",
    lint_allow: set[str] | None = None,
    with_stats: bool = False,
) -> tuple[Path, list[AuditStage]]:
    pipeline, decisions = build_audit_pipeline(
        draft_path,
        context_path=context_path,
        stages=stages,
        auto=auto,
        reference_paths=reference_paths,
        reference_style=reference_style,
        reference_budget=reference_budget,
        source_paths=source_paths,
        source_budget=source_budget,
        original_path=original_path,
        protect_content=protect_content,
        protect_terms=protect_terms,
        document_type=document_type,
    )
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    lint_report = lint_file(draft_path, style=lint_style, allow=lint_allow)
    (output / "00-pattern-lint.md").write_text(
        format_lint_report(lint_report, "markdown"), encoding="utf-8"
    )
    (output / "00-pattern-lint.json").write_text(
        format_lint_report(lint_report, "json"), encoding="utf-8"
    )
    stats_report = None
    if with_stats:
        stats_report = analyze_style_file(draft_path, style=lint_style)
        (output / "00-style-stats.md").write_text(
            format_style_statistics(stats_report, "markdown"), encoding="utf-8"
        )
        (output / "00-style-stats.json").write_text(
            format_style_statistics(stats_report, "json"), encoding="utf-8"
        )

    rows = []
    for stage in pipeline:
        filename = f"{stage.order:02d}-{stage.profile}.md"
        (output / filename).write_text(stage.prompt, encoding="utf-8")
        rows.append(f"| {stage.order} | `{stage.profile}` | {stage.reason} | `{filename}` |")

    decision_rows = [
        f"| `{decision.profile}` | {'yes' if decision.selected else 'no'} | {decision.reason} |"
        for decision in decisions
    ]
    manifest = "\n".join(
        [
            "# Audit Pipeline",
            "",
            "Run every stage in a fresh model conversation or independent API request.",
            "Do not carry the model's hidden conversation memory between stages.",
            "Save each stage report, then reconcile them after all selected stages finish.",
            "每个阶段都应放进新的模型会话或独立 API 请求；全部完成后再汇总报告。",
            "Start with `00-pattern-lint.md` for deterministic evidence spans. Its score is",
            "a transparent editing heuristic, not evidence of AI authorship.",
            f"Pattern lint style: `{lint_style}`; score: `{lint_report.score}`; findings: `{len(lint_report.findings)}`.",
            (
                f"Optional style statistics: enabled; warnings: `{len(stats_report.warnings)}`."
                if stats_report is not None
                else "Optional style statistics: disabled; use `--with-stats` when needed."
            ),
            "",
            "| Order | Profile | Why selected | Prompt file |",
            "| --- | --- | --- | --- |",
            *rows,
            "",
            "## Selection Decisions",
            "",
            "| Profile | Selected | Reason |",
            "| --- | --- | --- |",
            *decision_rows,
            "",
            "## Final Reconciliation",
            "",
            "Merge confirmed findings only after all stages finish. Deduplicate findings,",
            "resolve conflicts using quoted draft evidence, and apply repairs in this order:",
            "optional stats -> logic -> character/relationship/voice/register/capability/serial/world/process/momentum -> salience/recurrence/repetition -> physical -> AI trace/ending/texture -> style match/fidelity/optional preservation -> numbers -> sources -> proofreading.",
            "Re-run affected downstream stages after any structural rewrite.",
            "",
        ]
    )
    (output / "README.md").write_text(manifest, encoding="utf-8")
    return output, pipeline
