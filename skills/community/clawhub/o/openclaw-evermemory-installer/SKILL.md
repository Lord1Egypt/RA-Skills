---
name: openclaw-evermemory-installer
description: Use this skill when installing, upgrading, verifying, or publishing the EverMemory OpenClaw plugin and its companion skill, including local path install, npm install, ClawHub publish, and release-gate verification.
---

# OpenClaw EverMemory Installer

## Overview

This skill standardizes the end-to-end operator workflow for EverMemory:
- install plugin into OpenClaw (`openclaw plugins install`)
- bind and verify runtime (`plugins.slots.memory=evermemory`)
- publish/install the companion skill through ClawHub (`clawhub publish/install`)
- prepare and publish plugin package (`npm publish`)

Use this skill whenever the user asks to:
- install EverMemory in a new OpenClaw instance
- upgrade EverMemory safely with validation
- publish EverMemory skill to the OpenClaw skill site (ClawHub)
- publish EverMemory plugin package for `openclaw plugins install <npm-spec>`

## Quick Workflow

1. Run release gates first:
```bash
npm run teams:dev
npm run teams:release
```

2. Install plugin from local repo path:
```bash
bash scripts/install_plugin.sh --source local --link --bind-slot --restart-gateway
```

3. Verify runtime:
```bash
bash scripts/verify_install.sh
```

4. Publish skill to ClawHub:
```bash
bash scripts/publish_skill.sh --version 0.1.0 --changelog "Initial public release"
```

5. Publish plugin to npm:
```bash
bash scripts/publish_plugin.sh --dry-run
# remove --dry-run when ready and logged in
```

## Installation Modes

Use one of these plugin install paths:

1. Local workspace path (recommended for development):
```bash
bash scripts/install_plugin.sh --source local --link
```

2. Package archive (`.tgz`/`.zip`):
```bash
bash scripts/install_plugin.sh --source archive --value /tmp/evermemory-release/evermemory-0.0.1.tgz
```

3. npm spec:
```bash
bash scripts/install_plugin.sh --source spec --value your-scope/evermemory@0.0.1
```

## Publish Requirements

Before publishing skill or plugin:
- `clawhub whoami` must succeed
- `npm whoami` must succeed
- `npm run teams:release` must pass
- recall benchmark must remain `>=0.90` (target `>=0.95`)

If `clawhub whoami` fails, run:
```bash
clawhub login
```

If `npm whoami` fails, run:
```bash
npm login
```

## Script Reference

- `scripts/install_plugin.sh`
  - Installs EverMemory plugin via local/spec/archive
  - Optional slot bind + gateway restart
- `scripts/verify_install.sh`
  - Validates gateway/plugins/slot binding
- `scripts/publish_skill.sh`
  - Publishes the skill folder to ClawHub
- `scripts/publish_plugin.sh`
  - Runs release pack + npm publish (supports `--dry-run`)

## Safety Rules

1. Never publish when `teams:release` fails.
2. Never force-enable plugin without checking `openclaw gateway status`.
3. Never claim publish succeeded without capturing command output and artifact path.
4. Prefer `--dry-run` first for npm publish.

## More Details

For detailed command matrix and failure handling, read:
- `references/publish-and-install-playbook.md`
