#!/usr/bin/env python3
"""Inspect files and folders for localization planning."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

SKIP_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "venv",
}


CATEGORY_BY_EXTENSION = {
    ".arb": "locale",
    ".c": "code",
    ".cc": "code",
    ".cpp": "code",
    ".cs": "code",
    ".css": "web",
    ".doc": "office",
    ".docx": "office",
    ".go": "code",
    ".h": "code",
    ".hpp": "code",
    ".htm": "web",
    ".html": "web",
    ".ini": "config",
    ".java": "code",
    ".js": "code",
    ".json": "config",
    ".jsx": "web",
    ".kt": "code",
    ".less": "web",
    ".md": "docs",
    ".mdx": "docs",
    ".odt": "office",
    ".pdf": "pdf",
    ".php": "code",
    ".po": "locale",
    ".pot": "locale",
    ".ppt": "office",
    ".pptx": "office",
    ".properties": "config",
    ".py": "code",
    ".rb": "code",
    ".resx": "locale",
    ".rst": "docs",
    ".sass": "web",
    ".scss": "web",
    ".srt": "subtitle",
    ".strings": "locale",
    ".svg": "vector",
    ".tex": "docs",
    ".toml": "config",
    ".ts": "code",
    ".tsx": "web",
    ".txt": "docs",
    ".vue": "web",
    ".xhtml": "web",
    ".xls": "office",
    ".xlsx": "office",
    ".xml": "config",
    ".yaml": "config",
    ".yml": "config",
}

CODE_EXTENSIONS = {
    ".c",
    ".cc",
    ".cpp",
    ".cs",
    ".go",
    ".h",
    ".hpp",
    ".java",
    ".js",
    ".jsx",
    ".kt",
    ".php",
    ".py",
    ".rb",
    ".ts",
    ".tsx",
    ".vue",
}

WEB_EXTENSIONS = {
    ".css",
    ".htm",
    ".html",
    ".less",
    ".sass",
    ".scss",
    ".svg",
    ".xhtml",
}

OFFICE_EXTENSIONS = {
    ".doc",
    ".docx",
    ".odt",
    ".ppt",
    ".pptx",
    ".xls",
    ".xlsx",
}

IMAGE_EXTENSIONS = {
    ".bmp",
    ".gif",
    ".heic",
    ".jpeg",
    ".jpg",
    ".png",
    ".tif",
    ".tiff",
    ".webp",
}

FONT_EXTENSIONS = {
    ".otf",
    ".ttf",
    ".woff",
    ".woff2",
}

ARCHIVE_EXTENSIONS = {
    ".7z",
    ".bz2",
    ".gz",
    ".rar",
    ".tar",
    ".zip",
}


def iter_files(path: Path) -> Iterable[Path]:
    if path.is_file():
        yield path
        return
    for child in path.rglob("*"):
        if any(part in SKIP_DIR_NAMES for part in child.parts):
            continue
        if child.is_file():
            yield child


def classify_extension(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in CATEGORY_BY_EXTENSION:
        return CATEGORY_BY_EXTENSION[ext]
    if ext in IMAGE_EXTENSIONS:
        return "image"
    if ext in FONT_EXTENSIONS:
        return "font"
    if ext in ARCHIVE_EXTENSIONS:
        return "archive"
    if ext:
        return "other"
    return "extensionless"


def recommend_pipeline(categories: set[str], extensions: Counter[str]) -> str:
    if "pdf" in categories:
        if len(categories) > 1:
            return "mixed-folder"
        return "pdf"
    if "office" in categories:
        if "code" in categories or "web" in categories:
            return "mixed-folder"
        return "office"
    if "code" in categories or "web" in categories:
        return "code-web"
    if "locale" in categories:
        return "code-web"
    if "subtitle" in categories:
        return "subtitle"
    if "image" in categories and len(categories) == 1:
        return "raster-text"
    if ".md" in extensions or ".mdx" in extensions or ".rst" in extensions:
        return "docs"
    return "manual-review"


def collect_risks(categories: set[str], extensions: Counter[str]) -> list[str]:
    risks: list[str] = []
    if "pdf" in categories:
        risks.append("PDFs are hard to round-trip losslessly; prefer editable sources when available.")
    if "office" in categories:
        risks.append("Office files may overflow text boxes or use fonts that lack target-language glyphs.")
    if "code" in categories or "web" in categories:
        risks.append("Code and web artifacts require strict protection of identifiers, placeholders, and markup.")
    if "image" in categories:
        risks.append("Images may contain rasterized text that requires OCR or manual reconstruction.")
    if "font" not in categories and ("pdf" in categories or "office" in categories or "web" in categories):
        risks.append("No local font files were detected; verify glyph coverage in the target language.")
    if any(ext in ARCHIVE_EXTENSIONS for ext in extensions):
        risks.append("Archive outputs may be derived artifacts; translate the source content instead of the export when possible.")
    if ".svg" in extensions:
        risks.append("SVG files can mix translatable text with vector instructions; edit text nodes only.")
    if ".json" in extensions or ".yaml" in extensions or ".yml" in extensions:
        risks.append("Config files may contain locale strings alongside machine-readable keys; separate them carefully.")
    if "locale" in categories:
        risks.append("Localization resources still require placeholder parity, plural-rule safety, and glossary consistency.")
    if not risks:
        risks.append("No major format-specific risks detected; still define the safe translation surface before editing.")
    return risks


def summarize_path(path: Path) -> dict:
    files = list(iter_files(path))
    categories = Counter()
    extensions = Counter()
    examples: dict[str, list[str]] = defaultdict(list)

    for file_path in files:
        ext = file_path.suffix.lower() or "<none>"
        category = classify_extension(file_path)
        categories[category] += 1
        extensions[ext] += 1
        if len(examples[category]) < 5:
            examples[category].append(str(file_path))

    category_set = set(categories)
    pipeline = recommend_pipeline(category_set, extensions)
    risks = collect_risks(category_set, extensions)

    return {
        "path": str(path),
        "file_count": len(files),
        "categories": categories.most_common(),
        "top_extensions": extensions.most_common(12),
        "recommended_pipeline": pipeline,
        "risks": risks,
        "examples": {key: value for key, value in sorted(examples.items())},
    }


def render_text(summary: dict) -> str:
    lines = [
        f"Path: {summary['path']}",
        f"Files: {summary['file_count']}",
        f"Recommended pipeline: {summary['recommended_pipeline']}",
        "Categories:",
    ]
    for category, count in summary["categories"]:
        lines.append(f"  - {category}: {count}")
    lines.append("Top extensions:")
    for extension, count in summary["top_extensions"]:
        lines.append(f"  - {extension}: {count}")
    lines.append("Risks:")
    for risk in summary["risks"]:
        lines.append(f"  - {risk}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect files and folders to plan a high-fidelity localization workflow."
    )
    parser.add_argument("paths", nargs="+", help="Files or folders to inspect.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summaries = []
    for raw_path in args.paths:
        path = Path(raw_path).expanduser().resolve()
        if not path.exists():
            raise SystemExit(f"Path does not exist: {path}")
        summaries.append(summarize_path(path))

    if args.json:
        print(json.dumps(summaries, indent=2))
    else:
        for index, summary in enumerate(summaries):
            if index:
                print()
            print(render_text(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
