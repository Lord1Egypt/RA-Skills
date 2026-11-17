#!/usr/bin/env python3
"""Generate an interactive HTML knowledge graph from a personal-wiki dir.

Vendored from Google Open Knowledge Format (OKF) viewer, Apache-2.0
(github.com/GoogleCloudPlatform/knowledge-catalog). Patched to support
Obsidian-style [[wikilinks]] used by ~/wiki/ (the upstream viewer only
parses standard [text](path.md) links).

Standalone: depends only on PyYAML — deliberately avoids the OKF repo's
google-adk / google-cloud-bigquery deps (only needed by its enrich agent).

Usage:
    python3 visualize.py [WIKI_PAGES_DIR] [OUT_HTML] [BUNDLE_NAME]

Defaults:
    WIKI_PAGES_DIR = ~/wiki/pages
    OUT_HTML       = ~/wiki/wiki-graph.html
    BUNDLE_NAME    = "My Wiki"
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from generator import generate_visualization  # noqa: E402


def main(argv: list[str]) -> int:
    home = Path.home()
    pages = Path(argv[1]).expanduser() if len(argv) > 1 else home / "wiki" / "pages"
    out = Path(argv[2]).expanduser() if len(argv) > 2 else home / "wiki" / "wiki-graph.html"
    name = argv[3] if len(argv) > 3 else "My Wiki"

    if not pages.is_dir():
        print(f"[error] wiki pages dir not found: {pages}", file=sys.stderr)
        return 1

    stats = generate_visualization(pages, out, bundle_name=name)
    print(
        f"[ok] {stats['concepts']} concepts / {stats['edges']} edges / "
        f"{stats['bytes'] // 1024} KB -> {out}"
    )
    if stats["edges"] == 0 and stats["concepts"] > 1:
        print(
            "[warn] 0 edges but >1 concept — check that pages use [[wikilinks]] "
            "or [text](path.md) links.",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
