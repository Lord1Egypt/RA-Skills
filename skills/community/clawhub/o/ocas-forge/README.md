# 🔨 Forge

Forge is the system's skill architect -- given a capability idea or broken existing package, it runs a mandatory six-phase internal pipeline covering existence gate, classification, scoping, architecture, construction, and validation before writing a single file. The default output is the finished, installable package with all file contents written; Forge never returns design briefs or plans in place of the real artifact.

---

## Overview

Forge is the only place where new OCAS skills are designed and built. Rather than generating a plan or brief, Forge runs a mandatory six-phase internal pipeline (existence gate, classify, scope, architecture, build, validate) before writing a single file, and the output is always the finished, installable package. Mentor can also route improvement proposals to Forge via intake files, which Forge processes at each heartbeat pass. Skill packages are classified by type -- shortcut (20-120 lines), workflow (80-250 lines), or system (150-300 lines) -- and each type has its own structural expectations.

## Commands

| Command | Description |
|---|---|
| `forge.build` | Design, scope, build, and validate a complete skill package |
| `forge.critique` | Review a package and identify defects |
| `forge.repair` | Fix broken files in an existing package |
| `forge.classify` | Classify a proposed skill (shortcut, workflow, system) |
| `forge.validate` | Run validation checks on a package |
| `forge.scaffold` | Generate a minimal package skeleton |
| `forge.status` | Current build state if a multi-step build is in progress |
| `forge.journal` | Write journal for the current run |
| `forge.update` | Pull latest from GitHub source (preserves journals and data) |

## Setup

`forge.init` runs automatically on first invocation and creates all required directories, config.json, and JSONL files. It also registers the `forge:intake` heartbeat entry to process incoming VariantProposal and VariantDecision files from Mentor and `forge:update` (midnight daily, self-update). No manual setup is required.

## Dependencies

**OCAS Skills**
- [Mentor](https://github.com/indigokarasu/mentor) -- receives VariantProposal and VariantDecision files via intake directory

**External**
- None

## Scheduled Tasks

| Job | Mechanism | Schedule | Command |
|---|---|---|---|
| `forge:intake` | heartbeat | Every heartbeat pass | Process VariantProposal and VariantDecision files from Mentor intake |
| `forge:update` | cron | `0 0 * * *` (midnight daily) | Self-update from GitHub source |

## Changelog

### v2.3.0 -- March 27, 2026
- Added `forge.update` command and midnight cron for automatic version-checked self-updates

### v2.2.0 -- March 22, 2026
- Routing improvements

### v2.1.0 -- March 22, 2026
- Run completion with Mentor intake integration
- Initialization with heartbeat registration

### v2.0.0 -- March 18, 2026
- Initial release as part of the unified OCAS skill suite
---

*Forge is part of the [OpenClaw Agent Suite](https://github.com/indigokarasu) -- a collection of interconnected skills for personal intelligence, autonomous research, and continuous self-improvement. Each skill owns a narrow responsibility and communicates with others through structured signal files, shared journals, and Chronicle, a long-term knowledge graph that accumulates verified facts over time.*
