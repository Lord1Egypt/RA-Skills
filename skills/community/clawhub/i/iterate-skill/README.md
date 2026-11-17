# Iterate Skill

> **English** · [简体中文](./README.zh-CN.md)

<center>
  <strong>A portable, configurable AI coding assistant skill: fully automated multi-round code review and fixing.</strong>
</center>

<br/>

<p align="center">
  <a href="https://github.com/jingzhao-l/iterate-skill/blob/main/badges/downloads.json">
    <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjingzhao-l%2Fiterate-skill%2Fmain%2Fbadges%2Fdownloads.json&query=total&label=Total%20Downloads&style=for-the-badge&color=2ea44f&logo=download&logoColor=white" alt="Total Downloads">
  </a>
</p>

<p align="center">
  <a href="https://clawhub.ai/jingzhao-l/skills/iterate-skill"><img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjingzhao-l%2Fiterate-skill%2Fmain%2Fbadges%2Fdownloads.json&query=clawhub&label=ClawHub&color=4285F4&logo=cloudflare&logoColor=white" alt="ClawHub"></a>
  <a href="https://skillhub.cloud.tencent.com/"><img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjingzhao-l%2Fiterate-skill%2Fmain%2Fbadges%2Fdownloads.json&query=skillhub&label=SkillHub&color=624aff&logo=alibabacloud&logoColor=white" alt="SkillHub"></a>
  <a href="https://www.npmjs.com/package/iterate-skill-installer"><img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjingzhao-l%2Fiterate-skill%2Fmain%2Fbadges%2Fdownloads.json&query=npm&label=npm&color=CB3837&logo=npm&logoColor=white" alt="npm"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-yellow" alt="License"></a>
  <a href="https://github.com/jingzhao-l/iterate-skill/releases"><img src="https://img.shields.io/github/v/release/jingzhao-l/iterate-skill" alt="GitHub release"></a>
  <a href="https://github.com/jingzhao-l/iterate-skill"><img src="https://img.shields.io/github/stars/jingzhao-l/iterate-skill?style=social&label=Star" alt="GitHub stars"></a>
</p>

> Want to support this project? A GitHub **Star** is the best thank-you and helps more developers discover iterate.

---

## Table of Contents

- [About This Project](#about-this-project)
- [At a Glance](#at-a-glance)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [CLI Command Reference](#cli-command-reference)
- [How It Works](#how-it-works)
- [Configuration](#configuration)
- [FAQ](#faq)
- [Security](#security)
- [Directory Structure](#directory-structure)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)
- [License](#license)

---

## About This Project

**iterate** is an open-source project that gives AI coding assistants the ability to perform **multi-round, autonomous code review and fixing**. You don't need any background about an "iterate" concept — it solves a very concrete pain point:

> AI assistants often "talk a lot but do little": a single conversation touches only a few lines, looks at one file and never re-checks the whole, and rarely re-verifies what it broke. `/iterate` automates these small but critical finishing tasks — item-by-item review, per-dimension triage, fixing, verification, and iteration — so the AI truly finishes a change **completely and correctly**, like a senior engineer.

Its operating mechanism can be summarized as a self-closing pipeline:

```text
Set the goal → multi-dimension parallel review → atomic fixes + architecture fixes (with your approval) → verify → re-review → iterate until convergence / max rounds → output summary
```

The skill keeps evolving through major versions:

- **v2** — deterministic convergence: repeated multi-dimension review until a round finds zero new issues, plus isolated `iterate/*` branches and a decision log.
- **v3.0** — dual modes: the original `/iterate` review/fix loop stays untouched, and a new **defensive-programming mode** (`/iterate defensive`) covers everyday coding tasks (add features, fix bugs, refactor), hardened by deterministic `iterate guard` pre/post checks and an `invariant` delivery gate.
- **v3.1** — `iterate fingerprint` for non-blocking manifest-drift verification, a smarter `iterate doctor` that reports how many checks passed, and fail-closed guard semantics.

**iterate is not a standalone tool; it is a skill ecosystem that attaches to your existing AI assistants.** It doesn't replace your IDE or AI tools; instead it adds a strict "code gatekeeping" layer to your existing workflow. The ecosystem is made up of three components that share the same configuration and review dimensions:

- **Core Skill + CLI** — a portable AI skill `/iterate` + `iterate` CLI (root of this repo). Multi-round iteration inside the conversational UIs of Trae / Claude Code / Cursor / Copilot / Codex and 25+ assistants.
- **[iterate-harness](https://github.com/jingzhao-l/iterate-harness)** — a standalone headless engine, command `ih` (source `harness/iterate-harness`, npm: `iterate-harness`). Runs the same closed loop outside a conversational assistant — in the terminal / CI / git hooks.
- **[iterate-plugin](https://github.com/jingzhao-l/iterate-plugin)** — a dsh desktop-client plugin (source `harness/iterate-plugin`, npm: `iterate-plugin`). Brings iterate's convergence dashboard and review progress into the dsh desktop UI.

The relationship: the **skill** (this repo's core deliverable) targets conversational iteration in any AI assistant; the **harness** is the same closed-loop engine for headless / CI scenarios; the **plugin** re-plays the harness runtime inside dsh. The configuration (`iterate.config.yaml`) and dimension system are fully consistent across all three — understand one and you can transfer the rest.

**Related project: [GlassPane](https://github.com/jingzhao-l/GlassPane).** The JSON Schema contract layer in [`kernel/`](kernel) (`iterate-kernel`) is also the language spoken by GlassPane, a runtime verification engine for AI agents on macOS: an agent acts through MCP, and GlassPane returns evidence of whether the claimed UI change actually happened — accessibility-tree and pixel deltas, an attribution verdict, and a checkpoint to roll back to. iterate answers "is this code right?"; GlassPane answers "did that operation really take effect?". It is a deliberately separate concern: GlassPane does not read `iterate.config.yaml`, and it ships on its own release line.

The separation is not a wall: since 2026-10-25 the two halves exchange verifiable records — GlassPane's evidence ledger and the review loop's decision log are the same hash chain format, and a claim quoted from the other side's file is chain-verified before it is used. That reader lives on the loop's side today: the fork ships the same verifier and a fixed-point test proves a chain written here verifies there, while its own production path writes its ledger rather than reading the loop's. A `dimension` declaration travels with a verification call and a contradicting decision is refused, and the loop gates "the fix is done" on a chain-verified entry rather than on the agent's word. The commands are `ih iterate gate` / `ih iterate glasspane-ledger <path>` (and their `/iterate` twins); [the harness README](https://github.com/jingzhao-l/iterate-harness#-glasspane-integration) documents the whole exchange.

The harness and plugin can also be installed and used independently of this repo:

```bash
# iterate-harness: one-command install (npm wrapper, simplest)
npm install -g iterate-harness

# The harness repo also ships a shell installer. Pin a release tag and verify the
# checksum instead of piping `main` straight into a shell:
#   https://github.com/jingzhao-l/iterate-harness/releases
ih iterate init && ih iterate review

# iterate-plugin: GitHub install for the dsh desktop plugin
dsh plugin --profile web add github:jingzhao-l/iterate-plugin#main
```

> The harness bundles an OrcaRouter gateway provider (including a free model tier). Register via the [referral link](https://www.orcarouter.ai/ref/ref_5eca75a9c809c95ab152) to support the project; see the [iterate-harness README](https://github.com/jingzhao-l/iterate-harness) for setup guidance.

> The rest of this document focuses on the **skill (repo root)** and its most common conversational usage. Full docs for the harness and plugin live in their own repos: [iterate-harness](https://github.com/jingzhao-l/iterate-harness) (source `harness/iterate-harness/README.md`), [iterate-plugin](https://github.com/jingzhao-l/iterate-plugin) (source `harness/iterate-plugin/README.md`).

---

## At a Glance

**Iterate Skill** lets an AI assistant review and fix a codebase over multiple rounds, like a rigorous senior engineer.

- **Dual modes** — `/iterate` is the original multi-round review → fix → converge loop (v2 behavior, zero breakage); `/iterate defensive` is a defensive-programming mode for normal incremental coding tasks, ending in the same iterate convergence gate.
- **9 dimensions in parallel** — correctness, security, performance, architecture, style-tests, tech-debt, spec-compliance, frontend-backend, ui-ux.
- **Scope dimension sets** — named `dimension_sets` (e.g. `frontend`, `api`, `security`) preset at onboarding; a scoped goal routes to the matching set, off-catalog scopes trigger an on-the-fly redefinition recorded in `.iterate_decisions.md` (never copied from presets).
- **Two-track fixing** — atomic issues (≤20 lines, single file) are fixed automatically; architecture issues are fixed only after your approval.
- **Deterministic gate CLI** — `iterate guard pre-check` / `post-check` + `iterate invariant` — exact, fail-loud checks the host AI runs before/after every edit and at delivery (defensive mode).
- **Git isolation** — each round runs on an isolated `iterate/*` branch or worktree; merge/push is off by default and must be explicitly enabled.
- **Secure-by-default** — `push_per_round` and `auto_merge` default to `false`.
- **Command whitelist** — double validation at config time and personalization time; rejects dangerous shell metacharacters.
- **Checksum & verification** — enforces SHA256 verification when updating from GitHub Release.
- **Multi-assistant support** — Trae, Claude Code, Cursor, Windsurf, GitHub Copilot, Codex, Roo Code and 25+ tools.
- **Project knowledge base** — auto-generates `ITERATE.md` + `iterate.config.yaml`, with drift detection and incremental refresh.

---

## Quick Start

### 1. Install the skill

```bash
npx iterate-skill-installer
```

It auto-detects your installed AI coding tools and interactively lets you choose which assistants to install into. Use `--ai <name>` to target a single assistant directly. The installer also installs the `iterate` CLI (for step 2's `iterate onboard`, etc.) — one command installs skill + CLI.

### 2. Enter a project and complete onboarding

```bash
cd /path/to/your-project
iterate onboard
```

`iterate onboard` generates your project's knowledge base:

- `ITERATE.md`: tech stack, module map, conventions, forbidden areas, and more
- `iterate.config.yaml`: iteration goal, review dimensions, validation commands, and more

### 3. Start iterating

In your AI assistant's conversation, type:

```text
/iterate "improve code quality, ensure all functions are ≤80 lines and tests pass"
```

Or launch the CLI directly in the terminal:

```bash
iterate status      # view onboarding status and drift
iterate refresh     # incrementally refresh ITERATE.md
iterate personalize # add project-specific constraints
```

---

## Installation

### Recommended: one-command npx install (for most users)

No repo cloning, no manual Python environment setup — one command downloads, verifies, and installs the skill, and also installs the `iterate` CLI:

```bash
# Auto-detect installed AI assistants and choose interactively
npx iterate-skill-installer

# Install only into Trae
npx iterate-skill-installer --ai trae

# Install into a specific project directory
npx iterate-skill-installer --target /path/to/project

# Force-overwrite a previously installed skill
npx iterate-skill-installer --ai trae --global --force
```

Common options:

- `--ai <name>` — install only into a specific assistant, e.g. `trae`, `claude`, `cursor`
- `--target <path>` — project-level install into a directory
- `--global` — install into the user home directory (default)
- `--force` — overwrite existing skill files
- `--token <token>` — GitHub token to raise API rate limits
- `-h, --help` / `-v, --version` — show help / version

> **The installer puts the `iterate` CLI on your PATH** (prefer `pipx` isolated install, else `pip install --user`) so that `npx iterate-skill-installer` completes "skill + CLI" in one command. That does place an executable on your system. If you don't want automatic CLI install, use the "manually copy SKILL.md" or "source scripts" approaches below instead.
>
> The installer requires Node.js 18+ and Python 3.10+. It creates an isolated Python virtualenv, installs dependencies, and calls `scripts/install.py` to copy files. When downloading a release it forces verification against `SHA256SUMS.txt` — install is rejected on mismatch. If the `iterate` command fails to install, you can still install it manually with `pipx install .` or `pip install .`.

### Other install methods

If you can't use npm, or you want full control over the install, use one of these.

#### Method A: install the iterate CLI locally

`npx` one-command install already installs the `iterate` CLI. If you didn't use npx, or want to install/upgrade the CLI manually:

```bash
git clone https://github.com/jingzhao-l/iterate-skill.git
cd iterate-skill

# Recommended: isolated install with pipx
pipx install .

# or plain pip
pip install .

# verify
iterate --version
```

After install you can use `iterate onboard`, `iterate personalize`, `iterate status`, `iterate refresh`, `iterate reonboard` in any project directory.

#### Method B: manually copy the skill directory

> ⚠️ **You must copy the entire `iterate/` directory, not just `SKILL.md`.** `SKILL.md` resolves `config/`, `scripts/validate.py`, and `templates/` at runtime relative to its install directory. Copying only one file causes `/iterate` to fail because it can't find the config and validation scripts.

If you don't want to use the npx installer, copy the whole skill directory to the assistant directory:

```bash
# Clone or download the source first to get an iterate/ dir with SKILL.md, config/, scripts/, templates/
git clone https://github.com/jingzhao-l/iterate-skill.git
SKILL_DIR=$(pwd)/iterate-skill

# Trae
mkdir -p ~/.trae/skills/iterate
cp -R "$SKILL_DIR"/SKILL.md "$SKILL_DIR"/config "$SKILL_DIR"/scripts "$SKILL_DIR"/templates ~/.trae/skills/iterate/

# Claude Code
mkdir -p ~/.claude/skills/iterate
cp -R "$SKILL_DIR"/SKILL.md "$SKILL_DIR"/config "$SKILL_DIR"/scripts "$SKILL_DIR"/templates ~/.claude/skills/iterate/

# Cursor
mkdir -p ~/.cursor/skills/iterate
cp -R "$SKILL_DIR"/SKILL.md "$SKILL_DIR"/config "$SKILL_DIR"/scripts "$SKILL_DIR"/templates ~/.cursor/skills/iterate/
```

For more tool paths, see the "tool mapping table" in [`SKILL.md`](./SKILL.md).

#### Method C: source scripts (for developers)

```bash
git clone https://github.com/jingzhao-l/iterate-skill.git
cd iterate-skill

python scripts/install.py install --ai trae --global
python scripts/install.py update --ai trae --target /path/to/project
python scripts/install.py uninstall --ai trae --target /path/to/project --yes
```

### Global vs. project-level install

- **Global install** (`~/.trae/skills/iterate/`) — the first `/iterate` invocation triggers onboarding in every project.
- **Project-level install** (`/project/.trae/skills/iterate/`) — after onboarding it reuses the project root's `ITERATE.md`, no repeated onboarding.

Suggestion: install globally once so the assistant "gets to know you"; then do a project-level install in important projects to avoid repeated onboarding.

### Why not skills.sh?

This project was previously distributed on skills.sh / SkillHub and other platforms. Since v2.1, **`npx iterate-skill-installer` is the recommended unified install method** because:

1. **One command**: auto-download, SHA256 verify, environment prep, assistant selection — no manual cloning or file copying.
2. **Consistent versions**: always installs from the GitHub Release, avoiding version drift from platform caches.
3. **Unified across assistants**: one install logic supports 25+ AI assistants instead of each platform maintaining its own.
4. **Secure & verifiable**: forces verification against `SHA256SUMS.txt`; install is rejected on mismatch.

Marketplace pages like skills.sh remain for display and discovery but are no longer the primary install entry.

---

## Usage

### In an AI assistant

After installing the skill, type these into any AI tool that supports it:

```text
/iterate "your goal"
/iterate "your goal" 10
/iterate "your goal" no-limit
/iterate "review code quality" review-only    # pure review mode: review repeatedly to zero findings, read-only
/iterate "full health check" --dry-run # pure review alias: review report + meta-review final report
/iterate defensive "add user login + fix the payment bug"   # defensive-programming mode (v3.0): from design to delivery
```

The first invocation auto-triggers onboarding (if the project has no `ITERATE.md`).

> **Defensive-programming mode (`/iterate defensive`)**: when you want the AI to do **normal incremental coding work** — add features, fix bugs, refactor, wire up an API, add tests — instead of a pure review, use `/iterate defensive`. The host AI carries defensive-programming discipline from start to finish: declare assumptions + run `iterate guard pre-check` before touching code, validate at trust boundaries with minimal steps while editing, run `iterate guard post-check` after every change, and finish with `iterate invariant` plus the full 9-dimension review→fix→converge loop as a **delivery gate**. It does not deliver until everything converges. The original `/iterate` mode (v2) is unchanged.

> **Pure review mode / review-only (dry-run)**: when the invocation contains `review-only` or `dry-run`, this skill does a read-only health check and **never modifies any file**. It repeatedly reviews in parallel until a round yields 0 new findings (convergence), produces a review report, then **reviews that report itself** (meta-review, checking internal consistency) and gives a final report with an `approved` / `needs_revision` verdict. Use it for pre-release health checks, code quality audits, or when you don't want the AI to touch code.

### In the terminal

```bash
# Interactive onboarding (auto-branches on first/non-first use)
iterate onboard

# Add / view / clear personalization constraints mid-way
iterate personalize          # enter the 9-step personalization wizard
iterate personalize --clear  # clear all personalization (structured rules + ITERATE.md sections)
iterate personalize --clear --yes  # skip confirmation
iterate show                 # read-only merged config + personalization details (--json for structured output)

# Guided next action: what to run now, and why (read-only; always exits 0)
iterate next                 # fresh project -> init/onboard; drift -> refresh --diff; failing checks -> doctor --fix; healthy -> /iterate "<goal>"
iterate next --json          # stable plan for scripts/CI: state, blocking, drift, next, steps, notes

# View onboarding status and drift detection
iterate status

# Incremental refresh (keeps hand-written ITERATE.md section)
iterate refresh
iterate refresh --diff        # preview the EXACT unified diff a refresh would apply (writes nothing)
iterate refresh --dry-run     # preview line counts only (writes nothing)

# Full re-onboarding (backs up old files)
iterate reonboard

# Verify manifest fingerprints vs the recorded ones (non-blocking drift check)
iterate fingerprint           # verify (default): exits 0 = no drift, 1 = added/removed/changed manifests
iterate fingerprint --json    # structured JSON output (script-friendly)

# Non-interactive config inspection & editing (no wizard)
iterate config                      # list all settable values
iterate config get max_rounds      # read one resolved value (--json for {"key": value})
iterate config set goal "..."      # validate + write one value (auto timestamped backup)

# Defensive-programming deterministic checks (v3.0 defensive mode)
iterate guard pre-check src/        # before editing: target exists / worktree clean / manifests ready
iterate guard post-check python     # after editing: run exactly validation.commands.<module>
iterate invariant                   # at delivery: file-assertions + exact commands (degrades to validation.commands)

# List, restore or prune the timestamped backups write commands leave behind
iterate backup list                 # enumerate *.configset-* / *.doctorfix-* / *.refresh-* / *.bak-* etc.
iterate backup restore <file>       # restore one backup (backs up the current file first; reversible)
iterate backup prune --keep 5       # keep the 5 newest backups of each original file, delete the rest
iterate backup prune --older-than 30d  # delete any backup older than 30 days (7d/24h/90m also accepted)
```

> **Recommended new-user path**: `npx iterate-skill-installer` (install) → `iterate onboard` (init) → `iterate doctor` (optional health check) → `iterate personalize` (optional constraints) → `/iterate "your goal"` in your AI assistant, or `iterate status` / `iterate refresh` / `iterate personalize` on the CLI.
>
> Not sure where you are? Run **`iterate next`** — it inspects the project and prints the single next command (plus follow-ups and environment gaps), so you do not need to read this table first. `iterate next --json` returns the same plan for scripts and other skills.
>
> The first `/iterate` invocation will do onboarding first if the project has no knowledge base — seeing a "initializing project" message is normal, not a failure. After that, every round's changes stay on an isolated `iterate/*` branch/worktree; merge/push is off by default and happens after you review.

### Edge Cases

- **Onboarding cancelled mid-way (Ctrl+C / "skip")**: no half-finished artifacts. All files are written **atomically** (`tempfile + os.replace`), so nothing is left behind — just re-run.
- **Hand-written `ITERATE.md` missing `USER-OWNED` markers**: `iterate refresh` (and AI refresh) **refuses to overwrite and errors** instead of destroying your hand-written content. Add `<!-- ITERATE:USER-OWNED:START/END -->` markers to refresh normally.
- **Non-git project**: `onboard` / `status` / `refresh` / `doctor` / `personalize` don't depend on git and work directly; but the git-isolated branch/merge/push steps in `/iterate` need a git repo — without one those steps are skipped or prompted.
- **Empty project / no manifest files**: onboarding generates the knowledge base normally; without fingerprint files like `package.json` / `pyproject.toml`, drift detection skips fingerprint comparison.
- **Corrupted `iterate.config.yaml` (YAML error / schema violation)**: `iterate status` distinguishes a **present-but-unparsable** config (exit 1, "could not be parsed", suggests `iterate doctor`) from a **missing** one (exit 0, "config not found — only ITERATE.md exists" hint); `iterate doctor` reports schema errors; `doctor --fix` only fixes safely auto-fixable items, the rest need manual fixing. If config fails schema validation, `/iterate` aborts immediately with an error rather than running with a broken config.
- **Early convergence**: when a round returns 0 new findings, iteration ends early (Early Stop) instead of running to `max_rounds`.

---

## CLI Command Reference

### iterate doctor (project health diagnostics)

`iterate doctor` checks your project against the skill's own spec to catch drift early. It verifies:

- **Onboarding completeness** — `ITERATE.md` and `iterate.config.yaml` exist
- **Config parses & is valid** — config parses as YAML and **fully** matches `config/config.schema.json`
- **Dimensions valid** — `dimensions` only reference one of the 9 spec dimensions
- **Review scope valid** — `review.scope` allows only `full` / `changed-only`
- **Merge target branch** — `git.target_branch` is a non-empty string
- **Validation commands** — `validation.commands` is a non-empty string list
- **Command whitelist** — `command_whitelist` entries are safe and every command is within the whitelist
- **Personalization dimension refs** — `personalization` dimension references point to enabled dimensions
- **Version consistency** — onboarding `skill_version` matches the currently installed skill version
- **Drift detection** — whether the tech-stack manifest changed since onboarding

```bash
iterate doctor            # TUI output; healthy exit 0, problems exit 1
iterate doctor --json     # structured JSON to stdout (script-friendly)
iterate doctor --json-out report.json   # write JSON report to a file (auto-creates dirs)
iterate doctor --fix      # apply safe, non-destructive fixes (auto timestamped backup), then re-run diagnostics
iterate doctor --list-checks            # list every available check name and exit
iterate doctor --check config.schema    # run only the named check(s); repeatable / comma-separated
```

`--fix` only does items that can be safely auto-fixed, and always creates a timestamped backup of `iterate.config.yaml` (`.doctorfix-<timestamp>` suffix) before fixing. Destructive/ambiguous fixes are never applied automatically — they're reported for you to handle manually. Currently auto-fixable: `dimensions` de-dupe/empty-restore-to-default, `language` invalid value reset to `en`, `max_rounds` non-integer removal / out-of-range clamp to `[1, 50]`, `git.target_branch` empty reset to `main`, `onboarding.skill_version` sync to installed version.

`--check <name>` runs only that check (the preamble a config-dependent check needs still runs silently, surfacing only its errors, so a blocker is always explained). It accepts the same `check` values reported in `findings[].check` under `--json` — e.g. `doctor --json | jq -r '.findings[].check'` to see a failing check's name, then `doctor --check <name>` to iterate on it quickly without re-running everything. `--list-checks` prints every name and exits.

### iterate scan (read-only tech-stack export)

`iterate scan` shows what the project scanner detected — the same detection that onboarding runs internally, but readable without walking the wizard. It reads **existence only** (manifests, top-level directory names, feature directories) and **never writes a file**, so it is safe on any project and from CI. It always exits `0`: a project that matches nothing recognisable is a normal outcome, not a failure.

```bash
iterate scan         # TUI report
iterate scan --json  # one JSON document on stdout
```

The report contains the detected `manifests`, `detected_languages`, `detected_package_managers` and `top_level_dirs`, the five feature flags (`has_specs` / `has_tests` / `has_ci` / `has_frontend` / `has_api`), and the suggestions the scanner derives from them: `suggested_dimensions`, `suggested_dimension_sets` (named scope blueprints for `dimension_sets`), `suggested_validation_commands` (a drop-in shape for `validation.commands`) and `suggested_command_whitelist` (for `validation.whitelist`). `has_api` also recognises the usual nested layouts (`src/api`, `app/routes`, `src/controllers`, …), not just top-level directories.

```json
{
  "project": "/path/to/project",
  "manifests": ["pyproject.toml"],
  "detected_languages": ["Python"],
  "detected_package_managers": ["pip/poetry"],
  "top_level_dirs": ["iterate_cli", "scripts", "tests"],
  "has_specs": false, "has_tests": true, "has_ci": true, "has_frontend": false,
  "has_api": false,
  "suggested_dimensions": ["correctness", "security", "..."],
  "suggested_dimension_sets": {"backend": {"dimensions": ["..."]}},
  "suggested_validation_commands": {"python": ["ruff check .", "mypy . --ignore-missing-imports", "pytest tests -x -q"]},
  "suggested_command_whitelist": ["python", "python3", "ruff", "mypy", "pytest"]
}
```

Apply a suggestion with `iterate init` (one command, no prompts), `iterate onboard` (interactive) or `iterate config set <key> <value>`.

### iterate init (prompt-free onboarding)

`iterate onboard` is interactive by design, which means CI jobs, shell scripts and other skills cannot drive it (they would block on the first prompt). `iterate init` runs the same scanner and the same generator with **no questions**, so initializing a repository is one command:

```bash
iterate init --yes                  # write ITERATE.md + iterate.config.yaml
iterate init --dry-run --json       # preview the detected stack + would-be config, write nothing
iterate init --yes --json           # one JSON document for scripts/agents
iterate init --yes --language zh --target-branch develop --goal "Harden the API"
```

The generated config uses the scanner's suggested dimensions, dimension sets (pruned to those dimensions), validation commands and command whitelist. It is the same shape the wizard writes, so `iterate doctor` accepts it and `iterate show` / `iterate refresh` work immediately.

Safety properties:

- **Idempotent** — if `iterate.config.yaml` already exists, `init` reports "already initialized" and changes nothing (exit `0`). Use `onboard`/`refresh` to modify a tuned project.
- **Never clobbers hand edits** — an existing `ITERATE.md` is only rewritten when it carries the USER-OWNED markers, and that section is preserved; otherwise `init` refuses and points at `reonboard`.
- **Non-interactive contract** — piped stdin requires `--yes` (exit `2` otherwise), and `--json` always leaves exactly one JSON document on stdout.

### iterate export / import (portable project state)

`iterate export` snapshots the project's iterate state — `iterate.config.yaml` plus `ITERATE.md` — into one versioned JSON bundle. The project itself is never modified; only the bundle file is written. This is useful for backups, moving a tuned profile to another machine, attaching the exact state to a review, or seeding the same profile in another repository.

```bash
iterate export                       # writes iterate-bundle-<UTC>.json in the project root
iterate export --out state.json      # choose the path (refuses to overwrite without --force)
iterate export --json > state.json   # print the bundle on stdout and write nothing
```

`iterate import` validates the bundle (including the config against the JSON schema) **before touching anything**, takes timestamped backups (`.import-<UTC>-<salt>`), and only then writes `iterate.config.yaml` / `ITERATE.md`:

```bash
iterate import state.json --dry-run   # preview added / changed / removed keys
iterate import state.json --yes       # apply (required when stdin is not a terminal)
cat state.json | iterate import - --yes
iterate import state.json --yes --reset-fingerprints  # bundle from a different repo
```

`--reset-fingerprints` drops the exporting project's recorded manifest fingerprints so they are not immediately reported as drift; `iterate refresh` re-records them for the current repository. An invalid or foreign bundle exits `1`, leaves the project unchanged, and — with `--json` — still prints exactly one JSON document. Usage errors (for example `--json` together with `--out`) exit `2`.

### iterate fingerprint (verify manifest drift)

`iterate fingerprint` (default action `verify`) compares the SHA-256 manifest fingerprints recorded at onboarding/refresh time against the current project root, detecting added / removed / changed tech-stack manifests — a non-blocking informational health check. It exits `0` when there is no drift (or drift checking is unavailable), and `1` when drift is detected, making it CI-friendly:

```bash
iterate fingerprint         # verify (default): TUI output
iterate fingerprint --json  # structured JSON: {"project": ..., "available": bool, "drift": bool, ...}
```

Fingerprints are (re)captured by `iterate onboard` / `iterate refresh` / `iterate reonboard`, and the same check runs silently inside `iterate status` and in the drift-prompt path of each `/iterate` invocation.

### iterate show (read-only merged config & personalization)

`iterate show` read-only displays the current merged project state — handy for quickly checking config and constraints, **writing no files**:

```bash
iterate show        # TUI output: onboarding metadata + effective config + personalization + drift status
iterate show --json # structured JSON to stdout (for scripts / CI / quick diff)
```

When you just want to confirm what restrictions are configured (forbidden areas, risk zones, known intent, dimension customization, fix order, notes, code conventions, extra validation commands), or check the merged `validation.commands` / whitelist, `iterate show` is clearer than reading `iterate.config.yaml` + `ITERATE.md` directly.

### iterate personalize --clear (clear personalization)

When you need to clear previously configured personalization constraints, do it in one shot after confirmation (structured rules removed from `iterate.config.yaml`, associated extra validation commands cleaned from `validation.commands`, personalization section in `ITERATE.md` user area removed, while keeping your hand-written content):

```bash
iterate personalize --clear       # with confirmation prompt
iterate personalize --clear --yes # skip confirmation
```

If there is no personalization content, it says "no personalization to clear" and exits normally (exit code 0).

### iterate config (non-interactive config get/set)

`iterate config` lets you inspect or change config values without launching the wizard — handy for scripts / CI / quick edits:

```bash
iterate config                 # TUI: list every settable key + current value
iterate config --json          # JSON object of all settable values (stdout stays clean for scripts)
iterate config get max_rounds  # print one resolved value; --json -> {"max_rounds": ...}
iterate config set language zh # validate + write one value (auto timestamped backup before write)
iterate config set reasoning_effort high --json  # confirm object {"key": ..., "value": ...}
iterate config schema                # emit the canonical JSON Schema for iterate.config.yaml (editor/CI tooling)
iterate config schema --out schema.json --force  # write it to a file (yaml-language-server / CI)
```

Supports flat keys (`goal`, `max_rounds`, `reasoning_effort`, `language`, `mode`, `dimensions`) and every nested key in its dotted form (`atomic.max_lines`, `atomic.max_adjacent_methods`, `git.target_branch`, `git.use_worktree`, `git.push_per_round`, `git.auto_merge`, `review.scope`, `reviewer.output_schema_validation`, `reviewer.evidence_validation`, `reviewer.coverage_validation`, `reviewer.scope_chunk_size`). `validation.commands` / `command_whitelist` and `invariants.*` are **not** settable here — edit them in `iterate.config.yaml` (or let `iterate onboard` write them) and re-check with `python scripts/validate.py config`. A corrupted config is never overwritten — `set` aborts with a clear error.

`iterate config schema` emits the canonical JSON Schema (the exact document `doctor` and `scripts/validate.py` validate against) as pure JSON on stdout, so an editor (`yaml-language-server` `yaml.schemas`), a CI validator, or any other tool enforces the same contract the CLI does. `--out PATH` writes it to a file (refuses to overwrite unless `--force`; confirmation goes to stderr so stdout stays clean), `--compact` emits single-line JSON, and it needs no `iterate.config.yaml` (the schema describes the CLI's config contract, not one project).

### iterate guard (defensive-mode pre/post-edit checks, v3.0)

Deterministic fail-loud checks the host AI runs around every coding step in defensive mode. Contract: exit code 0 = safe to proceed / change is safe; 1 = must fix or roll back.

- `iterate guard pre-check [paths...]` — runs **before editing**: targets exist, git worktree clean, manifest files ready, validation config safe, and each configured validation command's tool is on `PATH` (shell builtins like `true` are allowed) (`PASS`/`FAIL`).
- `iterate guard post-check [module...]` — runs **after each change**: executes exactly the configured `validation.commands.<module>` (the runtime's single authority whitelist — no composition, no prefixing).

Both support `--json` and `--dry-run` (preview exact commands without executing).

### iterate invariant (defensive-mode delivery gate, v3.0)

`iterate invariant` checks the project-level `invariants` declared in config (`invariants.ensure` file-existence assertions + `invariants.commands` exact per-module command lists). `ensure` entries must be **relative paths inside the project root** — absolute paths and `../` ancestors escaping the root are rejected outright. When no `invariants` section is configured it **degrades to `validation.commands`**, so old configs keep working unchanged. Exit 0 = invariants hold, 1 = violations found. Supports `--json` / `--dry-run`.

### iterate help (help & typo suggestions)

`iterate help` prints the command overview and `iterate help <command>` prints one command's detailed help — no need to remember where the `--help` flag goes:

```bash
iterate help          # same as `iterate --help`
iterate help doctor   # the `doctor` help text
```

A mistyped command is answered with the closest real one instead of a bare usage wall:

```text
$ iterate statu
iterate: error: argument command: invalid choice: 'statu' (choose from onboard, …, help)
did you mean 'status'? Run `iterate help` to list every command.
```

This also applies to subcommand actions (`iterate fingerprint verfy` → `did you mean 'verify'?`). Usage errors stay exit `2`, and with `--json` stdout still holds exactly one JSON document — the suggestion is carried in its `did_you_mean` field:

```bash
iterate statu --json
# {"error": "invalid usage", "hint": "run `iterate --help`", "did_you_mean": "status"}
```

When nothing is close enough, no guess is made (a wrong suggestion is worse than none) and the original diagnosis is left intact.

### iterate report (one document for PRs, issues and CI)

`status` / `scan` / `doctor` each answer one question. `iterate report` combines them into a single read-only document you can paste into a PR, attach to an issue, or upload as a CI artifact:

```bash
iterate report                          # GitHub-flavoured Markdown on stdout
iterate report --out report.md          # write it to a file (atomic; stdout stays empty)
iterate report --out report.md --force  # replace an existing report file
iterate report --json                   # one structured JSON document for scripts
iterate report --strict                 # warnings become blocking (exit 1), like doctor --strict
```

The Markdown contains the tech stack, effective review configuration (target branch, scope, dimensions, dimension sets, validation/whitelist, personalization count), every doctor check as a table, drift + advice, and concrete next commands. Values are pipe/newline/backtick/HTML escaped, so the document is safe to paste as-is. `--out` refuses to overwrite an existing file (and iterate's own state files) unless `--force` is given, so a stray report can never clobber your notes. Exit code is `0` when healthy, `1` when the report is blocking (errors, plus warnings under `--strict`) — drop it into CI with no extra parsing.

### iterate completion (shell tab-completion)

Completion is generated from the same argparse parser as `--help`, so it can never drift from the real command and option list:

```bash
iterate completion bash                # print the script
iterate completion bash --install      # write to the conventional user path
iterate completion zsh --install       # ~/.zfunc or ~/.oh-my-zsh/completions
iterate completion fish --install      # ~/.config/fish/completions/iterate.fish
iterate completion bash --install --dir ./completions --force  # explicit path
iterate completion bash --uninstall    # remove the installed file (idempotent)
source <(iterate completion bash)      # or source it directly
```

It completes subcommands, per-command flags (hidden options are excluded), fixed values such as `init --language zh|en`, directories for `-p/--project`, file arguments for `import` / `--out`, and command names after `iterate help`. `--install` picks the shell's conventional per-user file (honouring `XDG_DATA_HOME` / `XDG_CONFIG_HOME`), creates parent directories, refuses to replace an existing file without `--force`, and prints the reload/fpath hint; `--uninstall` removes exactly that file (never an arbitrary path) and is idempotent — a second run, or a run before ever installing, is still exit 0 and reports `removed: false`, so it is safe in teardown scripts. `--json` returns one `{shell, path, bytes, reload_hint}` document for `--install` and `{shell, path, removed, reload_hint}` for `--uninstall`.

### iterate refresh --diff (exact change preview)

`iterate refresh --dry-run` already answered "how many lines would change?", but a user deciding whether to apply a refresh had no way to see *what* would change — only a count. `--diff` closes that gap:

```bash
iterate refresh --diff            # print the exact unified diff refresh would apply
iterate refresh --diff --json     # one JSON doc with md_diff / config_diff strings
```

It computes the same would-be content as a real refresh and renders a unified diff (ITERATE.md rewrite plus the `iterate.config.yaml` rewrite), and **never writes a file** — a diff is a preview, so it implies dry-run. When nothing would change it reports "no changes needed" (exit 0); under `--json` the diff strings ride in `md_diff` / `config_diff` (empty when unchanged). The diff is reviewable before it happens — in a terminal, in a PR, or as JSON in CI.

### iterate template (bundled template surface)

The templates the skill consumes silently (the `ITERATE.md` skeleton, the AI onboarding playbook, the decision-log structure) were unreachable from the CLI — a user who wanted to know what structure `iterate onboard` produces, or to customise a copy of the skeleton, had to locate the file inside the installed skill directory by hand. `iterate template` makes that surface discoverable and read-only:

```bash
iterate template                     # list every bundled template
iterate template list --json         # structured metadata for each template
iterate template show ITERATE.template.md  # print one template verbatim
iterate template show playbook       # aliases: 'iterate', 'playbook', 'decisions'
```

It works from any directory (the templates belong to the skill, not one project), never writes, and a bad name is a usage error (exit 2) that names `iterate template list`.

---

## How It Works

### Onboarding (project knowledge base initialization)

Each `/iterate` invocation checks whether `ITERATE.md` exists in the project root. If not, onboarding is triggered through either channel:

- **AI Onboarding** — the AI auto-identifies the tech stack from directory structure / manifest files, producing `ITERATE.md` + `iterate.config.yaml`.
- **CLI Onboarding** — the CLI scans then lets you confirm/adjust the tech stack and config, producing the same output.

The scan only reads file/directory **existence** and a few public context files like README.md — it does not read `.env`, keys, credentials, or other sensitive file contents. Project-specific constraints can be added with `iterate personalize`.

`ITERATE.md` has two sections:

- `<!-- ITERATE:AI-MAINTAINED:START -->`: AI-maintained section, updated on refresh.
- `<!-- ITERATE:USER-OWNED:START -->`: user-owned section — your hand-written conventions, forbidden areas, risk zones; preserved on refresh.

### Drift detection

Each `/iterate` invocation recomputes SHA-256 fingerprints of manifest files such as `package.json`, `pyproject.toml`:

- No drift → silent pass
- Drift detected → prompt: continue / incremental refresh / full re-onboarding

### Personalization

An AI scan can discover the tech stack and directory structure, but not project-specific constraints. `iterate personalize` captures that knowledge:

- **Forbidden areas** — files/dirs iterate must not modify → `iterate.config.yaml`
- **Risk zones** — changes needing architecture approval → `iterate.config.yaml`
- **Known intent** — suppresses false positives → `iterate.config.yaml`
- **Dimension customization** — append focus to specific dimensions → `iterate.config.yaml`
- **Fix priority order** — per-dimension fix priority → `iterate.config.yaml`
- **Forbidden fix methods** — techniques that must not be used → `iterate.config.yaml`
- **Project conventions & notes** — lessons learned, known pitfalls → `ITERATE.md` user area
- **Extra validation commands** — project-specific validation commands → `iterate.config.yaml`

See [`config/iterate.config.yaml`](./config/iterate.config.yaml) for a complete example.

### Scope dimension sets & review routing

The top-level `dimensions` is the default for **whole-project / global** review. For **scope-specific** goals, the skill's dimension planning (SKILL.md Phase 0) routes to the right dimension scheme:

1. **Goal is empty or generic** (e.g. "improve code quality") → use the global `dimensions`. Zero friction.
2. **Goal names a scope that hits a preset `dimension_sets` set** (e.g. "review the frontend" → `frontend`) → use that set's `dimensions` + `focus` override directly, after a quick confirmation.
3. **Goal names an off-catalog scope** (no preset matches) → the AI **redefines dimensions from scratch**: it starts from the 9 canonical dimensions (not from global `dimensions` or any existing set, which would just be a lazy copy), picks the ones truly relevant to that scope, gives each **a scope-specific independent reason**, and may add temporary non-standard dimensions. This redefinition is recorded in `.iterate_decisions.md` under a dedicated `### Scope Dimension Redefinition (on-the-fly)` section, and is **validated by `scripts/validate.py decisions`** to ensure each reason isn't just a copy of the dimension's default focus prompt.

Preset sets live only in `iterate.config.yaml` (`dimension_sets`); `ITERATE.md` renders a one-time "Recommended Review Blueprints" listing. Ad-hoc redefinitions are bounded to `.iterate_decisions.md` per-round — they never balloon `ITERATE.md` or `iterate.config.yaml`, so the knowledge base stays small no matter how many iterations accumulate.

### Decision log (`.iterate_decisions.md`)

Every round's AI decisions — atomic fixes (direct), architectural fixes (approved + executed / deferred), reverted fixes, important AI decisions, validation results, and any off-catalog scope redefinitions — are recorded in `.iterate_decisions.md` (see the template in `templates/iterate-decisions.template.md`). This keeps the process auditable while keeping `ITERATE.md`'s AI-maintained section to a **single latest snapshot**.

### Core flow

```text
Step 0 — Onboarding Check
  └─ locate project root → check ITERATE.md → drift detection → (onboarding if missing)

Setup
  └─ extract goal → load config → read project context → create isolated branch/worktree

Loop (round = 1 .. max_rounds)
  ├─ Phase 1: N-dimension parallel review
  ├─ Phase 2: atomic issues auto-fixed
  ├─ Phase 3: architecture issues executed after user approval
  ├─ Phase 4: record round result
  └─ Phase 5: verify → merge (if auto_merge=true) → push (if push_per_round=true)

Summary
```

For the detailed flow, see [`SKILL.md`](./SKILL.md).

---

## Configuration

The default config lives in [`config/iterate.config.yaml`](./config/iterate.config.yaml). Project-level config recursively overrides same-name fields in the Master config.

Common config options (each entry: key — type, default, meaning):

- `goal` — string, default `"Improve code quality"` — iteration goal
- `max_rounds` — int, default `7` — max rounds (cap 50)
- `language` — string, default `"en"` — output language: `zh` / `en`
- `mode` — string, default `"iterate"` — default execution mode: `iterate` / `defensive` (v3.0)
- `reasoning_effort` — string?, default `null` — `low` / `medium` / `high`; `null` = follow provider default
- `dimensions` — list, default all 9 — enabled review dimensions (whole-project default)
- `dimension_sets` — object — named scope blueprints (`frontend`/`api`/`security`/…) with `dimensions` + optional `focus`
- `invariants` — object — `ensure` file-existence assertions + `commands` exact per-module lists (defensive-mode delivery gate)
- `review.scope` — string, default `"full"` — `full` / `changed-only`
- `atomic.max_lines` — int, default `20` — max lines for an atomic issue
- `atomic.max_adjacent_methods` — int, default `3` — max adjacent methods for an atomic issue
- `git.target_branch` — string, default `main` — merge target branch
- `git.use_worktree` — bool, default `false` — prefer a worktree for isolation
- `git.push_per_round` — bool, default `false` — push after each round passes
- `git.auto_merge` — bool, default `false` — auto-merge after verification
- `validation.command_whitelist` — list, default common prefixes — allowed command prefixes (config-time safety)
- `validation.commands` — object, default example — per-language validation commands (runtime's single authority whitelist)
- `reviewer.evidence_validation` — bool, default `true` — hard gate: every finding's file/line must exist on disk
- `reviewer.coverage_validation` — bool, default `true` — emit `COVERAGE_GAP` when a reviewer skipped assigned files
- `reviewer.scope_chunk_size` — int, default `25` — files per reviewer batch in a `full` scope review
- `onboarding.drift_check` — bool, default `true` — whether to check manifest drift

Example:

```yaml
goal: "improve code quality, ensure all functions are ≤80 lines and tests pass"
max_rounds: 7
language: en
mode: iterate          # or defensive

dimensions:
  - correctness
  - security
  - performance
  - architecture
  - style-tests
  - tech-debt
  - spec-compliance
  - frontend-backend
  - ui-ux

# Named scope blueprints: a scoped goal routes to its matching set instead
# of the global `dimensions`.
dimension_sets:
  frontend:
    dimensions:
      - ui-ux
      - frontend-backend
      - correctness
      - performance
    focus:
      ui-ux: "responsive layout, a11y, and state handling specific to views"
  security:
    dimensions:
      - security
      - correctness
    focus:
      security: "OWASP Top 10, authn/authz, injection, secret handling"

# Defensive-mode delivery gate: artifacts that must exist and commands that
# must pass at delivery (absent -> degrades to validation.commands).
invariants:
  ensure:
    - "README.md"
  commands:
    python:
      - "pytest tests/ -x -q"

validation:
  command_whitelist:
    - "ruff"
    - "mypy"
    - "pytest"
    - "swift"
    - "npm run"
  commands:
    python:
      - "ruff check src/"
      - "mypy src/ --ignore-missing-imports"
      - "pytest tests/ -x -q"
    swift:
      - "swift build -c debug"
    typescript:
      - "npm run compile"
```

> Commands in `validation.commands` **must** start with a prefix in `command_whitelist`, or they are rejected.

---

## FAQ

### Installation

**Q: The installer needs GitHub access; what if my network can't reach GitHub?**
A: The installer downloads and verifies from GitHub Release, so it needs GitHub access. If your network is restricted, use GitHub-independent alternatives:
- Manually copy [`SKILL.md`](./SKILL.md) to the assistant directory (see "Method B").
- CN mirror channels (ModelScope / SkillHub CN) are published and can provide the skill files.
- Download from a community mirror, then run `python scripts/install.py install` locally.

**Q: `npx iterate-skill-installer` reports a Python or Node version mismatch?**
A: The installer requires Node.js 18+ and Python 3.10+. Upgrade your system Python/Node, or make sure `python3` / `node` are on the PATH. The installer prefers `python3`, then falls back to `python`.

**Q: The installer puts the `iterate` CLI on my machine; can I avoid that?**
A: Yes. `npx iterate-skill-installer` also installs the `iterate` CLI (prefer `pipx`, else `pip install --user`) to run `iterate onboard`, etc. If you don't want automatic CLI install, use the "manually copy SKILL.md" or "source scripts" methods — copy skill files only.

**Q: I want to cancel mid-install; will it leave half-finished artifacts?**
A: No. The installer does download/verify/unpack in a temp dir and only writes into the assistant dir after the target is selected. Cancelling or failing won't overwrite an already-installed skill. If one exists, reinstall prompts to overwrite by default (needs `--force`).

### Usage

**Q: What is this Skill for, and what isn't it for?**
A: It's for **multi-round** code review and auto-fixing — e.g. paying down tech debt, eliminating lint/type/test issues over rounds, project-level refactoring. It's **not** for single simple changes (one line, add a comment) — use a normal conversation for those, no need for `/iterate`.

**Q: `iterate` mode vs `defensive` mode — which should I use?**
A: `/iterate` is for **reviewing/fixing existing code** until it converges. `/iterate defensive` is for when you want the AI to do **normal coding work** (add a feature, fix a bug, refactor, wire up an API, write tests): the host AI runs `guard pre-check` before editing, `guard post-check` after every change, and finishes with `invariant` plus the full review→fix→converge loop as a delivery gate. Want the AI to "build something correctly" → `defensive`; want it to "polish/review what's there to zero findings" → `iterate`.

**Q: Why does the first use appear to do nothing?**
A: Before your first `/iterate` or `iterate onboard`, the project has no `ITERATE.md` or `iterate.config.yaml`. On first use the skill does **onboarding first**: it tells you "this is the first use, initializing the project", scans the codebase to generate `ITERATE.md` and config, then iterates. If you see an init message instead of immediate review, that's normal. You can also run `iterate onboard` in the project root to init manually.

**Q: It feels stuck on a large project, no progress?**
A: The first round reviews multiple dimensions in parallel and can take a while. To reduce the "stuck" feeling, the skill now streams progress: `▶ Round N/max` at round start, per-dimension `⏳ reviewing …` during parallel review, and `✅ Round N complete` at round end. To speed it up:
- Set `review.scope` to `changed-only` in `iterate.config.yaml` to review only this round's changes.
- Split reviewer tasks by directory/module (see the Reviewer Prompt checklist in SKILL.md).
- Lower `max_rounds` to avoid unnecessary extra rounds.

**Q: What does the drift prompt mean at runtime?**
A: Drift detection compares SHA-256 fingerprints of manifest files like `package.json`, `pyproject.toml` (onboarding-time fingerprints vs the current project state). If deps or config changed, it means the project state differs from the last onboarding; you'll be prompted to: continue / incremental refresh (`iterate refresh`) / full re-onboarding (`iterate reonboard`). To check drift without triggering a run, use `iterate fingerprint` (exits 1 when drift is detected).

**Q: My changes weren't merged to main or pushed remotely?**
A: That's the **secure default**: `git.auto_merge` and `git.push_per_round` both default to `false`, so changes stay on an isolated `iterate/*` branch or worktree for you to review before deciding to merge/push. To auto-merge/push, enable those two options explicitly in `iterate.config.yaml`.

**Q: I edited `iterate.config.yaml` manually but some validation commands don't work?**
A: Commands in `validation.commands` **must** start with a prefix in `validation.command_whitelist`, or they're rejected. Extra validation commands added by personalization also only accept 30+ pre-approved tool prefixes and reject shell metacharacters like `;`, `|`, `&` — for safety, so the project config can't run arbitrary commands.

**Q: I want to add a new validation tool (e.g. `sphinx`), how?**
A: The strict whitelist only accepts pre-approved tool prefixes (so project config can't run arbitrary commands). Two **safe** ways to add a tool:
- **Operator-level environment variable (recommended, no source change)**: set `ITERATE_EXTRA_SAFE_COMMAND_PREFIXES=sphinx` in the runtime environment (comma/space-separated for multiple tools). This variable **can only be set at the system level**, not in the project config, so it doesn't break the security model; entries containing `;`, `|`, `&` are dropped (fail-closed).
- **Source-level extension**: append the tool name to `KNOWN_SAFE_COMMAND_PREFIXES` in `iterate_cli/personalize.py`, then reinstall.
- Or configure directly via `validation.command_whitelist` + `validation.commands` (must pass `python scripts/validate.py config`).

### Security

**Q: Does this Skill read my keys / `.env`?**
A: No. The skill and onboarding scan only read manifest existence and public context files like `README.md` / `CLAUDE.md`; it explicitly does not read `.env`, `*.key`, `secrets/`, `*.pem`, etc. `projectContext` also never contains API keys, passwords, or tokens.

**Q: Is updating safe?**
A: Yes. `scripts/install.py update` and `npx iterate-skill-installer` download the pre-uploaded `iterate-skill.tar.gz` + `SHA256SUMS.txt` from the GitHub Release and force SHA256 verification after download; install is rejected if missing or mismatched.

---

## Security

- **High autonomy**: this skill autonomously edits files, runs `git` operations, and runs commands in `validation.commands`. All changes first happen on an isolated branch/worktree; architecture fixes require user approval.
- **Secure-by-default Git**: `push_per_round` and `auto_merge` both default to `false`; merge/push are opt-in, so changes stay on the iteration branch unless explicitly enabled. Rollback uses non-destructive commands like `git restore`.
- **Two-layer command whitelist**:
  - Command prefixes are validated at config time.
  - Personalization `extra_validation_commands` only accept 30+ pre-approved tool prefixes and reject shell metacharacters like `;`, `|`, `&`; commands are re-validated on load/merge, so hand-edited config can't bypass the whitelist.
- **Sensitive files**: this skill and its installer never read `.env`, keys, credentials, etc.; onboarding scans only check the existence of public files like manifests.
- **Update security**: `scripts/install.py update` and `npx iterate-skill-installer` download the pre-uploaded `iterate-skill.tar.gz` + `SHA256SUMS.txt` from the GitHub Release and force SHA256 verification; rejected if missing or mismatched.
- **Installer disclosure**: `npx iterate-skill-installer` also installs the `iterate` CLI to PATH (prefer `pipx` isolated, else `--user`). If you don't want the CLI, use the manual-copy or source-script method.

---

## Directory Structure

```text
iterate-skill/
├── SKILL.md                          # core skill file
├── README.md                         # this file (English)
├── README.zh-CN.md                   # Chinese README
├── LICENSE                           # MIT license
├── CONTRIBUTING.md                   # contribution guide
├── CHANGELOG.md                      # version changelog
├── pyproject.toml                    # iterate CLI package definition
├── npm-installer/                    # npx one-command installer source
│   ├── bin/cli.js
│   ├── lib/installer.js
│   └── package.json
├── config/
│   ├── iterate.config.yaml           # default config (Master)
│   ├── config.schema.json            # config JSON Schema
│   ├── dimensions.yaml               # aggregated dimension definitions
│   └── dimensions/                   # data-driven dimension definitions
├── examples/                         # per-language project examples
├── harness/                          # two engineering components of the iterate ecosystem (monorepo)
│   ├── iterate-harness/              # standalone headless engine (npm: iterate-harness, command ih)
│   │   ├── src/iterate_harness/      #   CLI / engine / web / UI source
│   │   ├── frontend/                 #   terminal / web frontend UI
│   │   ├── npm/                      #   npm wrapper (ih)
│   │   └── scripts/                  #   install scripts and e2e tests
│   └── iterate-plugin/               # dsh desktop plugin (npm: iterate-plugin)
│       ├── src/                      #   server logic (TypeScript, compiled to dist/)
│       ├── lib/                      #   client UI injection entry
│       └── cordis.patch.yml          #   dsh bundle declaration
├── templates/
│   ├── ITERATE.template.md           # knowledge-base template
│   └── iterate-decisions.template.md # per-round decision log template
├── iterate_cli/                      # onboarding CLI source
│   ├── cli.py                        #   top-level command dispatcher
│   ├── guard.py                      #   guard pre/post-check (defensive mode)
│   ├── configcmd.py                  #   iterate config get/set
│   ├── dimension_sets.py             #   scope dimension-set suggestion / normalize / merge
│   ├── wizard.py / scan.py / generator.py / refresh.py / personalize.py /
│   │   doctor.py / show.py / fingerprint.py / tui.py
│   └── data/
│       ├── ITERATE.template.md       # wheel-packaged template
│       └── config.schema.json        # wheel-packaged schema (kept in sync)
├── scripts/
│   ├── install.py                    # install/uninstall/config/validate script
│   ├── validate.py                   # config & decision-log validation (incl. scope redefinition checks)
│   └── requirements.txt              # script dependencies
├── tools/                            # per-assistant implementation examples
├── tests/                            # unit tests
└── .github/workflows/                # CI / Release
```

---

## Contributing

Issues and PRs are welcome!

1. Fork this repo
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit: `git commit -m "feat: description"`
4. Push: `git push origin feat/your-feature`
5. Open a Pull Request

Please keep `SKILL.md` in its bilingual (English/Chinese) structure and add config examples for new features.

---

## Disclaimer

This project is provided "AS IS", without warranty of any kind, express or implied, including but not limited to warranties of merchantability, fitness for a particular purpose, and non-infringement.

**Automated code review and fixing carry inherent risks.** Changes made in normal mode are generated by AI models and may introduce defects, regressions, or unexpected behavior. Before merging changes, you should:

- Review every diff individually before applying to `main` or pushing.
- Ensure the project is under git version control and can be rolled back (`git restore`, revert, or restore from backup).
- Run your project's own tests and build checks after each round of fixes.
- Never run this project on keys, credentials, `.env`, or any files you're not allowed to modify; configure the corresponding protected paths in `iterate.config.yaml`'s `protected_paths`.

You are solely responsible for the code you produce, modify, or commit while using this project. By using this project you agree that the maintainers and contributors are not liable for any loss, damage, or legal consequences arising from your use of it.

---

## License

[MIT](./LICENSE) © 2026 iterate-skill contributors