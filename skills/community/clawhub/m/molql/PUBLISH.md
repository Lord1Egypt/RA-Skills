# Publishing MolQL to ClawHub

This document describes how to publish the `molql` AI skill to [ClawHub](https://clawhub.ai), the OpenClaw package registry.

## Overview

MolQL is an **AI skill** (not a code plugin). Publishing follows the [ClawHub Skill Publishing](https://docs.openclaw.ai/clawhub/publishing) flow — the skill folder (`SKILL.md` + references) is uploaded under an owner on ClawHub.

## Prerequisites

| Requirement | How to get it |
|---|---|
| ClawHub CLI | `npm install -g @openclaw/clawhub` |
| ClawHub account | Sign up at https://clawhub.ai |
| Auth token | `clawhub login` (interactive) or set `CLAWHUB_TOKEN` env var |
| Publisher access | Must have publish rights for the target `--owner` |

## Manual Publish (CLI)

### As the authenticated user

```bash
clawhub skill publish ./packages/skills/molql \
  --slug molql \
  --name "MolQL"
```

### To an org owner

```bash
clawhub skill publish ./packages/skills/molql \
  --slug molql \
  --name "MolQL" \
  --owner openclaw
```

### Use the helper script

```bash
chmod +x packages/skills/molql/scripts/publish.sh
./packages/skills/molql/scripts/publish.sh --owner openclaw
```

Preview with `--dry-run`:

```bash
./packages/skills/molql/scripts/publish.sh --dry-run
```

## Automated Publish (GitHub Actions)

A reusable workflow from `openclaw/clawhub` handles CI publishing. See [`.github/workflows/skill-publish.yml`](../../.github/workflows/skill-publish.yml).

### Setting up

1. **Add `CLAWHUB_TOKEN`** to the repository secrets (Settings → Secrets and variables → Actions → New repository secret).
2. **Trigger manually** via `workflow_dispatch` on the Actions tab to publish a specific skill.
3. **On pushes to `main`** that change files under `packages/skills/`, the workflow auto-publishes all changed skills.

### Workflow parameters

| Parameter | Description |
|---|---|
| `owner` | Target ClawHub owner (default: `openclaw`) |
| `root` | Where to find skill folders (default: `packages/skills`) |
| `skill_path` | Publish only one skill folder (omit to publish all) |
| `dry_run` | Preview changes without publishing |

## Versioning

- ClawHub auto-increments the **patch** version on each publish.
- To pin a specific version, pass `--version <semver>` to `clawhub skill publish`.
- New skills start at `1.0.0`.

## Review Status

After publishing, the release enters automated security checks. It stays out of public install/download surfaces until review finishes.

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `Package scope "@X" must match selected owner "@Y"` | Owner mismatch | Use `--owner` matching the package scope |
| `Not authenticated` | Missing ClawHub session | Run `clawhub login` |
| `You do not have access` | Insufficient permissions | Request org access or transfer ownership |
