---
name: mnemospark-openclaw-governance
description: Operate OpenClaw multi-agent governance with openclaw-gov — read-only audit, material change documentation, staged discovery, validate registry/runbooks, and ship governance PRs. Use when changing crons, workflows, runbooks, registry.yaml, RACI, governance.config.yaml, refreshing inventory, running governance check, or completing material system config changes.
version: 1.1.0
metadata:
  openclaw:
    skillKey: mnemospark-openclaw-governance
    requires:
      bins:
        - openclaw-gov
        - openclaw
        - git
      anyBins:
        - gh
        - jq
    envVars:
      - name: OPENCLAW_GOVERNANCE_ROOT
        required: false
        description: Override path to governance root when not using default ~/.openclaw/governance or nearest governance.config.yaml.
    install:
      - kind: uv
        package: "openclaw-governance @ git+https://github.com/pawlsclick/openclaw-governance@v0.5.5"
        bins: [openclaw-gov]
    emoji: "📋"
    homepage: https://github.com/pawlsclick/openclaw-governance
---

# OpenClaw Governance (openclaw-gov)

Teaches agents to maintain the **governance root**: `registry.yaml`, runbooks, CHANGELOG, and CI drift checks. Pick **one workflow** below; do not run the full ship path for a read-only audit.

## Step 0 — Resolve governance root

**Precedence:** `--root PATH` > `OPENCLAW_GOVERNANCE_ROOT` > nearest `governance.config.yaml` walking up from cwd > `~/.openclaw/governance`.

**Workspace override:** If the agent workspace `AGENTS.md` governance stanza (`<!-- openclaw-governance:begin -->`) declares a **Governance root** path, use that path as `$GOV_ROOT` when it differs from the default. The stanza wins over skill defaults for this install.

```bash
export GOV_ROOT="${OPENCLAW_GOVERNANCE_ROOT:-$HOME/.openclaw/governance}"
# If AGENTS.md stanza specifies a path, set GOV_ROOT to that path instead.
```

### Version preflight (required)

This skill assumes **openclaw-gov v0.5.5+** (`--inventory`, `--staged`, inventory schema v2). Before using those flags:

```bash
openclaw-gov --version   # expect 0.5.5 or newer
```

If older, upgrade per [Install CLI](#install-cli-operators) before `--inventory`, `--staged`, `--promote`, or schema-v2 assumptions.

### Shared preflight (before any edit or ship)

Agents share the governance repo with humans. **Never overwrite unrelated user work.**

```bash
cd "$GOV_ROOT"
git status --short --branch
```

- **Dirty worktree with changes outside your task:** stop. Do not `ship start`, `--write`, `--promote`, or `regen --write`. Tell the human what is dirty; offer to scope edits to governance paths only after confirmation.
- **Unexpected changes under `workflows/` you did not make:** read the diff before proceeding.

Then confirm config:

```bash
openclaw-gov doctor --validate-config --root "$GOV_ROOT"
```

## Pick a workflow

| Goal | Section |
|------|---------|
| Audit only, no file writes | [Workflow A — Read-only audit](#workflow-a--read-only-audit) |
| Material change, document + verify locally | [Workflow B — Material change](#workflow-b--material-change) |
| Open governance PR | [Workflow C — Ship PR](#workflow-c--ship-pr) |

**Material threshold:** [references/material-change-threshold.md](references/material-change-threshold.md)

Governing runbook for material work: `workflows/runbooks/main.system_config_change_governance.md` under `$GOV_ROOT`.

## Workflow A — Read-only audit

No `ship start`. No `--write`, `--promote`, or `regen --write`.

```bash
openclaw-gov doctor --validate-config --root "$GOV_ROOT"
openclaw-gov discover --root "$GOV_ROOT"
openclaw-gov check --root "$GOV_ROOT"
openclaw-gov regen --check --root "$GOV_ROOT"
```

Optional JSON (targeted slices only): [references/discovery-json-slices.md](references/discovery-json-slices.md)

Pipe **only stdout** for `--json`; human report is on stderr.

## Workflow B — Material change

For system updates, cron/workflow/runbook/registry changes, and other [material](#what-counts-as-material) work. Branch before any mutating command.

```bash
cd "$GOV_ROOT" && git status --short --branch   # preflight again
openclaw-gov doctor --validate-config --root "$GOV_ROOT"

openclaw-gov ship start --branch "governance/$(date +%Y-%m-%d)-short-topic" --root "$GOV_ROOT"
# ... edit runbooks, registry, CHANGELOG; discover --inventory / --staged / --promote as needed ...

openclaw-gov check --root "$GOV_ROOT"
openclaw-gov regen --check --root "$GOV_ROOT"
# If regen --check fails ONLY because README/RACI markers drifted:
openclaw-gov regen --write --root "$GOV_ROOT"
```

**Regen rule:** default to `regen --check`. Run `regen --write` only when `regen --check` fails or you intentionally changed content that regen generates. Do not run `regen --write` habitually on every doc edit.

Completion checklist (before calling done):

- [ ] Live change applied and verified (see [Verification](#verification-local-vs-external))
- [ ] Runbook updated under `workflows/runbooks/`
- [ ] `workflows/registry.yaml` updated if workflow is new or materially changed
- [ ] `workflows/CHANGELOG.md` entry appended
- [ ] `check` and `regen --check` pass

If the change is material, continue to [Workflow C](#workflow-c--ship-pr) unless site policy says otherwise.

## Workflow C — Ship PR

Run [Preflight before ship](#preflight-before-ship) first. Use **one** commit path below — not both.

### Preflight before ship

```bash
cd "$GOV_ROOT"
git status --short --branch          # clean or only your intended files
git remote -v                        # origin configured
openclaw-gov doctor --validate-config --root "$GOV_ROOT"
gh auth status 2>/dev/null || true   # only if you will push
openclaw-gov check --root "$GOV_ROOT"
openclaw-gov regen --check --root "$GOV_ROOT"
```

If worktree is dirty with unrelated changes, **stop** (see Step 0).

### Branch and validate

```bash
openclaw-gov ship start \
  --branch "governance/$(date +%Y-%m-%d)-short-topic" \
  --root "$GOV_ROOT"
# ... edits already done on this branch, or make them now ...

openclaw-gov check --root "$GOV_ROOT"
openclaw-gov regen --check --root "$GOV_ROOT"
# If regen --check failed: openclaw-gov regen --write --root "$GOV_ROOT" then re-check
```

Use an explicit `--branch` name (date + topic) for audit trails; avoid anonymous default branch names during incidents.

### Commit — choose ONE path

**Path 1 — Local commit only** (human pushes later):

```bash
openclaw-gov ship commit \
  -m "docs(governance): describe the change" \
  --no-push \
  --root "$GOV_ROOT"
```

**Path 2 — Commit + push + PR** (non-interactive agents):

```bash
openclaw-gov ship commit \
  -m "docs(governance): describe the change" \
  --push \
  --root "$GOV_ROOT"
```

Do **not** run `ship commit` and then `ship commit --push` as two steps.

### Publish policy override

Default: `ship commit --push` uses `git push` + `gh pr create` when `gh auth login` is satisfied.

**Site override:** If the governing runbook, workspace `TOOLS.md`, or operator policy defines a stricter path (GitHub MCP only, human must open PR, no direct push), follow **that** policy instead of the default CLI push. When override applies, use Path 1 (`--no-push`) and hand off per local docs.

### Conventional Commits (required)

Format: `type(governance): imperative summary` — never vague messages (`update`, `WIP`).

| Type | Use when |
|------|----------|
| `docs` | Runbooks, README, CHANGELOG |
| `chore` | Registry sync, inventory refresh |
| `feat` | Workflow promoted to `active` / `required` |
| `fix` | Registry/runbook drift correction |

Prefer `ship commit -m "..."` over inferred generic messages.

### Post-merge cleanup

After the governance PR merges:

```bash
cd "$GOV_ROOT"
git fetch --prune origin
git switch main
git pull --ff-only origin main
git branch -d governance/YYYY-MM-DD-short-topic   # or -D if squash-merged
openclaw-gov check --root "$GOV_ROOT"
openclaw-gov regen --check --root "$GOV_ROOT"
```

## What counts as material

Governance PRs are required for system updates, workflow/cron/runbook changes, and major operational changes you would need to restore from git. Full examples: [references/material-change-threshold.md](references/material-change-threshold.md).

Cross-repo: material script-path or cron-payload changes in other repos need a **paired governance PR** in the same change window.

## Verification — local vs external

**Local (default, no ask):** `doctor`, `discover`, `check`, `regen --check`, read-only `git diff`, parsing inventory JSON.

**External / side effects (ask first):** smoke tests that send telemetry, hit production APIs, restart gateways, run live crons, post to chat, or mutate off-host state. Separate these from governance doc validation. Get explicit approval before running; document what ran in the runbook/CHANGELOG.

## NEVER (critical)

1. **Do not** run `discover --write`, `discover --promote`, or `regen --write` on branch `main`.
2. **Do not** edit governance files when `git status` shows unrelated human changes you did not confirm.
3. **Do not** pipe full `discover --json` into context — use [references/discovery-json-slices.md](references/discovery-json-slices.md).
4. **Do not** use `discover --write` on brownfield when `discover --staged` + `--promote` is available.
5. **Do not** call material work "done" without runbook + registry (when needed) + CHANGELOG + passing `check`.

## Discover — pick the right flag

| Intent | Command |
|--------|---------|
| Console summary only | `discover` |
| Refresh committed inventory JSON | `discover --inventory` |
| Inventory + candidates (no registry write) | `discover --staged` |
| Apply staged merge | `discover --promote` |
| Controlled promotion | `discover --promote --allowlist path.json` |
| Legacy immediate write | `discover --write` (greenfield; branch first) |

Brownfield: [references/brownfield-flow.md](references/brownfield-flow.md). Commands: [references/commands.md](references/commands.md).

## Bootstrap and migration

```bash
openclaw-gov init --root "$GOV_ROOT"
openclaw-gov adopt --from /path/to/existing-governance --root "$GOV_ROOT"
openclaw-gov inject-agents --write
openclaw-gov inject-agents --write --prune
```

Migrating guide: [docs/migrating-existing-governance.md](https://github.com/pawlsclick/openclaw-governance/blob/main/docs/migrating-existing-governance.md)

## Error rescue

| Symptom | Fix |
|---------|-----|
| No governance root | `openclaw-gov init --root "$GOV_ROOT"` |
| Dirty worktree | Do not ship; coordinate with human |
| Old CLI | `openclaw-gov --version`; upgrade to v0.5.5+ |
| `regen --check` fails | On feature branch: `regen --write`, re-check |
| promote touched curated rows | Restore from git; `--staged` + `--allowlist` |

## CI gate (governance repos)

```bash
openclaw-gov regen --check && openclaw-gov check
openclaw-gov discover --staged --root "$GOV_ROOT"
git diff --exit-code workflows/registry.yaml
```

## Install CLI (operators)

**Note:** Frontmatter `metadata.openclaw.install` (kind `uv`) is for **ClawHub/agent auto-install**. Humans on Ubuntu should prefer **pipx**; macOS/containers use **pip** — same git pin `@v0.5.5`, not competing products.

Ubuntu (pipx recommended):

```bash
pipx install "openclaw-governance @ git+https://github.com/pawlsclick/openclaw-governance@v0.5.5"
```

Mac / venv:

```bash
pip install "openclaw-governance @ git+https://github.com/pawlsclick/openclaw-governance@v0.5.5"
```
