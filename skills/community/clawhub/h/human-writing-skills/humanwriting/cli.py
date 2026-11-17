from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .compiler import (
    compile_audit_prompt,
    compile_audit_prompt_text,
    compile_humanize_prompt,
    compile_humanize_prompt_text,
    compile_prompt,
)
from .config import apply_project_defaults
from .detection import PIPELINE_PROFILES
from .evaluation import evaluate_cases, format_evaluation
from .fidelity import compare_fidelity_files, format_fidelity_report
from .fixer import fix_file, format_fix_report
from .ledger import compile_ledger_extraction_prompt, compile_ledger_extraction_prompt_text
from .linter import format_lint_report, lint_file, lint_rule_catalog, lint_text
from .longform import (
    AGENT_MODES,
    DEFAULT_BASELINE_BUDGET,
    DEFAULT_CHUNK_SIZE,
    DEFAULT_CONTEXT_BUDGET,
    DEFAULT_OVERLAP_SIZE,
    format_long_form_verification,
    verify_long_form_package,
    write_long_form_audit,
)
from .pipeline import write_audit_pipeline
from .protection import compare_protected_files, format_protection_report
from .reference import DEFAULT_REFERENCE_BUDGET
from .source import DEFAULT_SOURCE_BUDGET
from .statistics import analyze_style_file, analyze_style_statistics, format_style_statistics
from .skills import list_module_skills, list_skills, list_style_skills
from .review import compile_critique_prompt, prepare_blind_comparison
from .evaluation import evaluate_editorial_cases, format_editorial_evaluation


def add_reference_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--reference",
        action="append",
        default=[],
        help="Reference text file for style matching. Can be repeated.",
    )
    parser.add_argument(
        "--reference-style",
        help="Explicit high-level style direction. Activates reference style alignment.",
    )
    parser.add_argument(
        "--reference-budget",
        type=int,
        default=DEFAULT_REFERENCE_BUDGET,
        help=f"Maximum sampled reference characters. Default: {DEFAULT_REFERENCE_BUDGET}.",
    )


def add_source_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--source",
        action="append",
        default=[],
        help="Factual source file for factual-document grounding, including essays and self-media. Can be repeated.",
    )
    parser.add_argument(
        "--source-budget",
        type=int,
        default=DEFAULT_SOURCE_BUDGET,
        help=f"Maximum sampled factual-source characters. Default: {DEFAULT_SOURCE_BUDGET}.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="human-writing-skills",
        description="Compile writing SKILLS and continuity context into AI-ready instructions.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    writing = subparsers.add_parser("plan-writing", help="Plan a verified multi-agent drafting project.")
    writing.add_argument("--outline", required=True)
    writing.add_argument("--output-dir", required=True)
    writing.add_argument("--style", choices=list_style_skills(), default="fiction")
    writing.add_argument("--target-length", type=int, required=True)
    writing.add_argument("--chunk-size", type=int, default=5000)
    writing.add_argument("--length-unit", choices=["characters", "words"], default="characters")
    writing.add_argument("--execution-mode", choices=["sequential", "contract"], default="sequential")
    writing.add_argument("--max-parallel", type=int, default=4)
    for option in ("context", "source", "reference"):
        writing.add_argument(f"--{option}", action="append", default=[])
    for command in ("writing-tasks", "claim-writing", "submit-writing", "verify-writing", "assemble-writing"):
        operation = subparsers.add_parser(command, help="Coordinate a long-form drafting project.")
        operation.add_argument("--package-dir", required=True)
        if command in {"claim-writing", "submit-writing"}:
            operation.add_argument("--task-id", required=True)
            operation.add_argument("--agent-id", required=True)
        if command == "submit-writing":
            operation.add_argument("--result", required=True, help="JSON result file matching the claimed task schema.")
        if command == "assemble-writing":
            operation.add_argument("--output", required=True)
    editorial = subparsers.add_parser("evaluate-editorial", help="Aggregate recorded blind-review ballots; never generate scores.")
    editorial.add_argument("--cases", required=True)
    editorial.add_argument("--format", choices=["markdown", "json"], default="markdown")

    critique = subparsers.add_parser("critique", help="Compile a diagnosis-only prompt; no replacement prose.")
    critique.add_argument("--draft", required=True)
    critique.add_argument("--style", required=True, choices=list_style_skills())
    critique.add_argument("--brief", help="Reader purpose and authoritative material file.")
    critique.add_argument("--output", help="Prompt output file; default stdout.")
    blind = subparsers.add_parser("compare-blind", help="Prepare randomly ordered A/B prompt and a separate private version key.")
    blind.add_argument("--original", required=True)
    blind.add_argument("--candidate", required=True)
    blind.add_argument("--style", required=True, choices=list_style_skills())
    blind.add_argument("--brief", help="Reader purpose and authoritative material file.")
    blind.add_argument("--output-dir", required=True, help="New or empty directory; keep version-key.json away from the reviewer.")

    list_parser = subparsers.add_parser("list", help="List available writing skills.")
    list_parser.add_argument(
        "--kind",
        choices=["all", "style", "module", "rule"],
        default="all",
        help="Filter skills by kind.",
    )
    list_parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Rule catalog output format. Ignored for skill-name lists.",
    )

    build = subparsers.add_parser("build", help="Build an instruction pack.")
    build.add_argument("--style", help="Skill name, such as fiction or news-report. May come from .humanwriting.json.")
    build.add_argument(
        "--module",
        action="append",
        default=[],
        help="Optional technique module. Can be provided multiple times.",
    )
    build.add_argument(
        "--review",
        action="store_true",
        help="Add a compact editor loop and AI-trace rubric.",
    )
    build.add_argument(
        "--deep-review",
        action="store_true",
        help="Add compact review plus relationship, cliche, structure, progress, and narrative number audits.",
    )
    build.add_argument(
        "--strict-continuity",
        action="store_true",
        help="Add occupancy, spatial blocking, and appearance/prop generation guards.",
    )
    build.add_argument(
        "--number-sense",
        action="store_true",
        help="Add dynamic number necessity review for false precision.",
    )
    build.add_argument("--context", help="Optional Markdown continuity ledger or source notes.")
    build.add_argument(
        "--original",
        help="Original text file for a rewrite. Activates semantic-fidelity protection.",
    )
    build.add_argument("--task", required=True, help="Writing task to perform.")
    build.add_argument(
        "--protect-content",
        action="store_true",
        help="Explicitly protect factual spans; serious academic/news output enables this automatically.",
    )
    build.add_argument(
        "--protect-term",
        action="append",
        default=[],
        help="Exact term that generated prose must preserve. Can be repeated.",
    )
    add_reference_arguments(build)
    add_source_arguments(build)

    humanize = subparsers.add_parser(
        "humanize",
        help="Build a focused rewrite prompt that reduces formulaic AI tone without flattening voice.",
    )
    humanize.add_argument("--draft", required=True, help="Original Markdown/text file to humanize.")
    humanize.add_argument(
        "--style",
        choices=list_style_skills(),
        help="Genre contract for the rewrite. May come from .humanwriting.json.",
    )
    humanize.add_argument(
        "--mode",
        choices=["quick", "deep"],
        default="quick",
        help="Quick loads the minimum rewrite stack; deep adds structural editor passes.",
    )
    humanize.add_argument(
        "--task",
        help="Optional rewrite direction. The default preserves language, genre, meaning, and voice.",
    )
    humanize.add_argument("--context", help="Optional continuity ledger or prior chapters.")
    humanize.add_argument(
        "--module",
        action="append",
        default=[],
        help="Optional extra technique module. Can be repeated.",
    )
    humanize.add_argument(
        "--strict-continuity",
        action="store_true",
        help="Add occupancy, spatial blocking, and appearance/prop rewrite guards.",
    )
    humanize.add_argument(
        "--with-examples",
        action="store_true",
        help="Load the on-demand before/after example library.",
    )
    humanize.add_argument(
        "--protect-content",
        action="store_true",
        help="Explicitly protect factual spans; serious document styles enable this automatically.",
    )
    humanize.add_argument(
        "--protect-term",
        action="append",
        default=[],
        help="Exact term the rewrite must preserve. Can be repeated.",
    )
    add_reference_arguments(humanize)
    add_source_arguments(humanize)

    audit = subparsers.add_parser("audit", help="Build a forensic audit pack for an existing draft.")
    audit.add_argument("--draft", required=True, help="Markdown/text file containing the draft to audit.")
    audit.add_argument("--context", help="Optional Markdown continuity ledger or source notes.")
    audit.add_argument(
        "--original",
        help="Pre-rewrite original. Automatically adds the fidelity profile.",
    )
    audit.add_argument(
        "--module",
        action="append",
        default=[],
        help="Optional extra audit module. Can be provided multiple times.",
    )
    audit.add_argument(
        "--profile",
        action="append",
        choices=["full", *PIPELINE_PROFILES],
        help="Audit profile. Can be repeated. Defaults to full.",
    )
    audit.add_argument(
        "--strict-continuity",
        default=True,
        action="store_true",
        help="Include physical checks in the default full profile. Enabled by default.",
    )
    audit.add_argument(
        "--no-strict-continuity",
        dest="strict_continuity",
        action="store_false",
        help="Remove physical checks from the default full profile.",
    )
    audit.add_argument(
        "--numbers",
        action="store_true",
        help="Legacy alias that adds the numbers profile to the selected audit.",
    )
    add_reference_arguments(audit)
    add_source_arguments(audit)
    audit.add_argument(
        "--document-type",
        choices=["auto", "general", "fiction", "webnovel", "self-media", "argumentative", "academic-paper", "formal-document", "news-report", "legal", "technical"],
        default="auto",
        help="Controls serious-document protection. Auto requires strong textual evidence.",
    )
    audit.add_argument(
        "--protect-content",
        action="store_true",
        help="Add a manifest for numbers, citations, equations, URLs, code, quotes, and explicit terms.",
    )
    audit.add_argument(
        "--protect-term",
        action="append",
        default=[],
        help="Exact protected term. Can be repeated.",
    )

    pipeline = subparsers.add_parser(
        "pipeline",
        help="Write independent multi-stage audit prompt files for a draft.",
    )
    pipeline.add_argument("--draft", required=True, help="Markdown/text draft to audit.")
    pipeline.add_argument("--context", help="Optional continuity ledger or source notes.")
    pipeline.add_argument(
        "--original",
        help="Pre-rewrite original. Adds one isolated fidelity stage.",
    )
    pipeline.add_argument(
        "--output-dir",
        help="Output directory. Defaults to <draft-name>-audit-pipeline.",
    )
    add_reference_arguments(pipeline)
    add_source_arguments(pipeline)
    pipeline.add_argument(
        "--document-type",
        choices=["auto", "general", "fiction", "webnovel", "self-media", "argumentative", "academic-paper", "formal-document", "news-report", "legal", "technical"],
        default="auto",
        help="Controls serious-document protection. Auto requires strong textual evidence.",
    )
    pipeline.add_argument(
        "--protect-content",
        action="store_true",
        help="Include a protected-content manifest in every generated stage.",
    )
    pipeline.add_argument(
        "--protect-term",
        action="append",
        default=[],
        help="Exact protected term. Can be repeated.",
    )
    pipeline.add_argument(
        "--lint-style",
        choices=["general", *list_style_skills()],
        default="general",
        help="Genre tolerance profile for the deterministic preflight lint.",
    )
    pipeline.add_argument(
        "--lint-allow",
        action="append",
        default=[],
        help="Allowed lint rule id or category. Can be repeated.",
    )
    pipeline.add_argument(
        "--with-stats",
        action="store_true",
        help="Also write optional deterministic style-statistics preflight files.",
    )
    selection = pipeline.add_mutually_exclusive_group()
    selection.add_argument(
        "--auto",
        action="store_true",
        help="Keep core stages and add optional stages only when the draft contains matching cues.",
    )
    selection.add_argument(
        "--stage",
        action="append",
        choices=PIPELINE_PROFILES,
        help="Explicit stage. Can be repeated. Without --auto or --stage, the established broad stages are written.",
    )

    chunk_audit = subparsers.add_parser(
        "chunk-audit",
        help="Split a long manuscript or report into bounded style and continuity audit passes.",
    )
    chunk_audit.add_argument("--draft", required=True, help="Long Markdown/text draft to audit.")
    chunk_audit.add_argument(
        "--style",
        choices=list_style_skills(),
        help="Genre contract used for style-drift interpretation. May come from .humanwriting.json.",
    )
    chunk_audit.add_argument(
        "--context",
        "--outline",
        dest="context",
        help="Outline, character bible, report plan, or continuity ledger used as canonical context.",
    )
    chunk_audit.add_argument(
        "--output-dir",
        help="Output directory. Defaults to <draft-name>-long-form-audit.",
    )
    chunk_audit.add_argument(
        "--chunk-size",
        type=int,
        default=DEFAULT_CHUNK_SIZE,
        help=f"Maximum target characters in each unique audit body. Default: {DEFAULT_CHUNK_SIZE}.",
    )
    chunk_audit.add_argument(
        "--overlap",
        type=int,
        default=DEFAULT_OVERLAP_SIZE,
        help=f"Read-only lead-in characters from the preceding block. Default: {DEFAULT_OVERLAP_SIZE}.",
    )
    chunk_audit.add_argument(
        "--baseline-chunk",
        type=int,
        default=1,
        help="One-based candidate manuscript chunk used as the style baseline when no reference file is supplied.",
    )
    chunk_audit.add_argument(
        "--context-budget",
        type=int,
        default=DEFAULT_CONTEXT_BUDGET,
        help=f"Maximum sampled outline/context characters per audit prompt. Default: {DEFAULT_CONTEXT_BUDGET}.",
    )
    chunk_audit.add_argument(
        "--baseline-budget",
        type=int,
        default=DEFAULT_BASELINE_BUDGET,
        help=f"Maximum sampled baseline/reference characters per audit prompt. Default: {DEFAULT_BASELINE_BUDGET}.",
    )
    chunk_audit.add_argument(
        "--reference",
        action="append",
        default=[],
        help="Explicit approved style reference. Can be repeated; overrides the baseline chunk for style evidence.",
    )
    chunk_audit.add_argument(
        "--reference-style",
        help="Explicit high-level style direction. Never activates without this flag or --reference.",
    )
    add_source_arguments(chunk_audit)
    chunk_audit.add_argument(
        "--agent-mode",
        choices=sorted(AGENT_MODES),
        default="standard",
        help="standard creates one complete task per chunk; deep adds narrowly scoped specialist tasks and coverage receipts.",
    )
    chunk_audit.add_argument(
        "--translationese",
        action="store_true",
        help="Add translationese and cross-language fidelity review. Use only for an explicitly translated or localized draft.",
    )
    chunk_audit.add_argument(
        "--book-level",
        action="store_true",
        help="Add one evidence-backed whole-book architecture stage for fiction/webnovels with at least three chapters.",
    )

    verify_chunk_audit = subparsers.add_parser(
        "verify-chunk-audit",
        help="Verify that every planned long-form agent task returned a usable coverage receipt.",
    )
    verify_chunk_audit.add_argument(
        "--package-dir",
        required=True,
        help="Directory written by chunk-audit.",
    )
    verify_chunk_audit.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format.",
    )

    lint = subparsers.add_parser(
        "lint",
        help="Run deterministic writing-pattern checks with evidence locations.",
    )
    lint.add_argument("--draft", required=True, help="Markdown/text file to inspect.")
    lint.add_argument(
        "--style",
        choices=["general", *list_style_skills()],
        default="general",
        help="Genre tolerance profile.",
    )
    lint.add_argument(
        "--format",
        choices=["markdown", "json", "github"],
        default="markdown",
        help="Output format.",
    )
    lint.add_argument(
        "--source-name",
        help="File name used by --format github when --draft - reads standard input.",
    )
    lint.add_argument(
        "--allow",
        action="append",
        default=[],
        help="Allowed rule id or category. Can be repeated.",
    )
    lint.add_argument(
        "--fail-score",
        type=int,
        help="Return exit code 1 when the transparent pattern score reaches this value.",
    )

    stats = subparsers.add_parser(
        "stats",
        help="Report optional language-aware style statistics without authorship claims.",
    )
    stats.add_argument("--draft", required=True, help="Markdown/text file to inspect.")
    stats.add_argument("--language", default="auto", help="Language tag, e.g. en, de, pt-BR; auto uses heuristic detection.")
    stats.add_argument(
        "--style",
        choices=["general", *list_style_skills()],
        default="general",
        help="Genre tolerance profile.",
    )
    stats.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format.",
    )

    extract_ledger = subparsers.add_parser(
        "extract-ledger",
        help="Compile an evidence-backed continuity-ledger extraction prompt; it never invents canon locally.",
    )
    extract_ledger.add_argument("--draft", required=True, help="Manuscript file to extract, or - for standard input.")
    extract_ledger.add_argument("--context", help="Existing ledger to preserve and update cautiously.")
    extract_ledger.add_argument("--output", help="Write the extraction prompt to this Markdown file instead of standard output.")

    fix = subparsers.add_parser(
        "fix",
        help="Preview conservative mechanical fixes; semantic rewriting is never automatic.",
    )
    fix.add_argument("--draft", required=True, help="Markdown/text file to inspect.")
    fix_mode = fix.add_mutually_exclusive_group()
    fix_mode.add_argument(
        "--preview",
        action="store_true",
        help="Preview only. This is the default when no write option is supplied.",
    )
    fix_mode.add_argument(
        "--apply",
        action="store_true",
        help="Write the conservative candidate back to the original file.",
    )
    fix.add_argument(
        "--output",
        help="Write the conservative candidate to a separate file.",
    )
    fix.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Preview/report format.",
    )

    verify = subparsers.add_parser(
        "verify",
        help="Compare protected numbers, citations, equations, URLs, code, quotes, and terms after rewriting.",
    )
    verify.add_argument("--source", required=True, help="Original source file.")
    verify.add_argument("--candidate", required=True, help="Rewritten candidate file.")
    verify.add_argument(
        "--protect-term",
        action="append",
        default=[],
        help="Additional exact term to compare. Can be repeated.",
    )
    verify.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format.",
    )
    fidelity = subparsers.add_parser(
        "verify-fidelity",
        help="Locate every changed claim span and semantic-risk cue after rewriting; changed prose never passes automatically.",
    )
    fidelity.add_argument("--source", required=True, help="Pre-rewrite source file.")
    fidelity.add_argument("--candidate", required=True, help="Rewritten candidate file.")
    fidelity.add_argument("--protect-term", action="append", default=[], help="Additional exact term; repeatable.")
    fidelity.add_argument("--format", choices=["markdown", "json"], default="markdown")
    evaluation = subparsers.add_parser(
        "evaluate", help="Run labeled multilingual document-routing and rewrite-fidelity benchmarks."
    )
    evaluation.add_argument("--cases", required=True, help="JSON case file with provenance and review status.")
    evaluation.add_argument("--format", choices=["markdown", "json"], default="markdown")
    return parser


def _stdin_draft(path: str) -> str | None:
    return sys.stdin.read() if path == "-" else None


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    raw_args = list(argv if argv is not None else sys.argv[1:])
    parse_args = [item for item in raw_args if item != "--no-project-config"]
    args = parser.parse_args(parse_args)
    try:
        apply_project_defaults(args, raw_args)
    except ValueError as exc:
        parser.error(str(exc))
    if args.command in {"build", "humanize", "chunk-audit"} and not args.style:
        parser.error("--style is required unless .humanwriting.json supplies a style default.")

    if args.command == "list":
        if args.kind == "rule":
            catalog = lint_rule_catalog()
            if args.format == "json":
                print(json.dumps(catalog, ensure_ascii=False, indent=2))
            else:
                print("# Writing Pattern Rules\n")
                for item in catalog:
                    print(f"- `{item['id']}` ({item['severity']}, `{item['category']}`): {item['message']}")
            return 0
        if args.kind == "style":
            skills = list_style_skills()
        elif args.kind == "module":
            skills = list_module_skills()
        else:
            skills = list_skills()
        for skill in skills:
            print(skill)
        return 0

    if args.command in {"plan-writing", "writing-tasks", "claim-writing", "submit-writing", "verify-writing", "assemble-writing"}:
        from . import writing_queue

        try:
            if args.command == "plan-writing":
                report = writing_queue.plan_long_form_writing(
                    args.outline, args.output_dir, style=args.style,
                    target_length=args.target_length, chunk_size=args.chunk_size,
                    length_unit=args.length_unit, execution_mode=args.execution_mode,
                    max_parallel=args.max_parallel, context_paths=args.context,
                    source_paths=args.source, reference_paths=args.reference,
                )
            elif args.command == "writing-tasks":
                report = writing_queue.list_writing_tasks(args.package_dir)
            elif args.command == "claim-writing":
                report = writing_queue.claim_writing_task(args.package_dir, args.task_id, args.agent_id)
            elif args.command == "submit-writing":
                result = json.loads(Path(args.result).read_text(encoding="utf-8"))
                if not isinstance(result, dict):
                    raise ValueError("Result JSON must be an object.")
                report = writing_queue.submit_writing_result(args.package_dir, args.task_id, result, args.agent_id)
            elif args.command == "verify-writing":
                report = writing_queue.verify_writing_project(args.package_dir)
            else:
                report = writing_queue.assemble_writing_project(args.package_dir, args.output)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            print(json.dumps({"error": str(exc)}, ensure_ascii=False))
            return 1
        print(json.dumps(report, ensure_ascii=False, indent=2))
        if args.command == "verify-writing":
            return 0 if report.get("ready_for_assembly", report.get("ok", False)) else 1
        return 0

    if args.command == "evaluate-editorial":
        try:
            report = evaluate_editorial_cases(args.cases)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            parser.error(str(exc))
        print(format_editorial_evaluation(report, args.format), end="")
        return 0

    if args.command in {"critique", "compare-blind"}:
        try:
            brief = Path(args.brief).read_text(encoding="utf-8") if args.brief else ""
            if args.command == "critique":
                prompt = compile_critique_prompt(Path(args.draft).read_text(encoding="utf-8"), args.style, brief)
                if args.output:
                    Path(args.output).write_text(prompt, encoding="utf-8")
                else:
                    print(prompt, end="")
            else:
                directory = Path(args.output_dir)
                if directory.exists() and any(directory.iterdir()):
                    raise ValueError("Comparison output directory must be new or empty.")
                prompt, key = prepare_blind_comparison(
                    Path(args.original).read_text(encoding="utf-8"),
                    Path(args.candidate).read_text(encoding="utf-8"), args.style, brief,
                )
                directory.mkdir(parents=True, exist_ok=True)
                (directory / "comparison.md").write_text(prompt, encoding="utf-8")
                (directory / "version-key.json").write_text(json.dumps(key, indent=2) + "\n", encoding="utf-8")
                print("Send only comparison.md to an independent reviewer; retain version-key.json locally.")
        except (OSError, ValueError) as exc:
            parser.error(str(exc))
        return 0

    if args.command == "build":
        try:
            prompt = compile_prompt(
                style=args.style,
                task=args.task,
                context_path=args.context,
                modules=args.module,
                review=args.review,
                strict_continuity=args.strict_continuity,
                number_sense=args.number_sense,
                deep_review=args.deep_review,
                reference_paths=args.reference,
                reference_style=args.reference_style,
                reference_budget=args.reference_budget,
                source_paths=args.source,
                source_budget=args.source_budget,
                original_path=args.original,
                protect_content=args.protect_content,
                protect_terms=args.protect_term,
            )
        except (FileNotFoundError, OSError, ValueError) as exc:
            parser.error(str(exc))
        print(prompt, end="")
        return 0

    if args.command == "humanize":
        try:
            draft_text = _stdin_draft(args.draft)
            arguments = {
                "style": args.style,
                "mode": args.mode,
                "task": args.task,
                "context_path": args.context,
                "modules": args.module,
                "strict_continuity": args.strict_continuity,
                "with_examples": args.with_examples,
                "reference_paths": args.reference,
                "reference_style": args.reference_style,
                "reference_budget": args.reference_budget,
                "source_paths": args.source,
                "source_budget": args.source_budget,
                "protect_content": args.protect_content,
                "protect_terms": args.protect_term,
            }
            prompt = (
                compile_humanize_prompt_text(draft_text, **arguments)
                if draft_text is not None
                else compile_humanize_prompt(draft_path=args.draft, **arguments)
            )
        except (FileNotFoundError, OSError, ValueError) as exc:
            parser.error(str(exc))
        print(prompt, end="")
        return 0

    if args.command == "audit":
        try:
            draft_text = _stdin_draft(args.draft)
            arguments = {
                "context_path": args.context,
                "modules": args.module,
                "strict_continuity": args.strict_continuity,
                "number_sense": args.numbers,
                "profiles": args.profile,
                "reference_paths": args.reference,
                "reference_style": args.reference_style,
                "reference_budget": args.reference_budget,
                "source_paths": args.source,
                "source_budget": args.source_budget,
                "original_path": args.original,
                "protect_content": args.protect_content,
                "protect_terms": args.protect_term,
                "document_type": args.document_type,
            }
            prompt = (
                compile_audit_prompt_text(draft_text, **arguments)
                if draft_text is not None
                else compile_audit_prompt(draft_path=args.draft, **arguments)
            )
        except (FileNotFoundError, OSError, ValueError) as exc:
            parser.error(str(exc))
        print(prompt, end="")
        return 0

    if args.command == "pipeline":
        output_dir = args.output_dir or f"{Path(args.draft).stem}-audit-pipeline"
        try:
            output, stages = write_audit_pipeline(
                args.draft,
                output_dir,
                context_path=args.context,
                stages=args.stage,
                auto=args.auto,
                reference_paths=args.reference,
                reference_style=args.reference_style,
                reference_budget=args.reference_budget,
                source_paths=args.source,
                source_budget=args.source_budget,
                original_path=args.original,
                protect_content=args.protect_content,
                protect_terms=args.protect_term,
                document_type=args.document_type,
                lint_style=args.lint_style,
                lint_allow=set(args.lint_allow),
                with_stats=args.with_stats,
            )
        except (FileNotFoundError, OSError, ValueError) as exc:
            parser.error(str(exc))
        print(f"Wrote {len(stages)} independent audit stages to {output.resolve()}")
        for stage in stages:
            print(f"{stage.order:02d} {stage.profile}: {stage.reason}")
        return 0

    if args.command == "chunk-audit":
        output_dir = args.output_dir or f"{Path(args.draft).stem}-long-form-audit"
        try:
            output, chunks = write_long_form_audit(
                args.draft,
                output_dir,
                style=args.style,
                context_path=args.context,
                reference_paths=args.reference,
                reference_style=args.reference_style,
                chunk_size=args.chunk_size,
                overlap=args.overlap,
                baseline_chunk=args.baseline_chunk,
                context_budget=args.context_budget,
                baseline_budget=args.baseline_budget,
                source_paths=args.source,
                source_budget=args.source_budget,
                agent_mode=args.agent_mode,
                translationese=args.translationese,
                book_level=args.book_level,
            )
        except (FileNotFoundError, OSError, ValueError) as exc:
            parser.error(str(exc))
        print(f"Wrote {len(chunks)} bounded long-form audit chunks to {output.resolve()}")
        print("Run the baseline, all tasks in agent-plan.json, verify coverage, then reconcile.")
        return 0

    if args.command == "verify-chunk-audit":
        try:
            report = verify_long_form_package(args.package_dir)
        except (FileNotFoundError, OSError, ValueError, json.JSONDecodeError) as exc:
            parser.error(str(exc))
        print(format_long_form_verification(report, args.format), end="")
        if not report["ready_for_reconciliation"]:
            return 1
        return 0

    if args.command == "lint":
        try:
            draft_text = _stdin_draft(args.draft)
            report = (
                lint_text(draft_text, style=args.style, allow=set(args.allow))
                if draft_text is not None
                else lint_file(args.draft, style=args.style, allow=set(args.allow))
            )
        except (FileNotFoundError, OSError, ValueError) as exc:
            parser.error(str(exc))
        source_name = args.source_name or ("stdin.md" if args.draft == "-" else args.draft)
        print(format_lint_report(report, args.format, source_name=source_name), end="")
        if args.fail_score is not None and report.score >= args.fail_score:
            return 1
        return 0

    if args.command == "stats":
        try:
            draft_text = _stdin_draft(args.draft)
            report = (
                analyze_style_statistics(draft_text, style=args.style, language=args.language)
                if draft_text is not None
                else analyze_style_file(args.draft, style=args.style, language=args.language)
            )
        except (FileNotFoundError, OSError, ValueError) as exc:
            parser.error(str(exc))
        print(format_style_statistics(report, args.format), end="")
        return 0

    if args.command == "extract-ledger":
        try:
            draft_text = _stdin_draft(args.draft)
            prompt = (
                compile_ledger_extraction_prompt_text(
                    draft_text,
                    Path(args.context).read_text(encoding="utf-8") if args.context else "",
                )
                if draft_text is not None
                else compile_ledger_extraction_prompt(args.draft, args.context)
            )
            if args.output:
                Path(args.output).write_text(prompt, encoding="utf-8")
                print(f"Wrote evidence-backed ledger extraction prompt to {Path(args.output).resolve()}")
            else:
                print(prompt, end="")
        except (FileNotFoundError, OSError, ValueError) as exc:
            parser.error(str(exc))
        return 0

    if args.command == "fix":
        if args.preview and args.output:
            parser.error("--preview cannot be combined with --output.")
        if args.apply and args.output:
            parser.error("--apply cannot be combined with --output.")
        try:
            report = fix_file(args.draft, output_path=args.output, apply=args.apply)
        except (FileNotFoundError, OSError, ValueError) as exc:
            parser.error(str(exc))
        print(format_fix_report(report, args.format), end="")
        return 0

    if args.command == "verify":
        try:
            report = compare_protected_files(
                args.source,
                args.candidate,
                terms=args.protect_term,
            )
        except (FileNotFoundError, OSError, ValueError) as exc:
            parser.error(str(exc))
        print(format_protection_report(report, args.format), end="")
        return 0 if report.ok else 1

    if args.command == "verify-fidelity":
        try:
            report = compare_fidelity_files(args.source, args.candidate, args.protect_term)
        except (FileNotFoundError, OSError, ValueError) as exc:
            parser.error(str(exc))
        print(format_fidelity_report(report, args.format), end="")
        return {"pass-exact": 0, "fail-literal": 1, "needs-review": 2}[report.status]

    if args.command == "evaluate":
        try:
            report = evaluate_cases(args.cases)
        except (FileNotFoundError, OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            parser.error(str(exc))
        print(format_evaluation(report, args.format), end="")
        return 0 if all(row["passed"] for row in report["cases"]) else 1

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
