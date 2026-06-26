#!/usr/bin/env python3
"""Scaffold an n8n-evol-I workspace.

Default location is ``${PWD}/n8n-evol-I-workspace``. If you run from inside an
existing workspace directory (basename ``n8n-evol-I-workspace``), the existing
workspace is used in place. Pass ``--workspace <path>`` to override.
"""
import argparse
import shutil
import sys
from pathlib import Path

# Make `from helpers.X import ...` work when script is invoked directly.
sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.workspace import workspace_root

_AGENTS_MD = """\
# AGENTS.md — n8n-evol-I workspace orientation

You are a coding agent working in an n8n-evol-I workspace. This file tells you
where things are and how to operate. Read it at the start of every session.

## Skill router

All n8n actions route through `<harness>/SKILL.md`. When the user asks anything
n8n-related, read that file first to find the right sub-skill and helper.

## Workspace layout

```
n8n-evol-I-workspace/
├── n8n-config/             # env YAML (dev.yml, prod.yml, …) + .env.<env> secrets
├── n8n-workflows-template/ # *.template.json — canonical, version-controlled
├── n8n-build/              # hydrated outputs — gitignored, regenerated on deploy
├── n8n-functions/
│   ├── js/                 # pure JS functions injected via {{@js:...}}
│   └── py/                 # pure Python functions injected via {{@py:...}}
├── n8n-functions-tests/    # *.test.js / test_*.py — paired tests, required by validator
├── n8n-prompts/
│   ├── prompts/            # *_prompt.txt + *_schema.json
│   ├── datasets/           # *.json for iterate-prompt
│   └── evals/
├── n8n-assets/
│   ├── email-templates/    # *.html injected via {{@html:...}}
│   ├── images/
│   └── misc/
├── cloud-functions/        # FastAPI service scaffolded by add-cloud-function
│   └── functions/
├── cloud-functions-tests/
├── AGENTS.md               # ← this file
└── N8N-WORKSPACE-MEMORY.md # rolling journal — read and update this every session
```

## Session memory

**Read `N8N-WORKSPACE-MEMORY.md` at the start of every session.**
It contains project-specific knowledge accumulated over time: workflows that exist,
env configurations, investigation findings, workspace deviations from the default
tree, credential quirks, recurring failure patterns, and anything else worth
remembering. It saves you context that would otherwise require re-reading multiple
config files and asking the user to re-explain their setup.

**Update `N8N-WORKSPACE-MEMORY.md` whenever you learn something durable.** This is
your responsibility, not the user's. Append a short dated entry any time you:
- Create or significantly understand a workflow (what it does, key inputs/outputs).
- Add or configure a new environment.
- Discover a workspace deviation from the default layout above.
- Complete an investigation and reach a finding worth reusing (root cause, fix applied).
- Encounter a credential or integration quirk specific to this project.
- Learn anything that would save context in the next session.

You do not need to keep entries perfectly formatted. Short, direct notes are better
than no notes. Append; don't rewrite history.

## Notes (static, managed by user)
(project-specific context the user has chosen to pin here)
"""

_WORKSPACE_MEMORY_MD = """\
# N8N-WORKSPACE-MEMORY

Rolling journal for this n8n-evol-I workspace. The agent reads this at the start
of every session and appends entries as it learns new things.

## Workflows
(none yet — add entries as workflows are created and understood)

## Environments
(none yet — add env names, instance URLs, and any quirks after bootstrap-env)

## Investigations
(none yet — add dated findings from inspect-execution sessions)

## Workspace notes
(deviations from default layout, custom credential setups, etc.)
"""

_ALIAS_TEMPLATE = """\
@n8n-evol-I-workspace/AGENTS.md

(If your agent runtime does not support @file imports, read the file at the
path above directly. It contains workspace orientation and points to the rolling
session-memory journal.)
"""

_GITIGNORE = """\
n8n-build/
.env.*
"""


def _write_if_absent(path: Path, content: str, skip_msg: str) -> None:
    if path.exists():
        print(f"  {skip_msg}")
    else:
        path.write_text(content)
        print(f"  Wrote {path}")


def _scaffold(ws: Path, force: bool) -> None:
    if ws.exists():
        if not force:
            print(f"Workspace already exists at {ws}. Use --force to recreate (DESTRUCTIVE).", file=sys.stderr)
            sys.exit(1)
        shutil.rmtree(ws)

    dirs = [
        ws / "n8n-config",
        ws / "n8n-workflows-template",
        ws / "n8n-build",
        ws / "n8n-prompts" / "prompts",
        ws / "n8n-prompts" / "datasets",
        ws / "n8n-prompts" / "evals",
        ws / "n8n-functions" / "js",
        ws / "n8n-functions" / "py",
        ws / "n8n-functions-tests",
        ws / "n8n-assets" / "email-templates",
        ws / "n8n-assets" / "images",
        ws / "n8n-assets" / "misc",
        ws / "cloud-functions" / "functions",
        ws / "cloud-functions-tests",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    (ws / "AGENTS.md").write_text(_AGENTS_MD)
    (ws / "N8N-WORKSPACE-MEMORY.md").write_text(_WORKSPACE_MEMORY_MD)
    (ws / ".gitignore").write_text(_GITIGNORE)
    (ws / "n8n-config" / ".env.example").write_text(
        "# Document secret env-var names here (no values).\n"
        "# Copy relevant entries into .env.<env> with real values.\n"
    )
    (ws / "n8n-functions-tests" / "conftest.py").write_text(
        "import sys\n"
        "from pathlib import Path\n"
        'sys.path.insert(0, str(Path(__file__).parent.parent / "n8n-functions" / "py"))\n'
    )
    (ws / "cloud-functions-tests" / "conftest.py").write_text(
        "import sys\n"
        "from pathlib import Path\n"
        'sys.path.insert(0, str(Path(__file__).parent.parent / "cloud-functions"))\n'
    )

    # Write alias files at project root if this is the default workspace location.
    if ws.name == "n8n-evol-I-workspace" and ws.parent == Path.cwd():
        project_root = ws.parent
        _write_if_absent(
            project_root / "CLAUDE.md",
            _ALIAS_TEMPLATE,
            "CLAUDE.md already exists at project root — skipping",
        )
        copilot_dir = project_root / ".github"
        copilot_dir.mkdir(exist_ok=True)
        _write_if_absent(
            copilot_dir / "copilot-instructions.md",
            _ALIAS_TEMPLATE,
            ".github/copilot-instructions.md already exists — skipping",
        )
    else:
        print(
            "  Note: alias files (CLAUDE.md, .github/copilot-instructions.md) "
            "not written — non-default workspace path. Write them manually at "
            "your project root pointing to the workspace's AGENTS.md."
        )

    print(f"Workspace created at {ws}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None, help="Workspace path. Default: ${PWD}/n8n-evol-I-workspace, or ${PWD} if its basename is already n8n-evol-I-workspace.")
    parser.add_argument("--force", action="store_true", help="Recreate workspace if it already exists (DESTRUCTIVE)")
    args = parser.parse_args()
    _scaffold(workspace_root(args.workspace), args.force)


if __name__ == "__main__":
    main()
