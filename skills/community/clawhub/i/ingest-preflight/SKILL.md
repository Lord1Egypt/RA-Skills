---
name: ingest-preflight
description: Before publishing to ClawHub, validate a skill-shaped folder (required files, frontmatter, size, auth, slug availability, and a dry-run publish) with one script. Use when authoring or packaging a skill and you want to catch structural problems before the real publish.
metadata:
  clawdbot:
    emoji: "🛫"
    requires: ["clawhub"]
    tags: ["preflight", "publish", "packaging", "quality"]
  version: "1.0.0"
  license: MIT
---

# ingest-preflight

A tiny, honest gatekeeper for the **数字资源入库** step. Run it on a packaged
skill folder before `clawhub publish`; it tells you exactly what is wrong so you
do not ship a broken asset.

## When to use

- You have just finished the upstream workflow (content review, metadata fill,
  folder packaging) and want one authoritative check before publishing.
- You want a repeatable command instead of ad-hoc `ls` / `head` inspection.
- You are teaching the "process → ingest" chain and need a visible gate.

## Prerequisites

- `clawhub` CLI installed and on `PATH`.
- Authenticated: `clawhub whoami` returns a publisher handle.
- The asset folder contains at least `SKILL.md` (frontmatter with `name` and
  `description`). `references/` is recommended.

## Run it

```bash
# from anywhere, point at the skill folder
bash scripts/preflight.sh /path/to/your-skill --slug your-unique-slug
```

What it checks (in order):

1. `SKILL.md` exists.
2. Frontmatter starts with `---` and contains `name` and `description`.
3. `references/` directory is present (warns, does not fail).
4. No file larger than 2M (warns).
5. `clawhub` CLI is present and `clawhub whoami` succeeds.
6. The proposed `--slug` is free (`clawhub inspect`).
7. **Authoritative gate:** `clawhub publish --dry-run` actually accepts the
   folder.

Exit code `0` = safe to publish; `1` = fix the listed failures first.

## Example (self-test)

```bash
bash scripts/preflight.sh . --slug ingest-preflight
```

## Why it exists

The business-process tool packages the asset; `clawhub` is the tool that
ingests it. This script is the deterministic handoff check between them — it
keeps the "process" and "ingest" tools honest by refusing to continue until the
asset is structurally valid.
