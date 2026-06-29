#!/usr/bin/env python3
"""Convert a directory of reference documents into a Markdown style corpus."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from bootstrap_markitdown import default_runtime_dir, ensure_runtime, runtime_env


DEFAULT_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".pptx",
    ".xlsx",
    ".xls",
    ".html",
    ".htm",
    ".md",
    ".markdown",
    ".txt",
    ".csv",
    ".json",
    ".xml",
    ".epub",
    ".msg",
    ".zip",
}

EXTRA_BY_EXTENSION = {
    ".pdf": "pdf",
    ".docx": "docx",
    ".pptx": "pptx",
    ".xlsx": "xlsx",
    ".xls": "xls",
    ".msg": "outlook",
}


@dataclass
class ManifestItem:
    source: str
    output: str | None
    status: str
    extension: str
    bytes: int
    characters: int
    error: str | None = None


def normalize_path(value: str | Path) -> Path:
    text = str(value)
    if os.name != "nt":
        match = re.match(r"^([A-Za-z]):[\\/](.*)$", text)
        if match:
            drive = match.group(1).lower()
            rest = match.group(2).replace("\\", "/")
            return Path(f"/mnt/{drive}/{rest}")
    return Path(text).expanduser()


def parse_extensions(raw: str | None) -> set[str]:
    if not raw:
        return set(DEFAULT_EXTENSIONS)
    values = set()
    for item in raw.split(","):
        item = item.strip().lower()
        if not item:
            continue
        if not item.startswith("."):
            item = "." + item
        values.add(item)
    return values


def iter_files(input_dir: Path, recursive: bool, extensions: set[str]) -> Iterable[Path]:
    pattern = "**/*" if recursive else "*"
    for path in sorted(input_dir.glob(pattern)):
        if not path.is_file():
            continue
        rel = path.relative_to(input_dir)
        if any(part.startswith(".") for part in rel.parts):
            continue
        if path.suffix.lower() in extensions:
            yield path


def infer_extras(files: Iterable[Path]) -> str:
    extras = sorted(
        {
            extra
            for path in files
            for extra in [EXTRA_BY_EXTENSION.get(path.suffix.lower())]
            if extra
        }
    )
    return ",".join(extras)


def safe_output_name(index: int, source: Path, input_dir: Path) -> str:
    rel = source.relative_to(input_dir)
    stem = "__".join(rel.with_suffix("").parts)
    stem = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "_", stem)
    stem = re.sub(r"\s+", " ", stem).strip()
    digest = hashlib.sha1(str(rel).encode("utf-8")).hexdigest()[:8]
    return f"{index:04d}__{stem}__{digest}.md"


def convert_files(args: argparse.Namespace) -> int:
    input_dir = normalize_path(args.input_dir).resolve()
    if args.output_dir:
        output_dir = normalize_path(args.output_dir).resolve()
    else:
        output_dir = input_dir / ".own-style-writer"

    if not input_dir.exists() or not input_dir.is_dir():
        print(f"input directory not found: {input_dir}", file=sys.stderr)
        return 2

    converted_dir = output_dir / "converted"
    converted_dir.mkdir(parents=True, exist_ok=True)

    extensions = parse_extensions(args.extensions)
    files = list(iter_files(input_dir, args.recursive, extensions))
    if args.max_files:
        files = files[: args.max_files]

    if not files:
        print(f"no supported files found in {input_dir}", file=sys.stderr)
        return 3

    try:
        from markitdown import MarkItDown
    except Exception as exc:
        print(f"cannot import markitdown in worker runtime: {exc}", file=sys.stderr)
        return 4

    md = MarkItDown(enable_plugins=False)
    manifest: list[ManifestItem] = []
    errors: list[dict[str, str]] = []
    corpus_parts: list[str] = []

    for index, source in enumerate(files, start=1):
        output = converted_dir / safe_output_name(index, source, input_dir)
        if output.exists() and not args.overwrite:
            text = output.read_text(encoding="utf-8", errors="replace")
            item = ManifestItem(
                source=str(source),
                output=str(output),
                status="skipped_existing",
                extension=source.suffix.lower(),
                bytes=source.stat().st_size,
                characters=len(text),
            )
            manifest.append(item)
            corpus_parts.append(corpus_entry(index, source, output, text))
            continue

        try:
            result = md.convert_local(source)
            text = result.markdown
            output.write_text(text, encoding="utf-8", newline="\n")
            item = ManifestItem(
                source=str(source),
                output=str(output),
                status="converted",
                extension=source.suffix.lower(),
                bytes=source.stat().st_size,
                characters=len(text),
            )
            manifest.append(item)
            corpus_parts.append(corpus_entry(index, source, output, text))
            print(f"converted: {source.name} -> {output.name}", flush=True)
        except Exception as exc:
            message = repr(exc)
            item = ManifestItem(
                source=str(source),
                output=None,
                status="failed",
                extension=source.suffix.lower(),
                bytes=source.stat().st_size,
                characters=0,
                error=message,
            )
            manifest.append(item)
            errors.append({"source": str(source), "error": message})
            print(f"failed: {source.name}: {message}", file=sys.stderr, flush=True)

    write_outputs(output_dir, input_dir, manifest, errors, corpus_parts)
    failed = sum(1 for item in manifest if item.status == "failed")
    return 1 if failed and args.fail_on_error else 0


def corpus_entry(index: int, source: Path, output: Path, text: str) -> str:
    return "\n".join(
        [
            f"# Document {index}: {source.name}",
            "",
            f"- Source: `{source}`",
            f"- Converted: `{output}`",
            f"- Characters: {len(text)}",
            "",
            text.strip(),
            "",
        ]
    )


def write_outputs(
    output_dir: Path,
    input_dir: Path,
    manifest: list[ManifestItem],
    errors: list[dict[str, str]],
    corpus_parts: list[str],
) -> None:
    total_chars = sum(item.characters for item in manifest)
    converted = sum(1 for item in manifest if item.status in {"converted", "skipped_existing"})
    payload = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "input_dir": str(input_dir),
        "output_dir": str(output_dir),
        "total_files": len(manifest),
        "converted_files": converted,
        "failed_files": len(errors),
        "total_characters": total_chars,
        "items": [asdict(item) for item in manifest],
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "conversion_errors.json").write_text(
        json.dumps(errors, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "corpus.md").write_text(
        "\n---\n\n".join(corpus_parts),
        encoding="utf-8",
        newline="\n",
    )


def build_worker_args(args: argparse.Namespace) -> list[str]:
    worker_args = [str(Path(__file__).resolve()), "--no-bootstrap", "--input-dir", args.input_dir]
    if args.output_dir:
        worker_args.extend(["--output-dir", args.output_dir])
    if args.recursive:
        worker_args.append("--recursive")
    if args.overwrite:
        worker_args.append("--overwrite")
    if args.fail_on_error:
        worker_args.append("--fail-on-error")
    if args.extensions:
        worker_args.extend(["--extensions", args.extensions])
    if args.max_files:
        worker_args.extend(["--max-files", str(args.max_files)])
    return worker_args


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a Markdown corpus from reference documents.")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir")
    parser.add_argument("--runtime-dir")
    parser.add_argument("--extensions")
    parser.add_argument("--max-files", type=int)
    parser.add_argument(
        "--extras",
        default="auto",
        help="Comma-separated MarkItDown extras to install, or 'auto' to infer from input files.",
    )
    parser.add_argument("--recursive", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--fail-on-error", action="store_true")
    parser.add_argument("--force-bootstrap", action="store_true")
    parser.add_argument("--no-bootstrap", action="store_true")
    args = parser.parse_args()

    if args.no_bootstrap:
        return convert_files(args)

    runtime_dir = (
        normalize_path(args.runtime_dir).resolve()
        if args.runtime_dir
        else default_runtime_dir().resolve()
    )
    bootstrap_extras = args.extras
    if args.extras == "auto":
        input_dir = normalize_path(args.input_dir).resolve()
        extensions = parse_extensions(args.extensions)
        files = list(iter_files(input_dir, args.recursive, extensions))
        if args.max_files:
            files = files[: args.max_files]
        bootstrap_extras = infer_extras(files)

    try:
        python = ensure_runtime(runtime_dir, extras=bootstrap_extras, force=args.force_bootstrap)
    except Exception as exc:
        print(f"bootstrap failed: {exc}", file=sys.stderr)
        return 10

    cmd = [str(python), *build_worker_args(args)]
    print("+ " + " ".join(cmd), flush=True)
    return subprocess.run(cmd, env=runtime_env(runtime_dir)).returncode


if __name__ == "__main__":
    raise SystemExit(main())
