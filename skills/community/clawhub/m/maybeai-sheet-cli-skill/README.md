# maybeai-sheet-cli-skill

Agent skill for the `mbs` CLI from `maybeai-sheet-cli`.

It covers workbook/worksheet/table operations, safe full worksheet data
refreshes that retain headers and formulas, worksheet styling, PG/SheetTable
field style metadata, floating chart-like image objects, and worksheet-scoped
dashboard orchestration.

This repository owns agent-facing assets:

- `SKILL.md` — routing, playbooks, core rules
- `references/` — topic docs and `cli-commands.md` command catalog
- `agents/` — agent metadata
- `artifacts/` — demo datasets and reusable example specs

CLI implementation lives separately:

- `../maybeai-sheet-cli`

Install the CLI: `pip install maybeai-sheet-cli`

Set `MAYBEAI_API_TOKEN`, then run `mbs --help`.

## Sync after CLI release

After `../maybeai-sheet-cli` is published to PyPI, sync this skill's version
frontmatter from the released CLI metadata:

```bash
python scripts/sync_cli_release.py --cli-repo ../maybeai-sheet-cli
```

The hook verifies that the CLI repo version fields agree and that the same
version exists on PyPI before updating `SKILL.md`. Use `--skip-pypi-check` only
for local draft docs before a package release.
