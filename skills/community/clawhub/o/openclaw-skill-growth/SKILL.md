---
name: openclaw-skill-growth
description: Make OpenClaw Skills observable, diagnosable, and safely improvable over time. Use this when the user wants to maintain many SKILL.md files, inspect repeated failures, generate improvement proposals, preview patches, run guarded apply flows, or verify whether skill changes actually improved outcomes.
version: 0.1.0
license: MIT-0
homepage: https://github.com/Shuai-DaiDai/openclaw-skill-growth
---

# OpenClaw Skill Growth

A ClawHub entry skill for the **OpenClaw Skill Growth** plugin.

It helps users discover and operate a GitHub project that turns static `SKILL.md` files into **observable, diagnosable, safely improvable capabilities**.

**Important:** this package is an entry skill and usage wrapper, not the full plugin source code.

## Best for

Use this skill when a user wants to:
- maintain a growing library of OpenClaw skills
- see which skills are repeatedly failing or underperforming
- generate reviewable improvement proposals from real run history
- preview patches before changing skill files
- apply updates with backups, version bumping, and change history
- dry-run a skill update process before writing anything
- evaluate whether a skill change actually improved outcomes

## Not for

Do **not** use this skill when the user only wants to:
- read or summarize a normal web page
- install an unrelated plugin
- optimize a workflow that has nothing to do with OpenClaw skills
- upload an entire TypeScript repository into ClawHub as if it were a single skill

## Core idea

The underlying project provides a maintenance loop for OpenClaw Skills:

**Observe → Diagnose → Propose → Apply → Evaluate**

## What the GitHub project includes

- skill registry from `SKILL.md`
- structured run observation
- diagnosis of recurring failures and weak outcomes
- improvement proposal generation
- patch preview generation
- guarded apply flows with backups
- version bumping and applied change history
- dry-run support
- evaluation record generation
- demo fixtures and CI

## Install the real project

```bash
git clone https://github.com/Shuai-DaiDai/openclaw-skill-growth.git
cd openclaw-skill-growth
npm install
npm run build
npm run test
```

## Common commands

```bash
npm run scan
npm run analyze
npm run propose
npm run report
npm run apply
npm run demo:dry-run
```

## Recommended usage path

1. Point the plugin at a skill directory.
2. Feed it run logs.
3. Run `report` or `analyze`.
4. Review diagnoses and proposals.
5. Use `demo:dry-run` first.
6. Apply only after review.
7. Compare outcomes and keep iterating.

## Why this is useful

Most skill systems stay static even while tools, environments, models, and task patterns keep changing.

This project is for users who want skill maintenance to become a **real operational loop** instead of a manual prompt-editing chore.

## GitHub source

- Repo: https://github.com/Shuai-DaiDai/openclaw-skill-growth
- Release: https://github.com/Shuai-DaiDai/openclaw-skill-growth/releases/tag/v0.1.0

## ClawHub note

This package is a **wrapper skill** around the GitHub project.

Use it to discover, install, and operate the plugin.
It is intentionally lighter than the full repository.
 package for discovery and installation guidance
