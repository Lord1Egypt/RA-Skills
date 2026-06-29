from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--code_pack", required=True)
    parser.add_argument("--save_to", required=True)
    args = parser.parse_args()
    source = Path(args.code_pack)
    content = f"""# {source.stem}

## Goal
This code pack was submitted for Research KB codebase analysis.

## Directory structure
The deterministic fallback script does not expand archives. The OpenClaw Agent should inspect the pack and replace this page with a richer analysis.

## Sources and Traceability
- source_file: {source.name}
"""
    Path(args.save_to).write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
