---
name: Minecraft
slug: minecraft
version: 1.0.0
homepage: https://clawic.com/skills/minecraft
description: Plan, build, troubleshoot, and optimize Minecraft worlds, commands, redstone, mods, and servers without mixing Java and Bedrock advice.
changelog: Initial release with edition-aware planning, building, redstone, command, survival, and server workflows.
metadata: {"clawdbot":{"emoji":"🧱","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/minecraft/"]}}
---

# Minecraft

Minecraft workflow for real play decisions. Use this when the agent must help with world planning, survival progression, builds, commands, redstone, modded setups, or server issues without blending edition-specific rules.

## When to Use

Use this skill when the task is actually about Minecraft execution, not generic gaming chat.

Typical activation moments:
- when the user needs a build plan, farm layout, or resource estimate
- when a command, datapack, redstone machine, or automation chain is failing
- when Java vs Bedrock differences change the answer
- when a world upgrade, modpack change, or server setup needs a safer path
- when the user wants a survival route, boss prep checklist, or progression shortcut
- when coordinates, dimensions, spawn logic, chunk behavior, or mob rules matter

## Architecture

Memory lives in `~/minecraft/`. If `~/minecraft/` does not exist, run `setup.md`. See `memory-template.md` for structure.
Persistence is optional: if the user wants one-off help only, keep the work session-only and do not create or update local files.

```text
~/minecraft/
├── memory.md        # edition, version, style, and activation defaults
├── worlds.md        # optional world seeds, key locations, and constraints
├── builds.md        # optional build briefs and recurring dimensions
├── servers.md       # optional server stack, mod loaders, and admin notes
└── archive/         # retired saves, old versions, and deprecated setups
```

## Quick Reference

Load only the file that matches the current lane so the answer stays practical instead of turning into a giant wiki dump.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Optional local memory schema | `memory-template.md` |
| Java vs Bedrock gating | `edition-gate.md` |
| Build planning template | `build-brief.md` |
| Redstone and farm debugging | `redstone-debug.md` |
| Commands and datapack patterns | `command-patterns.md` |
| Survival progression routes | `survival-routes.md` |
| Server, Realm, and modpack lanes | `server-lanes.md` |

## Requirements

- No credentials are required to install this skill.
- No external binaries are required.
- Runtime tools depend on the player's actual setup: vanilla world, Realm, dedicated server, mod loader, or admin console.
- Never assume operator rights, creative access, or command privileges unless the user says so.
- Require explicit confirmation before advising destructive world edits, rollback-hostile commands, or risky modpack changes.

## Core Rules

### 1. Gate on Edition, Version, and Authority First
- Confirm Java or Bedrock, approximate version, single-player or multiplayer, and whether the user has cheats, operator rights, or admin access.
- Minecraft advice breaks fast when edition, version, or permissions are wrong.
- If that surface is unclear, ask the smallest question that changes the answer before giving steps.

### 2. Work in Lanes, Not Mixed Advice
- Separate the task into one main lane: build planning, survival progression, commands/datapacks, redstone/farms, or server/modpack operations.
- Do not mix Java command syntax into Bedrock help, or survival assumptions into creative builds, unless the user explicitly wants both.
- If a task crosses lanes, solve the blocker first and keep the dependencies visible.

### 3. Translate Goals into Coordinates, Counts, and Checkpoints
- Good Minecraft help uses dimensions, block counts, spawn spaces, fuel/time estimates, and test checkpoints.
- Prefer "build a 17x17 interior with two-block walkways and mark chunk borders first" over vague aesthetic advice.
- Every plan should tell the user what to verify before they scale it.

### 4. Preserve World Safety Before Speed
- Recommend backups, test copies, or small-area rehearsals before destructive commands, version jumps, chunk loaders, or modpack updates.
- For command blocks and datapacks, start in a disposable test world if the blast radius is unclear.
- Never suggest `/kill`, `/fill`, `/clone`, `/tp`, or world-edit style operations against a live area without naming the risk.

### 5. Debug the Smallest Reproducible Slice
- For redstone and farms: isolate one module, one clock, one spawn rule, or one villager pathing segment at a time.
- For commands: reduce to the smallest selector, target, and output before adding conditions or scoreboards.
- For servers/modpacks: confirm version, loader, logs, and one failing mod or plugin before proposing broad rewrites.

### 6. Keep Mechanics Canonical and Version-Aware
- Distinguish between hard mechanics, community conventions, and aesthetic preferences.
- If a mechanic changed between versions, say so directly instead of acting certain.
- When exact rates depend on simulation distance, tick settings, or gamerules, call that out.

### 7. Optimize for the Player's Constraint, Not Your Favorite Meta
- Some users want fastest progression, some want low-risk survival, some want pretty builds, and some want minimal admin burden.
- Match the answer to their actual constraint: time, materials, skill level, server lag, platform, or co-op play.
- If the constraint is not stated, infer cautiously and make the assumption explicit.

## Operating Lanes

Start by naming the main lane before recommending blocks, commands, or hosting changes. That keeps the answer grounded in the actual job instead of mixing unrelated systems.

| Lane | First questions | Best file |
|------|-----------------|-----------|
| Build planning | edition, biome/style, scale, material budget, survival or creative | `build-brief.md` |
| Redstone or farm issue | edition, version, single-player/server, exact failure symptom | `redstone-debug.md` |
| Commands or datapacks | edition, version, command access, target behavior | `command-patterns.md` |
| Survival route | world stage, current gear, objective, risk tolerance | `survival-routes.md` |
| Server or modpack | hosting type, loader, version, player count, logs | `server-lanes.md` |

## Default Output Pack

When the task is substantial, prefer this shape:
- edition, version, and authority assumptions
- recommended lane and why
- step-by-step plan with dimensions, counts, or commands
- risk checks before irreversible actions
- what to test next if the first fix fails

If the user wants a fast answer, compress the same logic into a short plan plus one critical warning.

## Common Traps

Most bad Minecraft advice fails because it skips the gating step, not because the mechanic is complicated. Use these traps as a quick filter before giving a confident answer.

| Trap | Why It Fails | Better Move |
|------|--------------|-------------|
| Mixing Java and Bedrock syntax | Commands, redstone, and farm rules diverge fast | Gate on edition before giving steps |
| Designing with unlimited blocks in a survival task | The plan becomes unusable in practice | Start from material budget and progression stage |
| Rebuilding the whole contraption at once | Debug signal is lost | Isolate one module and verify it works alone |
| Upgrading world, loader, and mods together | Root cause becomes unreadable | Change one layer at a time with backup first |
| Giving exact mob rates without server settings | Tick and simulation differences change results | State assumptions and give tuning checkpoints |
| Using destructive commands as "quick fixes" | Live areas get damaged fast | Use test copies, boundaries, and explicit confirmation |
| Treating every build as aesthetic only | Function often matters first | Ask whether the priority is beauty, throughput, safety, or lag |

## Security & Privacy

**Data that leaves your machine:**
- None by default. This is an instruction-only Minecraft execution skill.

**Data stored locally:**
- Optional notes in `~/minecraft/` about edition, preferred play style, build constraints, and server context only if the user wants persistence.

**This skill does NOT:**
- download mods, shaders, or plugins automatically
- join servers, change files, or run undeclared network requests by itself
- assume operator privileges or destructive access
- store credentials, server IPs, or paid account data unless the user explicitly wants local notes

## Trust

This skill provides structured Minecraft guidance and optional local note patterns.
No credentials are required and no third-party services are contacted by default.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `gaming` - broader game strategy and player-facing decision support outside Minecraft-specific mechanics
- `server` - deployment and troubleshooting patterns for dedicated server hosting
- `home-server` - stable self-hosted infrastructure for private Minecraft servers at home
- `java` - Java runtime and tooling issues behind Java Edition launchers, mods, or dedicated servers
- `linux` - host administration when Minecraft runs on Linux boxes or containers

## Feedback

- If useful: `clawhub star minecraft`
- Stay updated: `clawhub sync`
