#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = ROOT / "assets" / "templates"

BUILTIN_TEMPLATES = {
    "modern-blue": {
        "file": TEMPLATE_DIR / "modern-blue.docx",
        "description": "Clean report style with strong blue headings.",
    },
    "executive-serif": {
        "file": TEMPLATE_DIR / "executive-serif.docx",
        "description": "Formal memo style with serif typography.",
    },
    "warm-notebook": {
        "file": TEMPLATE_DIR / "warm-notebook.docx",
        "description": "Warm editorial style with softer accent colors.",
    },
    "minimal-gray": {
        "file": TEMPLATE_DIR / "minimal-gray.docx",
        "description": "Low-contrast documentation style.",
    },
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert Markdown files or Markdown strings into polished DOCX documents."
    )
    parser.add_argument("--input-file", type=Path, help="Absolute or relative path to a Markdown file.")
    parser.add_argument("--markdown", help="Raw Markdown string to convert.")
    parser.add_argument("--output", type=Path, help="Path to the output .docx file.")
    parser.add_argument(
        "--template",
        type=Path,
        help="Custom reference DOCX template. Overrides --builtin-template when provided.",
    )
    parser.add_argument(
        "--builtin-template",
        choices=sorted(BUILTIN_TEMPLATES.keys()),
        default="modern-blue",
        help="Built-in template name when no custom --template is provided.",
    )
    parser.add_argument("--metadata-file", type=Path, help="Pandoc metadata file, usually YAML.")
    parser.add_argument("--resource-path", help="Extra pandoc resource path for linked assets.")
    parser.add_argument("--title")
    parser.add_argument("--author")
    parser.add_argument("--date")
    parser.add_argument("--toc", action="store_true", help="Insert a table of contents.")
    parser.add_argument(
        "--number-sections",
        action="store_true",
        help="Number document headings in the output.",
    )
    parser.add_argument(
        "--highlight-style",
        default="tango",
        help="Pandoc syntax highlighting style. Default: tango.",
    )
    parser.add_argument(
        "--list-templates",
        action="store_true",
        help="Print built-in template names and exit.",
    )
    parser.add_argument(
        "--print-command",
        action="store_true",
        help="Print the pandoc command before running it.",
    )
    return parser


def ensure_pandoc() -> str:
    pandoc = shutil.which("pandoc")
    if not pandoc:
        raise SystemExit("pandoc is required but was not found on PATH.")
    return pandoc


def list_templates() -> None:
    payload = []
    for name, config in BUILTIN_TEMPLATES.items():
        payload.append(
            {
                "name": name,
                "path": str(config["file"]),
                "description": config["description"],
                "exists": config["file"].exists(),
            }
        )
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def validate_args(args: argparse.Namespace) -> None:
    if args.list_templates:
        return
    if bool(args.input_file) == bool(args.markdown):
        raise SystemExit("Provide exactly one of --input-file or --markdown.")
    if args.input_file and not args.input_file.exists():
        raise SystemExit(f"Input Markdown file not found: {args.input_file}")
    if args.template and not args.template.exists():
        raise SystemExit(f"Template file not found: {args.template}")
    if args.metadata_file and not args.metadata_file.exists():
        raise SystemExit(f"Metadata file not found: {args.metadata_file}")


def resolve_output(args: argparse.Namespace) -> Path:
    if args.output:
        return args.output.expanduser().resolve()
    if args.input_file:
        return args.input_file.expanduser().resolve().with_suffix(".docx")
    raise SystemExit("--output is required when using --markdown.")


def resolve_template(args: argparse.Namespace) -> Path:
    if args.template:
        return args.template.expanduser().resolve()
    template_path = BUILTIN_TEMPLATES[args.builtin_template]["file"]
    if not template_path.exists():
        raise SystemExit(
            f"Built-in template is missing: {template_path}. "
            "Run scripts/build_builtin_templates.py to regenerate templates."
        )
    return template_path


def base_resource_path(args: argparse.Namespace) -> str | None:
    if args.resource_path:
        return args.resource_path
    if args.input_file:
        return str(args.input_file.expanduser().resolve().parent)
    return None


def build_command(
    pandoc: str,
    source_path: Path,
    output_path: Path,
    template_path: Path,
    args: argparse.Namespace,
) -> list[str]:
    command = [
        pandoc,
        str(source_path),
        "--from",
        "markdown+yaml_metadata_block+emoji+footnotes+pipe_tables+grid_tables+task_lists+fenced_divs+fenced_code_attributes+raw_attribute+tex_math_dollars",
        "--to",
        "docx",
        "--standalone",
        "--reference-doc",
        str(template_path),
        "--syntax-highlighting",
        args.highlight_style,
        "--output",
        str(output_path),
    ]
    if args.metadata_file:
        command.extend(["--metadata-file", str(args.metadata_file.expanduser().resolve())])
    if args.title:
        command.extend(["--metadata", f"title={args.title}"])
    if args.author:
        command.extend(["--metadata", f"author={args.author}"])
    if args.date:
        command.extend(["--metadata", f"date={args.date}"])
    resource_path = base_resource_path(args)
    if resource_path:
        command.extend(["--resource-path", resource_path])
    if args.toc:
        command.append("--toc")
    if args.number_sections:
        command.append("--number-sections")
    return command


def run_conversion(args: argparse.Namespace) -> int:
    pandoc = ensure_pandoc()
    output_path = resolve_output(args)
    template_path = resolve_template(args)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    temp_source: tempfile.NamedTemporaryFile[str] | None = None
    try:
        if args.input_file:
            source_path = args.input_file.expanduser().resolve()
        else:
            # 使用上下文管理器确保临时文件总是被清理
            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".md",
                prefix="markdown-to-word-",
                encoding="utf-8",
                delete=False,
            ) as f:
                f.write(args.markdown)
                f.flush()
                source_path = Path(f.name)
                temp_source = f

        command = build_command(pandoc, source_path, output_path, template_path, args)
        if args.print_command:
            print(" ".join(command), file=sys.stderr)
        completed = subprocess.run(command, check=False)
        if completed.returncode != 0:
            return completed.returncode
        print(
            json.dumps(
                {
                    "output": str(output_path),
                    "template": str(template_path),
                    "builtin_template": None if args.template else args.builtin_template,
                    "source": str(source_path),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    finally:
        if temp_source is not None:
            try:
                Path(temp_source.name).unlink(missing_ok=True)
            except OSError:
                pass


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    validate_args(args)
    if args.list_templates:
        list_templates()
        return 0
    return run_conversion(args)


if __name__ == "__main__":
    raise SystemExit(main())
