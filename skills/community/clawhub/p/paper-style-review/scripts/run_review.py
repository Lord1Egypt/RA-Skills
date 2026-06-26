#!/usr/bin/env python3
"""paper-style-review 统一 CLI 入口。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from orchestrators.review_orchestrator import run_review
from orchestrators.style_stage_orchestrator import (
    run_annotation_stage,
    run_style_annotation_stage,
    run_style_profile_stage,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run paper-style-review mainline pipeline")
    parser.add_argument("--config", required=True, help="Path to config JSON")
    parser.add_argument(
        "--stage",
        default="all",
        choices=["all", "style_profile", "style_annotation", "annotation"],
        help="Run the full pipeline or one standalone stage",
    )
    parser.add_argument("--chapters", help="Optional chapter scope, e.g. abstract,1,2")
    parser.add_argument("--output-dir", help="Optional override for output directory")
    args = parser.parse_args()

    config_path = Path(args.config).expanduser().resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["configPath"] = str(config_path)
    if args.chapters:
        config["chapterScope"] = args.chapters
    if args.output_dir:
        config["outputDir"] = str(Path(args.output_dir).expanduser().resolve())
    if args.stage == "style_profile":
        summary = run_style_profile_stage(config)
    elif args.stage == "style_annotation":
        summary = run_style_annotation_stage(config)
    elif args.stage == "annotation":
        summary = run_annotation_stage(config)
    else:
        summary = run_review(config)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
