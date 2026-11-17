import argparse
import json
import sys
from pathlib import Path

from maintenance_context import inspect_context, prepare_context, read_selected_pages
from overview_writer import STATUS_PATH, RUNS_PATH, apply_draft_dir, apply_pages, validate_draft_dir, validate_pages_doc, write_failure_status
from task_io import print_json, read_payload, write_result
from utils import clip, now


def main():
    parser = argparse.ArgumentParser(description="Research KB overview maintenance helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect = subparsers.add_parser("inspect", help="Read KB catalog, overview pages, and maintenance status for OpenClaw-led reasoning")
    inspect.add_argument("--input", help="Optional backend/manual payload JSON path")
    inspect.add_argument("--output", required=True, help="Where to write the inspection JSON")
    inspect.add_argument("--quiet", action="store_true", help="Suppress success stdout; errors are still printed")

    prepare = subparsers.add_parser("prepare", help="Backward-compatible alias for inspect")
    prepare.add_argument("--input", help="Optional backend/manual payload JSON path")
    prepare.add_argument("--context-output", required=True, help="Where to write the inspection JSON")
    prepare.add_argument("--result-output", help="Optional result JSON path")
    prepare.add_argument("--quiet", action="store_true", help="Suppress success stdout; errors are still printed")

    read_pages = subparsers.add_parser("read-pages", help="Read selected KB pages chosen by OpenClaw")
    read_pages.add_argument("--input", help="Optional backend/manual payload JSON path")
    read_pages.add_argument("--paths", required=True, help="Comma-separated KB page paths")
    read_pages.add_argument("--output", required=True, help="Where to write selected page evidence JSON")
    read_pages.add_argument("--quiet", action="store_true", help="Suppress success stdout; errors are still printed")

    record_failure = subparsers.add_parser("record-failure", help="Write a failed maintenance status file when cron maintenance stops before apply")
    record_failure.add_argument("--input", help="Optional backend/manual payload JSON path")
    record_failure.add_argument("--summary", default="kb_maintenance failed", help="Failure summary stored in status files")
    record_failure.add_argument("--error", action="append", default=[], help="Failure message; can be repeated")
    record_failure.add_argument("--started-at", default="", help="Optional run start timestamp")
    record_failure.add_argument("--result-output", help="Optional result JSON path")
    record_failure.add_argument("--quiet", action="store_true", help="Suppress success stdout; errors are still printed")

    validate = subparsers.add_parser("validate-pages", help="Validate overview drafts without writing the KB")
    validate.add_argument("--input", help="Optional backend/manual payload JSON path")
    validate.add_argument("--context", help="Optional inspection JSON path")
    validate.add_argument("--pages", help="Optional OpenClaw-generated overview pages JSON path")
    validate.add_argument("--draft-dir", help="Directory containing overview Markdown drafts")
    validate.add_argument("--quiet", action="store_true", help="Suppress success stdout; errors are still printed")

    apply = subparsers.add_parser("apply", help="Write changed overview pages, catalog/index, and maintenance status files")
    apply.add_argument("--input", help="Optional backend/manual payload JSON path")
    apply.add_argument("--context", help="Optional inspection JSON path")
    apply.add_argument("--pages", help="Optional OpenClaw-generated overview pages JSON path")
    apply.add_argument("--draft-dir", help="Directory containing overview Markdown drafts")
    apply.add_argument("--summary", default="", help="Human-readable maintenance summary stored in status files")
    apply.add_argument("--result-output", help="Where to write backend/manual result JSON; defaults to payload.resultFile when present")
    apply.add_argument("--quiet", action="store_true", help="Suppress success stdout; errors are still printed")

    args = parser.parse_args()
    if args.command == "inspect":
        run_inspect(args)
    elif args.command == "prepare":
        run_prepare(args)
    elif args.command == "read-pages":
        run_read_pages(args)
    elif args.command == "record-failure":
        run_record_failure(args)
    elif args.command == "validate-pages":
        run_validate_pages(args)
    elif args.command == "apply":
        run_apply(args)


def emit_success(args, data):
    if not getattr(args, "quiet", False):
        print_json(data)


def emit_error(data):
    print_json(data)


def run_inspect(args):
    payload = read_payload(args.input)
    try:
        inspection = inspect_context(payload)
        write_json_file(args.output, inspection)
        emit_success(args, inspect_summary(inspection, args.output))
    except Exception as exc:
        emit_error({"success": False, "errors": [str(exc)], "commitId": ""})
        sys.exit(1)


def run_prepare(args):
    payload = read_payload(args.input)
    try:
        inspection = prepare_context(payload)
        write_json_file(args.context_output, inspection)
        emit_success(args, inspect_summary(inspection, args.context_output))
    except Exception as exc:
        result = {"success": False, "errors": [str(exc)], "commitId": ""}
        result_path = args.result_output or payload.get("resultFile")
        if result_path:
            write_result(result_path, result)
        emit_error(result)
        sys.exit(1)


def run_read_pages(args):
    payload = read_payload(args.input)
    paths = [item.strip() for item in args.paths.split(",") if item.strip()]
    try:
        evidence = read_selected_pages(payload, paths)
        write_json_file(args.output, evidence)
        emit_success(args, {
            "success": True,
            "evidenceFile": args.output,
            "pageCount": len(evidence.get("pages") or []),
            "missingPages": evidence.get("missingPages") or [],
            "next": "Read evidenceFile, update overview Markdown drafts, then validate-pages and apply.",
        })
    except Exception as exc:
        emit_error({"success": False, "errors": [str(exc)], "commitId": ""})
        sys.exit(1)


def run_record_failure(args):
    payload = read_payload(args.input)
    started_at = args.started_at or now()
    errors = [item for item in (args.error or []) if str(item).strip()]
    if not errors:
        errors = [args.summary or "kb_maintenance failed"]
    try:
        status = write_failure_status(payload, started_at, args.summary, errors, raise_on_error=True)
        result = {
            "success": True,
            "recordedStatus": status.get("status") or "failed",
            "errors": errors,
            "statusFiles": [STATUS_PATH, RUNS_PATH],
        }
        result_path = args.result_output or payload.get("resultFile")
        if result_path:
            write_result(result_path, result)
        emit_success(args, result)
    except Exception as exc:
        emit_error({"success": False, "errors": [str(exc)], "commitId": ""})
        sys.exit(1)


def run_validate_pages(args):
    payload = read_payload(args.input)
    try:
        if args.draft_dir:
            result = validate_draft_dir(args.draft_dir)
        elif args.pages:
            context = read_json_file(args.context) if args.context else {}
            pages_doc = read_json_file(args.pages)
            result = validate_pages_doc(payload, pages_doc, context)
        else:
            raise ValueError("validate-pages requires --draft-dir or --pages")
        emit_success(args, result)
    except Exception as exc:
        emit_error({"success": False, "errors": [str(exc)], "commitId": ""})
        sys.exit(1)


def run_apply(args):
    payload = read_payload(args.input)
    started_at = now()
    try:
        if args.draft_dir:
            result = apply_draft_dir(payload, args.draft_dir, summary=args.summary, started_at=started_at)
        elif args.pages:
            context = read_json_file(args.context) if args.context else {}
            pages_doc = read_json_file(args.pages)
            result = apply_pages(payload, pages_doc, context, summary=args.summary, started_at=started_at)
        else:
            raise ValueError("apply requires --draft-dir or --pages")
        result_path = args.result_output or payload.get("resultFile")
        if result_path:
            write_result(result_path, result)
        emit_success(args, result)
    except Exception as exc:
        errors = [str(exc)]
        write_failure_status(payload, started_at, args.summary, errors)
        result = {"success": False, "errors": errors, "commitId": ""}
        result_path = args.result_output or payload.get("resultFile")
        if result_path:
            write_result(result_path, result)
        emit_error(result)
        sys.exit(1)


def inspect_summary(inspection, output_path):
    catalog = inspection.get("catalog") or {}
    return {
        "success": True,
        "mode": "inspect",
        "inspectionFile": output_path,
        "pageCount": catalog.get("pageCount") or 0,
        "overviewTargets": [item.get("path") for item in inspection.get("overviewTargets") or []],
        "recentPages": len(catalog.get("recentPages") or []),
        "stats": catalog.get("stats") or {},
        "next": "OpenClaw should choose evidence pages, run read-pages as needed, write Markdown drafts, validate, then apply.",
    }


def read_json_file(path):
    try:
        text = Path(path).read_text(encoding="utf-8-sig")
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {clip(str(exc), 500)}")


def write_json_file(path, data):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()


