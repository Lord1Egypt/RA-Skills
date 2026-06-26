#!/usr/bin/env python3
"""Build a Chinese-friendly PDF from a single Markdown file via pandoc."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Iterable

PANDOC_CANDIDATES = [
    "pandoc",
    "/run/current-system/sw/bin/pandoc",
    "/opt/homebrew/bin/pandoc",
    "/usr/local/bin/pandoc",
]

ENGINE_CANDIDATES = {
    "tectonic": [
        "tectonic",
        "/opt/homebrew/bin/tectonic",
        "/run/current-system/sw/bin/tectonic",
        "/usr/local/bin/tectonic",
    ],
    "xelatex": [
        "xelatex",
        "/Library/TeX/texbin/xelatex",
        "/opt/homebrew/bin/xelatex",
        "/run/current-system/sw/bin/xelatex",
        "/usr/local/bin/xelatex",
    ],
    "lualatex": [
        "lualatex",
        "/Library/TeX/texbin/lualatex",
        "/opt/homebrew/bin/lualatex",
        "/run/current-system/sw/bin/lualatex",
        "/usr/local/bin/lualatex",
    ],
}

DEFAULT_FONTS = [
    "Hiragino Sans GB",
    "PingFang SC",
    "Noto Sans CJK SC",
    "Source Han Sans SC",
    "Songti SC",
    "STHeiti",
    "Heiti SC",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build PDF from a Markdown guide")
    parser.add_argument("--markdown", required=True, help="Input Markdown path")
    parser.add_argument("--output", required=True, help="Output PDF path")
    parser.add_argument("--title", required=True, help="Document title")
    parser.add_argument("--source-url", default="", help="Source repository URL")
    parser.add_argument("--mainfont", help="Preferred CJK font")
    parser.add_argument("--toc-depth", type=int, default=3, help="Table-of-contents depth")
    return parser.parse_args()


def resolve_binary(candidates: Iterable[str]) -> str | None:
    for candidate in candidates:
        if os.path.isabs(candidate) and os.path.exists(candidate):
            return candidate
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    return None


def choose_engine() -> tuple[str, str]:
    for engine, candidates in ENGINE_CANDIDATES.items():
        resolved = resolve_binary(candidates)
        if resolved:
            return engine, resolved
    raise RuntimeError("No PDF engine found. Install tectonic, xelatex, or lualatex.")


def build_cover(title: str, source_url: str) -> str:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"# {title}",
        "",
        f"- Source: {source_url}" if source_url else "- Source: (not provided)",
        f"- Generated: {generated_at}",
        "- Note: this guide focuses on usage, not implementation internals.",
        "",
        "\\newpage",
        "",
    ]
    return "\n".join(lines)


def ensure_single_document(markdown_path: Path, title: str, source_url: str) -> Path:
    content = markdown_path.read_text(encoding="utf-8").strip()
    if not content.startswith("# "):
        content = f"# {title}\n\n{content}" if content else f"# {title}"
    first_lines = content.splitlines()[:8]
    source_line = f"Source: {source_url}" if source_url else None
    if source_line and source_line not in first_lines:
        content = content.replace(content.splitlines()[0], content.splitlines()[0] + f"\n\n{source_line}", 1)

    build_dir = markdown_path.parent / ".build-pdf"
    build_dir.mkdir(parents=True, exist_ok=True)
    combined = build_dir / f"{markdown_path.stem}.combined.md"
    combined.write_text(build_cover(title, source_url) + "\n\n" + content + "\n", encoding="utf-8")
    return combined


def build_pdf(combined_md: Path, output_pdf: Path, title: str, mainfont: str | None, toc_depth: int) -> tuple[str, str]:
    pandoc = resolve_binary(PANDOC_CANDIDATES)
    if not pandoc:
        raise RuntimeError("Pandoc not found.")

    engine_name, engine_path = choose_engine()
    fonts = [mainfont] if mainfont else []
    fonts.extend(font for font in DEFAULT_FONTS if font not in fonts)

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []

    for font in fonts:
        command = [
            pandoc,
            str(combined_md),
            "--from",
            "markdown+raw_tex+pipe_tables+task_lists",
            "--pdf-engine",
            engine_path,
            "--toc",
            "--toc-depth",
            str(toc_depth),
            "--number-sections",
            "-V",
            f"mainfont={font}",
            "-V",
            "fontsize=11pt",
            "-V",
            "geometry:margin=1in",
            "-V",
            "papersize:a4",
            "-V",
            "colorlinks=true",
            "-V",
            "linkcolor=blue",
            "-M",
            f"title={title}",
            "-M",
            "lang=zh-CN",
            "-o",
            str(output_pdf),
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0 and output_pdf.exists() and output_pdf.stat().st_size > 0:
            return engine_name, font
        errors.append(
            f"font={font}\nstdout:\n{result.stdout.strip()}\nstderr:\n{result.stderr.strip()}"
        )

    raise RuntimeError("Pandoc PDF build failed with all font candidates.\n\n" + "\n\n---\n\n".join(errors))


def main() -> int:
    args = parse_args()
    markdown_path = Path(args.markdown).expanduser().resolve()
    output_pdf = Path(args.output).expanduser().resolve()

    if not markdown_path.exists():
        print(f"[ERROR] Markdown file not found: {markdown_path}", file=sys.stderr)
        return 1

    try:
        combined = ensure_single_document(markdown_path, args.title, args.source_url)
        engine_name, font = build_pdf(
            combined_md=combined,
            output_pdf=output_pdf,
            title=args.title,
            mainfont=args.mainfont,
            toc_depth=args.toc_depth,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    print(f"[OK] Combined markdown: {combined}")
    print(f"[OK] PDF: {output_pdf}")
    print(f"[OK] Engine: {engine_name}")
    print(f"[OK] Font: {font}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
