"""Render the Kinema TDD instructions for Claude Code or Codex.

Usage:
    python render.py --target claude --params params.json --out CLAUDE.md.draft.md
    python render.py --target codex --params params.json --out AGENTS.md.draft.md

Requires: jinja2 (install with `uv pip install jinja2` or `pip install jinja2`).
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined


TARGET_CONTEXT = {
    "claude": {
        "instruction_file": "CLAUDE.md",
        "coding_agent": "Claude Code",
        "ai_coauthor_name": "Claude Opus 4.7",
        "ai_coauthor_email": "noreply@anthropic.com",
    },
    "codex": {
        "instruction_file": "AGENTS.md",
        "coding_agent": "Codex",
        "ai_coauthor_name": "Codex",
        "ai_coauthor_email": "codex@openai.com",
    },
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target",
        choices=sorted(TARGET_CONTEXT),
        default="claude",
        help="Instruction target (default: claude)",
    )
    parser.add_argument("--params", required=True, help="Path to params JSON")
    parser.add_argument("--out", required=True, help="Path to write rendered markdown")
    parser.add_argument(
        "--template-dir",
        default=str(Path(__file__).resolve().parent.parent / "assets"),
        help="Directory containing claude_md.j2 (default: ../assets relative to this script)",
    )
    args = parser.parse_args()

    params = json.loads(Path(args.params).read_text(encoding="utf-8-sig"))
    params.setdefault("iso_date", date.today().isoformat())
    params.update(TARGET_CONTEXT[args.target])

    env = Environment(
        loader=FileSystemLoader(args.template_dir),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        undefined=StrictUndefined,
    )
    template = env.get_template("claude_md.j2")
    rendered = template.render(**params)
    Path(args.out).write_text(rendered, encoding="utf-8")
    print(f"Rendered to {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
