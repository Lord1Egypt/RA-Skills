import argparse
import sys

from kb_writer import apply_pages, validate_pages_doc
from local_file_reader import prepare_context
from task_io import print_json, read_payload, write_result
from utils import read_json_file, write_json_file


def main():
    parser = argparse.ArgumentParser(description="Research KB local document ingest helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser("prepare", help="Validate uploaded local files and build OpenClaw analysis context")
    prepare.add_argument("--input", required=True, help="Backend payload JSON path")
    prepare.add_argument("--context-output", help="Where to write the generated context JSON")
    prepare.add_argument("--result-output", help="Optional result JSON path when there is nothing to process")

    apply = subparsers.add_parser("apply", help="Archive local source files and write generated pages to the Gitea KB")
    apply.add_argument("--input", required=True, help="Backend payload JSON path")
    apply.add_argument("--pages", required=True, help="OpenClaw-generated pages JSON path")
    apply.add_argument("--context", help="Context JSON produced by the prepare command")
    apply.add_argument("--result-output", help="Where to write the backend result JSON")

    validate = subparsers.add_parser("validate-pages", help="Validate OpenClaw-generated pages JSON without writing the KB")
    validate.add_argument("--input", required=True, help="Backend payload JSON path")
    validate.add_argument("--pages", required=True, help="OpenClaw-generated pages JSON path")
    validate.add_argument("--context", help="Context JSON produced by the prepare command")

    args = parser.parse_args()
    if args.command == "prepare":
        run_prepare(args)
    elif args.command == "apply":
        run_apply(args)
    elif args.command == "validate-pages":
        run_validate_pages(args)


def run_prepare(args):
    payload = read_payload(args.input)
    try:
        context = prepare_context(payload)
        if args.context_output:
            write_json_file(args.context_output, context)
        if not context.get("inputItems"):
            result = {
                "success": True,
                "processedSources": [],
                "createdPages": [],
                "updatedPages": [],
                "archivedFiles": [],
                "skippedSources": context.get("skippedSources") or [{"reason": "no_content_changes"}],
                "errors": [],
                "commitId": "",
                "snapshot": {"sourceId": (context.get("source") or {}).get("id"), "processedItemHashes": []},
            }
            result_path = args.result_output or payload.get("resultFile")
            if result_path:
                write_result(result_path, result)
        print_json(context)
    except Exception as exc:
        result = {"success": False, "errors": [str(exc)], "commitId": ""}
        result_path = args.result_output or payload.get("resultFile")
        if result_path:
            write_result(result_path, result)
        print_json(result)
        sys.exit(1)


def run_apply(args):
    payload = read_payload(args.input)
    try:
        pages_doc = read_json_file(args.pages)
        context = read_json_file(args.context) if args.context else {}
        result = apply_pages(payload, pages_doc, context)
        result_path = args.result_output or payload.get("resultFile")
        if result_path:
            write_result(result_path, result)
        print_json(result)
    except Exception as exc:
        result = {"success": False, "errors": [str(exc)], "commitId": ""}
        result_path = args.result_output or payload.get("resultFile")
        if result_path:
            write_result(result_path, result)
        print_json(result)
        sys.exit(1)


def run_validate_pages(args):
    payload = read_payload(args.input)
    try:
        pages_doc = read_json_file(args.pages)
        context = read_json_file(args.context) if args.context else {}
        result = validate_pages_doc(payload, pages_doc, context)
        print_json(result)
    except Exception as exc:
        print_json({"success": False, "errors": [str(exc)], "commitId": ""})
        sys.exit(1)


if __name__ == "__main__":
    main()
