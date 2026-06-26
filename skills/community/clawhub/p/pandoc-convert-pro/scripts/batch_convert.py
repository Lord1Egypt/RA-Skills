#!/usr/bin/env python3
"""Batch document conversion wrapper for pandoc-convert."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterable

SUPPORTED_EXTENSIONS = {
    ".md", ".markdown", ".mkd", ".html", ".htm", ".docx", ".odt", ".rtf",
    ".epub", ".tex", ".latex", ".typ", ".rst", ".adoc", ".asciidoc", ".org", ".ipynb", ".txt",
}
EXCLUDED_DIRS = {".git", ".hg", ".svn", "node_modules", "dist", "build", "out", "target", "__pycache__"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Batch convert documents with pandoc-convert.")
    parser.add_argument("inputs", nargs="+", help="Input files or directories")
    parser.add_argument("--output-dir", required=True, help="Directory for converted files")
    parser.add_argument("--to", required=True, help="Target format or extension, e.g. html, docx, pdf")
    parser.add_argument("--from", dest="from_format", help="Input format override for all files")
    parser.add_argument("--retries", type=int, default=1, help="Retries after a failed conversion, default: 1")
    parser.add_argument("--retry-delay", type=float, default=1.0, help="Seconds to wait between retries, default: 1")
    parser.add_argument("--fail-fast", action="store_true", help="Stop after the first failed file")
    parser.add_argument("--continue-on-error", action="store_true", help="Continue after failures and summarize them")
    parser.add_argument("--report", help="Write a Markdown summary report")
    parser.add_argument("--json-report", help="Write a JSON summary report")
    parser.add_argument("--pdf-engine", help="PDF engine passed to pandoc")
    parser.add_argument("--toc", action="store_true", help="Add table of contents")
    parser.add_argument("--standalone", "-s", action="store_true", help="Produce standalone output")
    parser.add_argument("--number-sections", action="store_true", help="Number section headings")
    parser.add_argument("--citeproc", action="store_true", help="Process citations")
    parser.add_argument("--bibliography", help="Bibliography file")
    parser.add_argument("--csl", help="Citation style file")
    parser.add_argument("--reference-doc", help="DOCX/ODT reference document")
    parser.add_argument("--template", help="Pandoc template file")
    parser.add_argument("--css", help="CSS file for HTML/EPUB")
    parser.add_argument("--resource-path", help="Resource search path")
    parser.add_argument("--skip-existing", action="store_true", help="Skip files whose output already exists")
    return parser.parse_args()


def target_extension(target: str) -> str:
    cleaned = target.strip().lower().lstrip(".")
    if not cleaned:
        raise ValueError("--to must not be empty")
    return cleaned


def should_skip_dir(path: Path, output_dir: Path) -> bool:
    if path.name.startswith("."):
        return True
    if path.name in EXCLUDED_DIRS:
        return True
    try:
        path.resolve().relative_to(output_dir.resolve())
        return True
    except ValueError:
        return False


def collect_files(inputs: Iterable[str], output_dir: Path) -> list[Path]:
    files: list[Path] = []
    for raw_input in inputs:
        input_path = Path(raw_input).expanduser()
        if input_path.is_file():
            if input_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                files.append(input_path)
            continue
        if input_path.is_dir():
            for root, dirs, names in os.walk(input_path):
                root_path = Path(root)
                dirs[:] = [name for name in dirs if not should_skip_dir(root_path / name, output_dir)]
                for name in names:
                    candidate = root_path / name
                    if candidate.name.startswith("."):
                        continue
                    if candidate.suffix.lower() in SUPPORTED_EXTENSIONS:
                        files.append(candidate)
            continue
        print(f"Skipping missing input: {input_path}", file=sys.stderr)
    return sorted(dict.fromkeys(files))


def output_for(input_file: Path, inputs: list[str], output_dir: Path, ext: str) -> Path:
    base_root = None
    for raw_input in inputs:
        candidate = Path(raw_input).expanduser()
        if candidate.is_dir():
            try:
                input_file.relative_to(candidate)
                base_root = candidate
                break
            except ValueError:
                pass
    if base_root is None:
        relative = Path(input_file.name)
    else:
        relative = input_file.relative_to(base_root)
    return (output_dir / relative).with_suffix(f".{ext}")


def build_common_args(args: argparse.Namespace) -> list[str]:
    common: list[str] = []
    if args.from_format:
        common.extend(["--from", args.from_format])
    common.extend(["--to", args.to])
    for flag, enabled in [
        ("--toc", args.toc),
        ("--standalone", args.standalone),
        ("--number-sections", args.number_sections),
        ("--citeproc", args.citeproc),
    ]:
        if enabled:
            common.append(flag)
    for option_name, value in [
        ("--pdf-engine", args.pdf_engine),
        ("--bibliography", args.bibliography),
        ("--csl", args.csl),
        ("--reference-doc", args.reference_doc),
        ("--template", args.template),
        ("--css", args.css),
        ("--resource-path", args.resource_path),
    ]:
        if value:
            common.extend([option_name, value])
    return common


def summarize_stderr(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return " | ".join(lines[-5:])[:1000]


def run_conversion(convert_script: Path, input_file: Path, output_file: Path, common_args: list[str], retries: int, retry_delay: float) -> dict:
    attempts = 0
    last_result = None
    while attempts <= retries:
        attempts += 1
        command = ["bash", str(convert_script), str(input_file), "-o", str(output_file), *common_args]
        last_result = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if last_result.returncode == 0:
            return {
                "input": str(input_file),
                "output": str(output_file),
                "status": "success",
                "attempts": attempts,
                "exit_code": 0,
                "stderr": summarize_stderr(last_result.stderr),
            }
        if attempts <= retries:
            print(f"  Retry {attempts}/{retries} after exit {last_result.returncode}: {input_file}", flush=True)
            if retry_delay > 0:
                time.sleep(retry_delay)
    assert last_result is not None
    return {
        "input": str(input_file),
        "output": str(output_file),
        "status": "failed",
        "attempts": attempts,
        "exit_code": last_result.returncode,
        "stderr": summarize_stderr(last_result.stderr),
    }


def write_markdown_report(path: Path, results: list[dict], stats: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Pandoc Batch Conversion Report",
        "",
        f"- Succeeded: {stats['succeeded']}",
        f"- Failed: {stats['failed']}",
        f"- Skipped: {stats['skipped']}",
        "",
        "## Results",
        "",
        "| Status | Attempts | Input | Output | Error |",
        "|---|---:|---|---|---|",
    ]
    for item in results:
        error = item.get("stderr", "").replace("|", "\\|")
        lines.append(f"| {item['status']} | {item['attempts']} | `{item['input']}` | `{item['output']}` | {error} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_json_report(path: Path, results: list[dict], stats: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"summary": stats, "results": results, **stats}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    retries = max(args.retries, 0)
    output_dir = Path(args.output_dir).expanduser()
    ext = target_extension(args.to)
    skill_dir = Path(__file__).resolve().parents[1]
    convert_script = skill_dir / "scripts" / "convert.sh"
    files = collect_files(args.inputs, output_dir)
    common_args = build_common_args(args)

    if not files:
        print("No supported input files found.", file=sys.stderr)
        return 1

    output_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []
    skipped = 0

    for index, input_file in enumerate(files, start=1):
        output_file = output_for(input_file, args.inputs, output_dir, ext)
        print(f"[{index}/{len(files)}] converting {input_file} -> {output_file}", flush=True)
        if args.skip_existing and output_file.exists():
            skipped += 1
            results.append({
                "input": str(input_file),
                "output": str(output_file),
                "status": "skipped",
                "attempts": 0,
                "exit_code": 0,
                "stderr": "output exists",
            })
            continue
        output_file.parent.mkdir(parents=True, exist_ok=True)
        result = run_conversion(convert_script, input_file, output_file, common_args, retries, args.retry_delay)
        results.append(result)
        if result["status"] == "failed" and args.fail_fast:
            break

    succeeded = sum(1 for item in results if item["status"] == "success")
    failed = sum(1 for item in results if item["status"] == "failed")
    skipped = sum(1 for item in results if item["status"] == "skipped")
    stats = {"succeeded": succeeded, "failed": failed, "skipped": skipped, "total": len(results)}

    print(f"Summary: {succeeded} succeeded, {failed} failed, {skipped} skipped")
    if failed:
        print("Failed files:")
        for item in results:
            if item["status"] == "failed":
                print(f"- {item['input']} -> {item['output']} (exit {item['exit_code']}): {item['stderr']}")

    if args.report:
        write_markdown_report(Path(args.report).expanduser(), results, stats)
        print(f"Markdown report: {args.report}")
    if args.json_report:
        write_json_report(Path(args.json_report).expanduser(), results, stats)
        print(f"JSON report: {args.json_report}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
