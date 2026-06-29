#!/usr/bin/env python3
"""Prepare separate style and content corpora for Own Style Writer."""

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
from mineru_client import (
    API_KEY_ENV,
    DEFAULT_MAX_WAIT_MINUTES,
    DEFAULT_MODEL_VERSION,
    MODEL_VERSION_ENV,
    MinerUResult,
    can_use_agent,
    can_use_precise,
    convert_agent_file,
    convert_precise_batch,
    env_api_key,
    env_model_version,
)


DEFAULT_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
    ".ppt",
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
    ".png",
    ".jpg",
    ".jpeg",
    ".jp2",
    ".webp",
    ".gif",
    ".bmp",
}

EXTRA_BY_EXTENSION = {
    ".pdf": "pdf",
    ".docx": "docx",
    ".pptx": "pptx",
    ".xlsx": "xlsx",
    ".xls": "xls",
    ".msg": "outlook",
}

CONVERTER_CHOICES = {"auto", "mineru-precise", "mineru-agent", "markitdown"}


@dataclass
class FileTask:
    role: str
    source: Path
    input_root: Path
    output: Path
    index: int


@dataclass
class ManifestItem:
    role: str
    source: str
    output: str | None
    status: str
    extension: str
    bytes: int
    characters: int
    converter: str | None
    converter_mode: str | None
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


def safe_output_name(index: int, source: Path, input_root: Path) -> str:
    rel = source.relative_to(input_root) if is_relative_to(source, input_root) else source.name
    if isinstance(rel, Path):
        raw_stem = "__".join(rel.with_suffix("").parts)
        digest_source = str(rel)
    else:
        raw_stem = Path(rel).stem
        digest_source = str(source)
    stem = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "_", raw_stem)
    stem = re.sub(r"\s+", " ", stem).strip() or source.stem or "document"
    digest = hashlib.sha1(digest_source.encode("utf-8")).hexdigest()[:8]
    return f"{index:04d}__{stem}__{digest}.md"


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def collect_tasks(args: argparse.Namespace, output_dir: Path) -> list[FileTask]:
    extensions = parse_extensions(args.extensions)
    tasks: list[FileTask] = []

    style_dir = normalize_path(args.style_dir).resolve()
    if not style_dir.exists() or not style_dir.is_dir():
        raise FileNotFoundError(f"style directory not found: {style_dir}")

    style_files = list(iter_files(style_dir, args.recursive, extensions))
    for index, source in enumerate(style_files, start=1):
        tasks.append(
            FileTask(
                role="style",
                source=source,
                input_root=style_dir,
                output=output_dir / "style" / "converted" / safe_output_name(index, source, style_dir),
                index=index,
            )
        )

    content_sources: list[tuple[Path, Path]] = []
    if args.content_dir:
        content_dir = normalize_path(args.content_dir).resolve()
        if not content_dir.exists() or not content_dir.is_dir():
            raise FileNotFoundError(f"content directory not found: {content_dir}")
        content_sources.extend((source, content_dir) for source in iter_files(content_dir, args.recursive, extensions))

    for raw_file in args.content_file or []:
        path = normalize_path(raw_file).resolve()
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"content file not found: {path}")
        if path.suffix.lower() not in extensions:
            continue
        content_sources.append((path, path.parent))

    for index, (source, root) in enumerate(content_sources, start=1):
        tasks.append(
            FileTask(
                role="content",
                source=source,
                input_root=root,
                output=output_dir / "content" / "converted" / safe_output_name(index, source, root),
                index=index,
            )
        )

    if args.max_files:
        style_count = 0
        content_count = 0
        limited: list[FileTask] = []
        for task in tasks:
            if task.role == "style" and style_count < args.max_files:
                limited.append(task)
                style_count += 1
            elif task.role == "content" and content_count < args.max_files:
                limited.append(task)
                content_count += 1
        tasks = limited

    return tasks


def convert_workspace(args: argparse.Namespace) -> int:
    style_dir = normalize_path(args.style_dir).resolve()
    output_dir = normalize_path(args.output_dir).resolve() if args.output_dir else style_dir / ".own-style-writer"
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        tasks = collect_tasks(args, output_dir)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 2

    style_tasks = [task for task in tasks if task.role == "style"]
    if not style_tasks:
        print(f"no style files found in {style_dir}", file=sys.stderr)
        return 3

    if not any(task.role == "content" for task in tasks):
        (output_dir / "content").mkdir(parents=True, exist_ok=True)

    manifest: list[ManifestItem] = []
    handled: set[tuple[str, Path]] = set()

    if args.converter == "markitdown":
        manifest.extend(convert_with_markitdown(tasks, args))
        handled.update((task.role, task.source) for task in tasks)
    elif args.converter == "mineru-precise":
        manifest.extend(convert_with_mineru_precise(tasks, args, fallback=False))
        handled.update((task.role, task.source) for task in tasks)
    elif args.converter == "mineru-agent":
        manifest.extend(convert_with_mineru_agent(tasks, args, fallback=False))
        handled.update((task.role, task.source) for task in tasks)
    else:
        manifest.extend(convert_auto(tasks, args))
        handled.update((task.role, task.source) for task in tasks)

    if len(handled) != len(tasks):
        missing = [task for task in tasks if (task.role, task.source) not in handled]
        manifest.extend(convert_with_markitdown(missing, args))

    write_outputs(output_dir, manifest)
    failed = sum(1 for item in manifest if item.status == "failed")
    return 1 if failed and args.fail_on_error else 0


def convert_auto(tasks: list[FileTask], args: argparse.Namespace) -> list[ManifestItem]:
    manifest: list[ManifestItem] = []
    remaining = list(tasks)

    if args.allow_upload:
        if env_api_key():
            precise_items = convert_with_mineru_precise(remaining, args, fallback=True)
            manifest.extend(precise_items)
            remaining = remaining_after_success_or_nonfallback(remaining, precise_items)
        else:
            print(
                f"{API_KEY_ENV} is not set. Precise MinerU parsing is unavailable; "
                "using MinerU agent for eligible files and MarkItDown fallback.",
                flush=True,
            )
            agent_items = convert_with_mineru_agent(remaining, args, fallback=True)
            manifest.extend(agent_items)
            remaining = remaining_after_success_or_nonfallback(remaining, agent_items)
    else:
        print("upload is not allowed; using local MarkItDown fallback.", flush=True)

    if remaining:
        manifest.extend(convert_with_markitdown(remaining, args))

    return manifest


def remaining_after_success_or_nonfallback(tasks: list[FileTask], items: list[ManifestItem]) -> list[FileTask]:
    completed = {
        (item.role, Path(item.source))
        for item in items
        if item.status in {"converted", "skipped_existing"}
    }
    return [task for task in tasks if (task.role, task.source) not in completed]


def convert_with_mineru_precise(
    tasks: list[FileTask], args: argparse.Namespace, *, fallback: bool
) -> list[ManifestItem]:
    if not args.allow_upload:
        return [
            failed_item(task, "mineru", "mineru-precise", "upload is not allowed")
            for task in tasks
        ]

    api_key = env_api_key()
    if not api_key:
        return [
            failed_item(
                task,
                "mineru",
                "mineru-precise",
                f"{API_KEY_ENV} is not set; get a key from https://mineru.net/apiManage/docs",
            )
            for task in tasks
        ]

    eligible: list[FileTask] = []
    manifest: list[ManifestItem] = []
    for task in tasks:
        if task.output.exists() and not args.overwrite:
            manifest.append(existing_item(task, "mineru", "mineru-precise"))
            continue
        ok, reason = can_use_precise(task.source)
        if ok:
            eligible.append(task)
        elif not fallback:
            manifest.append(failed_item(task, "mineru", "mineru-precise", reason or "not eligible for MinerU precise"))

    by_output_dir: dict[Path, list[FileTask]] = {}
    for task in eligible:
        by_output_dir.setdefault(task.output.parent, []).append(task)

    for output_parent, group in by_output_dir.items():
        output_names = {task.source: task.output.name for task in group}
        try:
            results = convert_precise_batch(
                [task.source for task in group],
                output_parent,
                output_names,
                api_key=api_key,
                model_version=args.mineru_model or env_model_version(DEFAULT_MODEL_VERSION),
                max_wait_minutes=args.max_wait_minutes,
                poll_interval_seconds=args.poll_interval_seconds,
            )
        except Exception as exc:
            if fallback:
                continue
            for task in group:
                manifest.append(failed_item(task, "mineru", "mineru-precise", str(exc)))
            continue

        for task in group:
            result = results.get(task.source)
            if result and result.status == "converted":
                manifest.append(success_item(task, result.output or task.output, "mineru", result.mode))
            elif result and not fallback:
                manifest.append(failed_item(task, "mineru", result.mode, result.error or "MinerU precise failed"))

    return manifest


def convert_with_mineru_agent(tasks: list[FileTask], args: argparse.Namespace, *, fallback: bool) -> list[ManifestItem]:
    if not args.allow_upload:
        return [
            failed_item(task, "mineru", "mineru-agent", "upload is not allowed")
            for task in tasks
        ]

    manifest: list[ManifestItem] = []
    for task in tasks:
        if task.output.exists() and not args.overwrite:
            manifest.append(existing_item(task, "mineru", "mineru-agent"))
            continue
        ok, reason = can_use_agent(task.source)
        if not ok:
            if not fallback:
                manifest.append(failed_item(task, "mineru", "mineru-agent", reason or "not eligible for MinerU agent"))
            continue
        result = convert_agent_file(
            task.source,
            task.output,
            max_wait_minutes=args.max_wait_minutes,
            poll_interval_seconds=args.poll_interval_seconds,
        )
        if result.status == "converted":
            manifest.append(success_item(task, result.output or task.output, "mineru", result.mode))
        elif not fallback:
            manifest.append(failed_item(task, "mineru", result.mode, result.error or "MinerU agent failed"))
    return manifest


def convert_with_markitdown(tasks: list[FileTask], args: argparse.Namespace) -> list[ManifestItem]:
    try:
        from markitdown import MarkItDown
    except Exception as exc:
        return [failed_item(task, "markitdown", "local", f"cannot import markitdown: {exc}") for task in tasks]

    md = MarkItDown(enable_plugins=False)
    manifest: list[ManifestItem] = []
    for task in tasks:
        if task.output.exists() and not args.overwrite:
            manifest.append(existing_item(task, "markitdown", "local"))
            continue

        try:
            task.output.parent.mkdir(parents=True, exist_ok=True)
            result = md.convert_local(task.source)
            task.output.write_text(result.markdown, encoding="utf-8", newline="\n")
            manifest.append(success_item(task, task.output, "markitdown", "local"))
            print(f"converted [{task.role}]: {task.source.name} -> {task.output.name}", flush=True)
        except Exception as exc:
            manifest.append(failed_item(task, "markitdown", "local", repr(exc)))
            print(f"failed [{task.role}]: {task.source.name}: {exc}", file=sys.stderr, flush=True)

    return manifest


def existing_item(task: FileTask, converter: str, mode: str) -> ManifestItem:
    text = task.output.read_text(encoding="utf-8", errors="replace")
    return ManifestItem(
        role=task.role,
        source=str(task.source),
        output=str(task.output),
        status="skipped_existing",
        extension=task.source.suffix.lower(),
        bytes=task.source.stat().st_size,
        characters=len(text),
        converter=converter,
        converter_mode=mode,
    )


def success_item(task: FileTask, output: Path, converter: str, mode: str) -> ManifestItem:
    text = output.read_text(encoding="utf-8", errors="replace")
    return ManifestItem(
        role=task.role,
        source=str(task.source),
        output=str(output),
        status="converted",
        extension=task.source.suffix.lower(),
        bytes=task.source.stat().st_size,
        characters=len(text),
        converter=converter,
        converter_mode=mode,
    )


def failed_item(task: FileTask, converter: str, mode: str, error: str | None) -> ManifestItem:
    return ManifestItem(
        role=task.role,
        source=str(task.source),
        output=None,
        status="failed",
        extension=task.source.suffix.lower(),
        bytes=task.source.stat().st_size,
        characters=0,
        converter=converter,
        converter_mode=mode,
        error=error,
    )


def write_outputs(output_dir: Path, manifest: list[ManifestItem]) -> None:
    errors = [
        {
            "role": item.role,
            "source": item.source,
            "converter": item.converter,
            "converter_mode": item.converter_mode,
            "error": item.error,
        }
        for item in manifest
        if item.status == "failed"
    ]
    total_chars = sum(item.characters for item in manifest)
    converted = sum(1 for item in manifest if item.status in {"converted", "skipped_existing"})
    payload = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "output_dir": str(output_dir),
        "total_files": len(manifest),
        "converted_files": converted,
        "failed_files": len(errors),
        "total_characters": total_chars,
        "roles": {
            "style": summarize_role(manifest, "style"),
            "content": summarize_role(manifest, "content"),
        },
        "items": [asdict(item) for item in manifest],
    }
    (output_dir / "manifest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "conversion_errors.json").write_text(
        json.dumps(errors, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    for role in ("style", "content"):
        corpus = build_corpus(manifest, role)
        role_dir = output_dir / role
        role_dir.mkdir(parents=True, exist_ok=True)
        (role_dir / "corpus.md").write_text(corpus, encoding="utf-8", newline="\n")
        (output_dir / f"{role}_corpus.md").write_text(corpus, encoding="utf-8", newline="\n")


def summarize_role(manifest: list[ManifestItem], role: str) -> dict[str, int]:
    items = [item for item in manifest if item.role == role]
    return {
        "total_files": len(items),
        "converted_files": sum(1 for item in items if item.status in {"converted", "skipped_existing"}),
        "failed_files": sum(1 for item in items if item.status == "failed"),
        "total_characters": sum(item.characters for item in items),
    }


def build_corpus(manifest: list[ManifestItem], role: str) -> str:
    parts = []
    for index, item in enumerate([item for item in manifest if item.role == role and item.output], start=1):
        output = Path(item.output)
        text = output.read_text(encoding="utf-8", errors="replace").strip()
        parts.append(
            "\n".join(
                [
                    f"# {role.title()} Document {index}: {Path(item.source).name}",
                    "",
                    f"- Role: `{role}`",
                    f"- Source: `{item.source}`",
                    f"- Converted: `{item.output}`",
                    f"- Converter: `{item.converter}` / `{item.converter_mode}`",
                    f"- Characters: {item.characters}",
                    "",
                    text,
                    "",
                ]
            )
        )
    return "\n---\n\n".join(parts)


def all_candidate_files(args: argparse.Namespace) -> list[Path]:
    output_dir = normalize_path(args.output_dir).resolve() if args.output_dir else normalize_path(args.style_dir).resolve() / ".own-style-writer"
    try:
        return [task.source for task in collect_tasks(args, output_dir)]
    except Exception:
        return []


def build_worker_args(args: argparse.Namespace) -> list[str]:
    worker_args = [str(Path(__file__).resolve()), "--no-bootstrap", "--style-dir", args.style_dir]
    if args.content_dir:
        worker_args.extend(["--content-dir", args.content_dir])
    for content_file in args.content_file or []:
        worker_args.extend(["--content-file", content_file])
    if args.output_dir:
        worker_args.extend(["--output-dir", args.output_dir])
    worker_args.extend(["--converter", args.converter])
    if args.allow_upload:
        worker_args.append("--allow-upload")
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
    if args.mineru_model:
        worker_args.extend(["--mineru-model", args.mineru_model])
    if args.max_wait_minutes != DEFAULT_MAX_WAIT_MINUTES:
        worker_args.extend(["--max-wait-minutes", str(args.max_wait_minutes)])
    if args.poll_interval_seconds != 10:
        worker_args.extend(["--poll-interval-seconds", str(args.poll_interval_seconds)])
    return worker_args


def should_bootstrap_markitdown(args: argparse.Namespace) -> bool:
    return args.converter in {"auto", "markitdown"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare separate style and content corpora.")
    parser.add_argument("--style-dir", required=True, help="Directory containing writing-style reference materials.")
    parser.add_argument("--content-dir", help="Directory containing factual/source materials for this article.")
    parser.add_argument("--content-file", action="append", help="Single factual/source file. May be passed more than once.")
    parser.add_argument("--output-dir")
    parser.add_argument("--runtime-dir")
    parser.add_argument("--extensions")
    parser.add_argument("--max-files", type=int)
    parser.add_argument("--converter", choices=sorted(CONVERTER_CHOICES), default="auto")
    parser.add_argument("--allow-upload", action="store_true", help="Allow uploading local documents to MinerU.")
    parser.add_argument("--mineru-model", default="", help=f"MinerU precise model. Defaults to {MODEL_VERSION_ENV} or vlm.")
    parser.add_argument("--max-wait-minutes", type=int, default=DEFAULT_MAX_WAIT_MINUTES)
    parser.add_argument("--poll-interval-seconds", type=int, default=10)
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

    if args.no_bootstrap or not should_bootstrap_markitdown(args):
        return convert_workspace(args)

    runtime_dir = (
        normalize_path(args.runtime_dir).resolve()
        if args.runtime_dir
        else default_runtime_dir().resolve()
    )
    bootstrap_extras = args.extras
    if args.extras == "auto":
        bootstrap_extras = infer_extras(all_candidate_files(args))

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
