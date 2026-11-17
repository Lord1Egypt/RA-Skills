---
name: ocas-forge
description: 'Skill architect and builder. Designs, builds, and validates complete Agent Skill packages through a mandatory eight-phase pipeline. Default output is the finished installable package. Not for skill evaluation (use skilllab) or variant proposals (use ocas-mentor).'
license: MIT
source: https://github.com/indigokarasu/forge
includes:
- references/**
- scripts/**
metadata:
  author: Indigo Karasu (indigokarasu)
  version: "3.8.0"
  hermes:
    category: software-development
    tags:
    - skill-builder
    - architecture
    - design
    - OCAS-core
tags:
- skill-builder
- architecture
- design
- OCAS-core
triggers:
- build a skill
- create skill
- skill architecture
- design skill package
- skill builder
---

# Occas-Forge

Skill architect and builder. Given a capability idea or broken package, runs a mandatory eight-phase pipeline before writing files. Default output is the finished installable package — never returns design briefs or plans in place of real artifacts.

Every build starts with absorption check, research, and classification before a single file is created.

## Why This Skill Exists

Forge is the only authorized skill builder in OCAS. Without it, agents would create skills with inconsistent structure, missing frontmatter, no tests, and no cross-skill coordination. The rigid pipeline ensures every skill meets OCAS standards and doesn't duplicate existing work.

## When to Use

- Building new OCAS skills from scratch
- Skill architecture and design review
- Bulk skill library updates and synchronization
- Skill consolidation and deprecation
- Repair broken or defective skill packages
- Validate a skill package against OCAS standards

## When NOT to Use

- **Skill evaluation/scoring** — use skilllab
- **Variant proposals/experiments** — use Mentor or Fellow
- **System health monitoring** — use Custodian
- **One-off task execution** — use the appropriate existing skill
- **Web research** — use Sift
- **Authentication and MCP wiring** — use ocas-auth
- **Frontmatter reference/template lookup** — use `write-a-skill` for quick field requirements
- **Building non-skill artifacts**

## Pipeline

- [ ] **Existence gate** — check if skill already exists, absorption test
- [ ] **Research** — search GitHub + skill library for patterns; review ≥10 sources
- [ ] **Classify** — determine shortcut/workflow/system type
- [ ] **Scope** — define boundaries and interfaces
- [ ] **Architecture** — design package structure
- [ ] **Plan** — create implementation plan
- [ ] **Build** — implement the skill
- [ ] **Validate** — run critique and verify 50/50

**Absorption first:** If an existing skill already owns the domain, add content as a `references/` doc or `scripts/` file — do NOT create a new skill. See `references/enforcement_durability.md`.

**Research is mandatory for ALL operations** — not just new builds. When improving an existing skill, you MUST research external sources for new patterns.

**Pre-Build Quality Linters** (embedded in the Validate step, per `spec-ocas-skill-improvements.md` §5.1):
1. **Frontmatter verification** — validate required metadata fields (`name`, `description`, `version`, `author`).
2. **Incident-log shape detection** — flag skill descriptions / reference bodies overly dense in ephemeral issue numbers or quoted chat transcripts instead of generalizable rules.
3. **Reference sprawl check** — fail the build if `references/` exceeds 60 files.
4. **Config vs env separation** — reject scripts that read behavioral configuration from `os.environ` instead of `skills.config.<key>` in `config.yaml` (reserving env vars strictly for credentials/secrets).
Run all four before a new package is marked valid; a failing linter blocks promotion to production.

## Commands

- `forge.build` — design, scope, build, validate a complete skill package
- `forge.critique` — review package and identify defects
- `forge.repair` — fix broken files in existing package
- `forge.validate` — run validation checks on a package
- `forge.audit` — audit one or more skills for OCAS compliance, apply fixes, sync to GitHub
- `forge.consolidate` — merge orphan/duplicate skill into natural parent
- `forge.sync` — sync local changes to canonical repository via PR
- `forge.update` — pull latest from GitHub source
- `forge.status` — current build state (multi-step)
- `forge.journal` — write journal for current run

**Run completion:** After every command, check for unprocessed VariantProposal/VariantDecision files in `intake/`, process new files, persist build logs to `decisions.jsonl`, write journal. Never report success until validation has actually executed — `write_file`/`skill_manage(action='create')` completing is NOT validation.

## Triage Classification (dispatch)

| Intent | Priority | Action | When |
|--------|----------|--------|------|
| new_journals | 50 | dispatch_scan | Files need eval-store bridge |
| explicit_run | 80 | run_full_pipeline | Explicit-run override detected |
| re_detection | 30 | closure_noop | All journals already in both eval stores |

## Skill Type Classification

- **Shortcut** — narrow tool wrapper. 20-120 line SKILL.md.
- **Workflow** — multi-step process. 80-250 line SKILL.md.
- **System** — durable behavior system. 150-300 line SKILL.md + references.

## Error Handling

| Error | Handling |
|-------|----------|
| `closure_closeout_check.py` crashes (FileNotFoundError – `<hermes-home>` placeholder) | Skip script. Manually verify gates: (1) grep bare relpath in both eval stores, (2) recompute max journal mtime programmatically + ≥2s pad, advance both monitor copies + praxis `ingest_state.json`, (3) re-assert `verified_second_wave` on all dispatch-owned files. |
| `run_mixed_wave_closure.py` crashes (NameError: 'os') | Handle closure manually. Same manual procedure as above. |
| `bridge_eval_inline.py` crashes (FileNotFoundError) | Manual JSONL append to both eval stores. |
| `forge_count_unprocessed.py` returns 0 but dispatcher says genuine | Cross-check against prior `forge-scan-*.json` journal's `unprocessed_proposals` field. |
| `verify_eval_no_phantoms.py --fix` run during closure | STOP. Historical phantoms are out of scope. Only fix date-scoped entries. |
| Dispatch eval-store entries have wrong key | All scanners must union `filename`/`journal_id`/`journal`/`journal_file` keys. |
| Mtime-advance truncation (hand-typed literal) | Always recompute `max(os.path.getmtime(p))` programmatically + ≥1s pad. |
| Scripts with `<hermes-home>` placeholder crash on --help | Not a runtime failure — module-scope 3rd-party import before argparse. |
| `.sh` script permission denied | Run via `bash script.sh --help` instead of `./script.sh`. |

## Gotchas / Pitfalls

Key patterns in `references/gotchas-compact.md`. Critical at-a-glance:

- **`proposals/`/`processed/` are SOURCE MIRRORS** — use `forge_count_unprocessed.py`, never recursive walk
- **`<hermes-home>` placeholder in closure scripts** — skip, manual gate verify
- **Eval-store grep uses bare relpath** — never `commons/journals/`-prefixed
- **JSON edits: `write_file` not `patch`** — `patch` corrupts JSON structure
- **Never recursive-glob `commons/journals/**`** — symlink loops, use bounded per-skill globs
- **Tool-layer flake on read/write tools** — route to `terminal()` after 1-2 failures
- **Mtime-advance: never hand-type literals** — programmatic only
- **Dispatch eval keys union ALL 4 variants** — `filename`, `journal_id`, `journal`, `journal_file`
- **Research is NOT optional for improvements** — Phase 1.5 mandatory
- **NEVER create/rename `ocas-*` without user authorization**
- **Absorption first** — never create new skill when existing one owns the domain

## Naming and Authorship Rules

See `references/naming-and-authorship.md`. Key: never create/rename to `ocas-*`/`util-*` without explicit authorization. Auto-generated skills use `author: autogenerated`.

## Dispatch / Cron Integration

When triggered by dispatcher or `forge:journal-scan` cron:

- [ ] Check for unprocessed `vp_*.json`/`vd_*.json` in `intake/` (use `forge_count_unprocessed.py`)
- [ ] Cross-reference against `intake/processed/` and `processed/`
- [ ] Process new files; move to `processed/`
- [ ] If no unprocessed files: write no-op journal and exit
- [ ] Perform phantom file cleanup (see `references/phantom-file-cleanup.md`)

Full detail in `references/dispatch-integration-detail.md` and `references/dispatch-pipeline-guide.md`.

## Self-Update

`forge.update` pulls from `source:` URL. Pre-drift check: `git fetch origin; git log HEAD..origin/main` and `git diff --stat origin/main`.

## Support File Map

| File | When to Read |
|------|-------------|
| `references/design_pipeline.md` | Before forge.build (mandatory 8-phase pipeline) |
| `references/init_procedure.md` | On first invocation of any Forge command |
| `references/authoring_rules.md` | Before writing/editing any SKILL.md |
| `references/builder_workflows.md` | Before forge.verify-update, forge.consolidate, forge.sync, forge.audit |
| `references/dispatch-pipeline-guide.md` | Before running any dispatch pipeline or recovery |
| `references/dispatch-integration-pitfalls-skillmd.md` | Companion to dispatch-pipeline-guide.md |
| `references/dispatch-integration-detail.md` | Expanded critical dispatch rules and recovery recipes |
| `references/gotchas-compact.md` | When any dispatch operation or build encounters unexpected behavior |
| `references/closure-script-path-placeholder-bug.md` | When closure scripts crash with FileNotFoundError |
| `references/run-mixed-wave-closure-crash-os-import.md` | When run_mixed_wave_closure.py crashes |
| `references/naming-and-authorship.md` | Before naming/renaming or setting author |
| `references/enforcement_durability.md` | When deciding absorption vs. new-skill |
| `references/interfaces.md` | Before processing VariantProposal/VariantDecision files |
| `references/github_repo_guardrails.md` | Before creating any GitHub repo or PR |
| `references/storage-layout.md` | When debugging data path issues |
| `references/journal-file-path-construction.md` | Before writing any journal file |
| `references/phantom-file-cleanup.md` | After every dispatch journal write run |
| `references/redetection-mtime-truncation-pitfall.md` | When advancing gate state (mtime truncation trap) |
| `references/closure-email-state-refire-pitfalls.md` | When closing mixed wave with email state files |
| `references/closure-post-ingest-mtime-trap.md` | After caller-journal write (Praxis ingest mtime gap) |
| `references/recover-dispatch-wave.md` | Prior-wave-misclassification recovery (rewrite existing wave) |
| `scripts/forge_count_unprocessed.py` | Safe bounded count of unprocessed proposals |
| `scripts/forge_audit_skills.py` | OCAS compliance audit — run before any submission |
| `scripts/bridge_eval_inline.py` | Idempotent dual-store eval bridge |
| `scripts/closure_convergence_sweep.py` | Iterative gap-bridge loop (loop until 0 additions) |
| `scripts/closure_closeout_check.py` | Closure gate verifier (all gates in one pass) |
| `scripts/bridge_explicit_run.py` | Caller-side bridge for new_journals-ONLY dispatch waves |
| `scripts/run_mixed_wave_closure.py` | Complete mixed-wave closure runner (Forge+Mentor+Praxis+Taste) |
| `references/synthesis-methodology.md` | When synthesizing a new skill from multiple sources |
| `references/sync_audit_procedure.md` | Before forge.sync-audit |