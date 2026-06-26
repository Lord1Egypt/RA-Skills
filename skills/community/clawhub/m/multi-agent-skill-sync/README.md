# Skill Sync

One source of truth for local AI agent skills.

`skill-sync` turns a messy multi-agent setup into a maintainable local skill system:

- scan skills across Codex, Claude, OpenClaw, OpenCode, workspace `./skills`, and shared agent roots
- score the hygiene of your current setup
- show shared, duplicate, compatible, and host-specific skills
- pick a canonical source automatically
- replace duplicate copies with symlinks
- back up every replaced install so you can restore it later
- export a portable layout manifest and recreate that topology on another machine

## Who This Is For

`skill-sync` is built for people who:

- use more than one AI coding agent
- install lots of local skills
- keep a shared skill library in `~/.agents/skills`
- move between machines or rebuild environments often
- want one canonical skill source instead of version drift everywhere

## The Problem

In a real machine, the same skill often appears in multiple places:

- `~/.codex/skills`
- `~/.claude/skills`
- `~/.openclaw/skills`
- `~/.config/opencode/skills`
- `~/.agents/skills`
- `<workspace>/skills`

That creates drift:

- one copy gets updated, another stays stale
- the same skill gets installed repeatedly
- nobody remembers which copy is the real source of truth

## The Product Promise

`skill-sync` gives you four things that basic skill managers usually do not:

1. Cross-host discovery  
It scans all the common local roots at once instead of showing one host in isolation.

2. Canonical source selection  
It decides which copy should win based on strategy, timestamps, shared roots, and your preferred source order.

3. Safe convergence  
It can turn duplicates into symlinks and centralize ownership without destructive blind replacement.

4. Reversible operations  
Every dedupe run writes a restorable backup manifest under `~/.skill-sync/backups`.

## What Makes It Different

Compared with generic local skill managers, `skill-sync` is specifically about:

- cross-agent skill hygiene
- canonical source adoption
- symlink-based dedupe
- compatible skill diffing
- reversible local convergence

## Supported Skill Roots

- `<current-workdir>/skills`
- `~/.codex/skills`
- `~/.agents/skills`
- `~/.claude/skills`
- `~/.claude/skills/anthropic-skills/skills`
- `~/.config/opencode/skills`
- `~/.openclaw/skills`
- `~/.openclaw/extensions/*/skills`

## Quick Start

Install into your main hosts:

```bash
git clone https://github.com/LearnPrompt/skill-sync.git
cd skill-sync
./install.sh --codex --claude --openclaw --agents
```

Scan everything:

```bash
python3 scripts/skill_sync.py
```

Export the current topology as a migration manifest:

```bash
python3 scripts/skill_sync.py \
  --adopt-root agents \
  --export-manifest .skill-sync/agent-layout.json
```

Preview that layout on another machine:

```bash
python3 scripts/skill_sync.py \
  --import-manifest .skill-sync/agent-layout.json
```

Apply it with backups:

```bash
python3 scripts/skill_sync.py \
  --import-manifest .skill-sync/agent-layout.json \
  --apply
```

Show only shared and host-specific skills:

```bash
python3 scripts/skill_sync.py --status shared,specific --list-names
```

Inspect a compatibility conflict:

```bash
python3 scripts/skill_sync.py --diff rapid-ocr
```

Preview safe dedupe:

```bash
python3 scripts/skill_sync.py --dedupe --strategy strict
```

Preview a full convergence onto the shared agent root:

```bash
python3 scripts/skill_sync.py --adopt-root agents
```

Apply that convergence:

```bash
python3 scripts/skill_sync.py --adopt-root agents --apply
```

Restore the latest run:

```bash
python3 scripts/skill_sync.py --restore latest
python3 scripts/skill_sync.py --restore latest --apply
```

## Example Output

```text
Discovered 99 unique skills from 183 installs.
Hygiene score: 46/100 (risky) | shared_ratio=38.4% | review=2 | duplicates=20

RECOMMENDED ACTIONS
- [high] Review 2 compatible skills before dedupe
- [medium] Deduplicate 20 identical multi-host skills
- [low] Preview a single-root convergence plan
```

The point is not just to list skills. The point is to tell you what to do next.

## Validation

Run the fast local checks:

```bash
python3 -m py_compile scripts/skill_sync.py
python3 -m unittest discover -s tests -q
```

## Status Model

- `shared`: multiple hosts already point to the same real path
- `duplicate`: portable installs match exactly but live at different real paths
- `compatible`: portable installs share a name but differ in content
- `specific`: found on only one host
- `mixed`: same name exists with incompatible formats or host-specific layouts

## Strategy Model

- `strict`: only dedupe identical portable skills
- `prefer-latest`: keep the newest portable copy when content differs
- `trust-high`: same canonical logic as `prefer-latest`, but allows more aggressive replacement of scanned roots

## Superpowers

### Hygiene Score

Every scan computes a rough operational score so you can tell whether your local skill ecosystem is clean or drifting.

### Recommended Actions

The report suggests next steps instead of dumping raw data only.

### File-Level Diff

Use `--diff <skill>` to compare portable installs against the selected canonical source and see which files changed, were added, or removed.

### Root Adoption

Use `--adopt-root agents` or another root to preview or apply a convergence plan around one canonical host.

### Cross-Machine Migration

Use `--export-manifest` to save the desired symlink topology and `--import-manifest` to recreate that topology elsewhere.

The manifest records:

- which skills are portable enough to converge
- which host should act as canonical source
- which primary hosts should expose each skill

The manifest does not copy skill payloads themselves. On the target machine, the canonical source still needs to exist locally.

## About `~/.agents/skills`

If you already use `~/.agents/skills` as a shared skill library, that works especially well with `skill-sync`.

By default:

- it participates in discovery
- it often becomes the canonical source because it is first in the default source order

That is usually desirable. If you want a different preference order:

```bash
python3 scripts/skill_sync.py --source-order workspace,codex,claude,agents,opencode,openclaw
```

## Backup Model

Applied runs are written to:

```text
~/.skill-sync/backups/<run-id>/
```

Each run stores:

- `manifest.json`
- `originals/...`
- `latest`

This makes dedupe reversible. A real directory is moved to backup before a symlink replaces it.

## Install Script

`install.sh` supports:

- `--codex`
- `--agents`
- `--claude`
- `--opencode`
- `--openclaw`
- `--all`
- `--copy`
- `--force`

Examples:

```bash
./install.sh --all
./install.sh --codex --claude --force
./install.sh --openclaw --copy
```

## Project Layout

```text
.
├── SKILL.md
├── README.md
├── install.sh
├── agents/openai.yaml
├── references/compatibility.md
└── scripts/skill_sync.py
```

## License

MIT
