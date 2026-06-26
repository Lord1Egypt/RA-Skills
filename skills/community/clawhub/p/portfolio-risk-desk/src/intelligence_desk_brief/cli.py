"""CLI entrypoints for local validation of the packaged skill."""

from __future__ import annotations

import argparse
from dataclasses import replace
from datetime import date
import json
import sys

from intelligence_desk_brief.apify_bootstrap import ensure_apify_tasks
from intelligence_desk_brief.benchmarks import run_quality_benchmarks
from intelligence_desk_brief.config import AppConfig, ConfigurationError
from intelligence_desk_brief.contracts import (
    ContractValidationError,
    CreateBriefResponse,
    DeliveryTarget,
    WriteBriefToNotionInput,
)
from intelligence_desk_brief.demo import run_demo
from intelligence_desk_brief.input_parser import (
    load_fixture_request,
    load_request_from_file,
    load_request_from_saved_profile,
)
from intelligence_desk_brief.orchestrator import PortfolioRiskDesk
from intelligence_desk_brief.profiles import SavedProfile
from intelligence_desk_brief.providers.local_state import LocalWorkspaceStore


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="portfolio-risk-desk")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create-brief", help="Run the local create_brief flow.")
    source_group = create_parser.add_mutually_exclusive_group()
    source_group.add_argument("--fixture", action="store_true", help="Use the canonical fixture request.")
    source_group.add_argument("--input", help="Path to a JSON payload file matching create_brief input.")
    source_group.add_argument("--saved-profile", help="Load a saved profile by profile ID or name.")
    create_parser.add_argument(
        "--output-format",
        choices=["markdown", "json", "both"],
        default="both",
        help="Control stdout rendering.",
    )
    create_parser.add_argument(
        "--as-of-date",
        help="Override the brief date using ISO format, useful for deterministic tests.",
    )
    create_parser.add_argument("--workspace-id", help="Override the workspace identifier for the run.")
    create_parser.add_argument("--profile-id", help="Optional saved profile identifier for the run.")
    create_parser.add_argument("--profile-name", help="Optional saved profile name for the run.")
    create_parser.add_argument("--local-state-dir", help="Local state directory for workspace data.")

    demo_parser = subparsers.add_parser("run-demo", help="Run the canonical Portfolio Risk Desk demo flow.")
    demo_parser.add_argument(
        "--mode",
        choices=["happy", "provider_failure", "delivery_failure"],
        default="happy",
        help="Choose the happy path or one failure-mode rehearsal.",
    )
    demo_parser.add_argument(
        "--output-format",
        choices=["markdown", "json", "both"],
        default="both",
        help="Control stdout rendering for the demo artifact.",
    )

    benchmarks_parser = subparsers.add_parser(
        "run-benchmarks",
        help="Run the lightweight quality benchmark harness.",
    )
    benchmarks_parser.add_argument(
        "--output-format",
        choices=["json", "summary", "both"],
        default="both",
        help="Control stdout rendering for benchmark results.",
    )

    bootstrap_parser = subparsers.add_parser(
        "bootstrap-apify",
        help="Create or update the Apify tasks needed for live retrieval.",
    )
    bootstrap_parser.add_argument(
        "--include-x-signals",
        choices=["true", "false"],
        default="true",
        help="Whether to create the supplementary X signals task.",
    )

    save_profile_parser = subparsers.add_parser("save-profile", help="Persist a saved profile locally.")
    save_source_group = save_profile_parser.add_mutually_exclusive_group()
    save_source_group.add_argument("--fixture", action="store_true", help="Use the canonical fixture request.")
    save_source_group.add_argument("--input", help="Path to a JSON payload file matching create_brief input.")
    save_profile_parser.add_argument("--workspace-id", help="Workspace identifier for the saved profile.")
    save_profile_parser.add_argument("--profile-id", help="Optional saved profile identifier.")
    save_profile_parser.add_argument("--profile-name", help="Saved profile name.")
    save_profile_parser.add_argument("--local-state-dir", help="Local state directory for workspace data.")

    list_profiles_parser = subparsers.add_parser("list-profiles", help="List saved profiles in a workspace.")
    list_profiles_parser.add_argument("--workspace-id", required=True, help="Workspace identifier to inspect.")
    list_profiles_parser.add_argument("--local-state-dir", help="Local state directory for workspace data.")

    notion_parser = subparsers.add_parser(
        "write-brief-to-notion",
        help="Emit the OpenClaw-facing Notion handoff payload.",
    )
    notion_parser.add_argument("--input", required=True, help="Path to a JSON brief payload file.")
    notion_parser.add_argument(
        "--parent-page-id",
        default="local-parent-page",
        help="Parent page identifier to pass into the write call.",
    )
    notion_parser.add_argument("--workspace-id", required=True, help="Workspace identifier for the handoff.")
    notion_parser.add_argument("--profile-id", help="Optional saved profile identifier for the handoff.")
    notion_parser.add_argument("--profile-name", help="Optional saved profile name for the handoff.")
    notion_parser.add_argument("--local-state-dir", help="Local state directory for workspace data.")
    return parser


def _resolve_date(raw_value: str | None) -> date | None:
    if raw_value is None:
        return None
    return date.fromisoformat(raw_value)


def _load_request(args: argparse.Namespace, config: AppConfig):
    if getattr(args, "saved_profile", None):
        request = load_request_from_saved_profile(
            _require_local_state_dir(args, config),
            workspace_id=args.workspace_id or "guest-workspace",
            profile_ref=args.saved_profile,
            delivery_target=DeliveryTarget.INLINE,
        )
    else:
        request = load_fixture_request() if args.fixture or not args.input else load_request_from_file(args.input)
    if args.workspace_id is not None:
        request.workspace_id = args.workspace_id
    if args.profile_id is not None:
        request.profile_id = args.profile_id
    if args.profile_name is not None:
        request.profile_name = args.profile_name
    return request


def _print_create_brief_output(
    brief: CreateBriefResponse,
    markdown: str,
    output_format: str,
) -> None:
    if output_format == "markdown":
        sys.stdout.write(markdown)
        return
    if output_format == "json":
        sys.stdout.write(json.dumps(brief.to_dict(), indent=2) + "\n")
        return
    sys.stdout.write(markdown.rstrip() + "\n\n")
    sys.stdout.write(json.dumps(brief.to_dict(), indent=2) + "\n")


def _print_demo_output(result, output_format: str) -> None:
    if output_format == "markdown":
        sys.stdout.write(f"# Demo prompt\n\n{result.prompt}\n\n")
        sys.stdout.write("# Operator notes\n\n")
        for note in result.operator_notes:
            sys.stdout.write(f"- {note}\n")
        sys.stdout.write(f"\n{result.markdown}")
        return
    if output_format == "json":
        sys.stdout.write(json.dumps(result.payload, indent=2) + "\n")
        return
    sys.stdout.write(f"# Demo prompt\n\n{result.prompt}\n\n")
    sys.stdout.write("# Operator notes\n\n")
    for note in result.operator_notes:
        sys.stdout.write(f"- {note}\n")
    sys.stdout.write(f"\n{result.markdown.rstrip()}\n\n")
    sys.stdout.write(json.dumps(result.payload, indent=2) + "\n")


def _print_benchmark_output(results, output_format: str) -> None:
    payload = [
        {
            "name": result.name,
            "score": result.score,
            "max_score": result.max_score,
            "checks": result.checks,
        }
        for result in results
    ]
    if output_format == "json":
        sys.stdout.write(json.dumps(payload, indent=2) + "\n")
        return
    summary_lines = [
        f"- {result['name']}: {result['score']}/{result['max_score']} "
        f"({', '.join(name for name, passed in result['checks'].items() if passed) or 'no checks passed'})"
        for result in payload
    ]
    if output_format == "summary":
        sys.stdout.write("\n".join(summary_lines) + "\n")
        return
    sys.stdout.write("\n".join(summary_lines) + "\n\n")
    sys.stdout.write(json.dumps(payload, indent=2) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        config = AppConfig.from_env()
        if getattr(args, "local_state_dir", None):
            config = replace(config, local_state_dir=args.local_state_dir)
        runtime = PortfolioRiskDesk(config)

        if args.command == "create-brief":
            request = _load_request(args, config)
            brief, markdown = runtime.create_brief(
                request,
                as_of_date=_resolve_date(args.as_of_date),
            )
            _print_create_brief_output(brief, markdown, args.output_format)
            return 0

        if args.command == "run-demo":
            result = run_demo(args.mode)
            _print_demo_output(result, args.output_format)
            return 0

        if args.command == "run-benchmarks":
            results = run_quality_benchmarks()
            _print_benchmark_output(results, args.output_format)
            return 0

        if args.command == "bootstrap-apify":
            if not config.apify_api_token:
                raise ConfigurationError("APIFY_API_TOKEN is required to bootstrap Apify tasks.")
            payload = ensure_apify_tasks(
                token=config.apify_api_token,
                base_url=config.apify_base_url,
                include_x_signals=args.include_x_signals == "true",
            )
            sys.stdout.write(json.dumps(payload, indent=2) + "\n")
            return 0

        if args.command == "save-profile":
            request = _load_request(args, config)
            state_dir = _require_local_state_dir(args, config)
            store = LocalWorkspaceStore(state_dir)
            profile = SavedProfile.from_request(
                request,
                profile_id=args.profile_id,
                profile_name=args.profile_name,
            )
            store.save_profile(profile)
            sys.stdout.write(json.dumps(profile.to_dict(), indent=2) + "\n")
            return 0

        if args.command == "list-profiles":
            state_dir = _require_local_state_dir(args, config)
            store = LocalWorkspaceStore(state_dir)
            payload = [profile.to_dict() for profile in store.list_profiles(args.workspace_id)]
            sys.stdout.write(json.dumps(payload, indent=2) + "\n")
            return 0

        notion_input = WriteBriefToNotionInput.from_dict(
            {
                "brief_payload": json.loads(open(args.input, encoding="utf-8").read()),
                "parent_page_id": args.parent_page_id,
                "workspace_id": args.workspace_id,
                "profile_id": args.profile_id,
                "profile_name": args.profile_name,
            }
        )
        result = runtime.write_brief_to_notion(notion_input)
        sys.stdout.write(json.dumps(result.to_dict(), indent=2) + "\n")
        return 0
    except (ConfigurationError, ContractValidationError, ValueError, OSError, json.JSONDecodeError) as error:
        parser.exit(2, f"Error: {error}\n")


def _require_local_state_dir(args: argparse.Namespace, config: AppConfig) -> str:
    state_dir = getattr(args, "local_state_dir", None) or config.local_state_dir
    if not state_dir:
        raise ConfigurationError("LOCAL_STATE_DIR or --local-state-dir is required for saved profile workflows.")
    return state_dir


if __name__ == "__main__":
    raise SystemExit(main())
