#!/usr/bin/env python3
"""CLI entrypoint for report aggregation and Word annotation stage."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from orchestrators.style_stage_orchestrator import run_annotation_stage


def main() -> None:
    parser = argparse.ArgumentParser(description="Run annotation export stage")
    parser.add_argument("--config", required=True, help="Path to config JSON")
    parser.add_argument("--output-dir", help="Optional override for output directory")
    args = parser.parse_args()

    config_path = Path(args.config).expanduser().resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["configPath"] = str(config_path)
    if args.output_dir:
        config["outputDir"] = str(Path(args.output_dir).expanduser().resolve())
    summary = run_annotation_stage(config)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
