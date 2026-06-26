# Adapting CLI-Anything into OpenClaw

CLI-Anything is a methodology repo plus plugin/command assets, not a native OpenClaw skill package.

## Safe adaptation pattern

1. Keep OpenClaw `SKILL.md` short and procedural
2. Store heavier methodology in references
3. Point to the local `CLI-Anything/` checkout as the implementation source
4. Distinguish clearly between:
   - plugin commands for Claude Code / OpenCode
   - local Python harnesses
   - OpenClaw skill wrappers

## Good packaging targets

### Option A — method skill

Create an OpenClaw skill that teaches the agent how to:

- inspect the local CLI-Anything repo
- choose a harness or target app
- verify dependencies
- adapt generated outputs into OpenClaw-friendly workflows

### Option B — concrete harness skill

Wrap one concrete generated CLI, for example a `cli-anything-libreoffice` workflow.
This is often easier to test than packaging the whole methodology.

## Publishing cautions

Before publishing to ClawHub:

- verify there is real implementation value beyond copied docs
- avoid bundling unnecessary large third-party source trees in the skill unless intentionally distributing them
- make sure the description says whether the skill is:
  - methodology only
  - a wrapper around a local repo
  - a distributable harness with runnable scripts

## Recommended wording

Prefer wording like:

- "Uses a local checkout of CLI-Anything to guide harness generation"
- "Wraps existing CLI-Anything harnesses for OpenClaw workflows"

Avoid wording like:

- "Provides full CLI-Anything functionality" unless you actually wired all of it up
