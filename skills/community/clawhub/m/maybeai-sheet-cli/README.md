# maybeai-sheet-cli-skill

Agent skill for the `mbs` CLI from `maybeai-sheet-cli` **0.28.0**.

The installed CLI's runtime help is the command contract. Start a spreadsheet
session with:

```bash
mbs --help
mbs <group> --help
mbs <group> <command> --help
```

The parent `--help` output identifies commands that agents may generate in new
workflows. A directly callable command missing from that output is a hidden
compatibility command: do not recommend or generate it. If public commands
cannot preserve the requested behavior, explain the capability gap instead of
constructing a destructive approximation.

This skill provides model-routing guidance for Sheet, SheetTable, Base, and SQL
workflows; safe mutation and verification practices; and topic references for
imports, reads/writes, formulas, charts, sharing, recovery, and lineage. It
intentionally does **not** duplicate a complete CLI command tree. Consult the
installed command help for available groups, operations, parameters, and
feature changes.

Notable public-workflow boundaries:

- Use `workbook inspect` and `worksheet list` for target discovery.
- Use `formula set` for formula writes and `range note` for Sheet notes.
- Use `mbs image` for image operations.
- Use public `mbs table clear --target "$BASE_TABLE" --yes --verify` to remove
  all Base table records while preserving fields/schema. It is destructive, so
  preview with `--dry-run` when needed. For batch updates to existing Base
  field schema, use public `mbs column batch-update` after
  confirming its installed `--help` contract.

This repository owns agent-facing assets:

- `SKILL.md` — routing, playbooks, and core rules
- `references/` — runtime-help-first operational guidance and semantic caveats
- `agents/` — agent metadata
- `artifacts/` — demo datasets and reusable example specs

CLI implementation lives separately at:

- `../maybeai-sheet-cli`

Install the CLI:

```bash
pip install maybeai-sheet-cli
```

To get a MaybeAI API token, register at [maybe.ai](https://www.maybe.ai/), then
open [My Plan](https://www.maybe.ai/user/my-plan) and copy a token from the
**API Token** section.

Set `MAYBEAI_API_TOKEN`, then run `mbs --help`:

```bash
export MAYBEAI_API_TOKEN="your-api-token"
mbs --help
```

## Sync after CLI release

After `../maybeai-sheet-cli` is published to PyPI, sync this skill's version
frontmatter from the released CLI metadata:

```bash
python scripts/sync_cli_release.py --cli-repo ../maybeai-sheet-cli
```

The hook verifies that the CLI repository version fields agree and that the
same version exists on PyPI before updating `SKILL.md`. Use `--skip-pypi-check`
only for local draft docs before a package release.
