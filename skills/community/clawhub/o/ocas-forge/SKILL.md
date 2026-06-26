---
name: ocas-forge
source: https://github.com/indigokarasu/forge
install: openclaw skill install https://github.com/indigokarasu/forge
description: Use when creating, building, reviewing, repairing, or validating Agent Skill packages. Runs a mandatory six-phase pipeline: existence gate, classify, scope, architecture, build, validate. Default output is the finished installable package. Trigger phrases: 'create a new skill', 'build a skill', 'design a skill', 'review this skill', 'repair this skill', 'validate skill package', 'update forge'. Do not use for skill evaluation or variant proposals (use Mentor).
metadata: {"openclaw":{"emoji":"🔨"}}
---

# Forge

Forge is the system's skill architect — given a capability idea or broken existing package, it runs a mandatory six-phase internal pipeline covering existence gate, classification, scoping, architecture, construction, and validation before writing a single file. The default output is the finished, installable package with all file contents written; Forge never returns design briefs or plans in place of the real artifact.


## When to use

- Create a new Agent Skill from a goal or capability description
- Review or critique an existing skill package
- Repair broken or defective skill packages
- Classify whether a proposed capability deserves to be a skill
- Validate a skill package against OCAS standards


## When not to use

- Evaluating skill performance — use Mentor
- Running or orchestrating skills — use Mentor
- Web research — use Sift
- Building non-skill artifacts


## Responsibility boundary

Forge owns skill design, construction, and validation.

Forge does not own: skill evaluation or variant testing (Mentor), behavioral pattern analysis (Corvus), behavioral refinement (Praxis), experimentation (Fellow).

Forge receives VariantProposal and VariantDecision files from Mentor. It builds variant packages and applies promotion decisions.


## Commands

- `forge.build` — design, scope, build, and validate a complete skill package
- `forge.critique` — review a package and identify defects
- `forge.repair` — fix broken files in an existing package
- `forge.classify` — classify a proposed skill (shortcut, workflow, system)
- `forge.validate` — run validation checks on a package
- `forge.scaffold` — generate a minimal package skeleton
- `forge.status` — current build state if multi-step build in progress
- `forge.journal` — write journal for the current run; called at end of every run
- `forge.update` — pull latest from GitHub source; preserves journals and data


## Mandatory design pipeline

Run all phases before writing files:

1. **Existence gate** — Is this better as a skill than a one-off prompt?
2. **Classify** — Shortcut, workflow, or system?
3. **Scope** — Exact job, explicit non-goals, smallest useful promise
4. **Architecture** — What goes in SKILL.md vs references vs scripts vs assets?
5. **Build** — Write all files
6. **Validate** — Routing, structural, usefulness checks


## Skill type classification

- **Shortcut** — narrow tool wrapper. 20-120 line SKILL.md.
- **Workflow** — multi-step process. 80-250 line SKILL.md.
- **System** — durable behavior system. 150-300 line SKILL.md, deeper material in references.


## Package rules

Minimum package: skill.json + SKILL.md. Add references/, scripts/, assets/ only when justified.

Read `references/authoring_rules.md` for full authoring standards.
Read `references/package_patterns.md` for package shape guidance by type.
Read `references/examples.md` for good and bad examples.


## Run completion

After every Forge command (build, critique, repair, validate):

1. Check `~/openclaw/data/ocas-forge/intake/` for VariantProposal and VariantDecision files from Mentor; process and move to `intake/processed/`
2. Persist build log entries and decisions to local JSONL files
3. Log material decisions to `decisions.jsonl`
4. Write journal via `forge.journal`

## Anti-patterns to reject

- Vague or overly broad scope
- Generic descriptions that don't route well
- SKILL.md bloated with background explanation
- Support folders created for aesthetics
- Plans returned instead of packages
- Template residue and placeholders
- Storage inside skill package directories
- Undocumented inter-skill interfaces


## Inter-skill interfaces

Forge receives intake files from Mentor at: `~/openclaw/data/ocas-forge/intake/`

File types received:
- `{proposal_id}.json` — VariantProposal (spec-ocas-shared-schemas.md)
- `{decision_id}.json` — VariantDecision (spec-ocas-shared-schemas.md)

After processing each file, move to `intake/processed/`.

See `spec-ocas-interfaces.md` for full handoff contracts.


## Storage layout

```
~/openclaw/data/ocas-forge/
  config.json
  build_log.jsonl
  decisions.jsonl
  intake/
    {proposal_id}.json
    {decision_id}.json
    processed/

~/openclaw/journals/ocas-forge/
  YYYY-MM-DD/
    {run_id}.json
```


Default config.json:
```json
{
  "skill_id": "ocas-forge",
  "skill_version": "2.3.0",
  "config_version": "1",
  "created_at": "",
  "updated_at": "",
  "validation": {
    "require_routing_tests": true,
    "require_structural_check": true,
    "require_usefulness_check": true
  },
  "retention": {
    "days": 0,
    "max_records": 10000
  }
}
```


## OKRs

Universal OKRs from spec-ocas-journal.md apply to all runs.

```yaml
skill_okrs:
  - name: build_completion_rate
    metric: fraction of forge.build invocations producing a complete package
    direction: maximize
    target: 0.95
    evaluation_window: 30_runs
  - name: validation_pass_rate
    metric: fraction of built packages passing all three validation checks
    direction: maximize
    target: 0.90
    evaluation_window: 30_runs
  - name: variant_build_success
    metric: fraction of VariantProposal intake files successfully built
    direction: maximize
    target: 0.90
    evaluation_window: 30_runs
```


## Optional skill cooperation

- Mentor — receives VariantProposal and VariantDecision files via intake directory
- Fellow — Forge may build experiment harnesses for Fellow benchmarks


## Journal outputs

Action Journal — every build, critique, repair, validation, and variant processing run.


## Initialization

On first invocation of any Forge command, run `forge.init`:

1. Create `~/openclaw/data/ocas-forge/` and subdirectories (`intake/`, `intake/processed/`)
2. Write default `config.json` with ConfigBase fields if absent
3. Create empty JSONL files: `build_log.jsonl`, `decisions.jsonl`
4. Create `~/openclaw/journals/ocas-forge/`
5. Register heartbeat entry `forge:intake` in `HEARTBEAT.md` if not already present
6. Register cron job `forge:update` if not already present (check `openclaw cron list` first)
7. Log initialization as a DecisionRecord in `decisions.jsonl`


## Background tasks

| Job name | Mechanism | Schedule | Command |
|---|---|---|---|
| `forge:intake` | heartbeat | every heartbeat pass | Check `~/openclaw/data/ocas-forge/intake/` for VariantProposal and VariantDecision files from Mentor; process and move to `intake/processed/` |
| `forge:update` | cron | `0 0 * * *` (midnight daily) | `forge.update` |

Heartbeat registration: append `forge:intake` entry to `~/.openclaw/workspace/HEARTBEAT.md` if not already present.

Registration during `forge.init`:
```
openclaw cron list
# If forge:update absent:
openclaw cron add --name forge:update --schedule "0 0 * * *" --command "forge.update" --sessionTarget isolated --lightContext true --timezone America/Los_Angeles
```


## Self-update

`forge.update` pulls the latest package from the `source:` URL in this file's frontmatter. Runs silently — no output unless the version changed or an error occurred.

1. Read `source:` from frontmatter → extract `{owner}/{repo}` from URL
2. Read local version from `skill.json`
3. Fetch remote version: `gh api "repos/{owner}/{repo}/contents/skill.json" --jq '.content' | base64 -d | python3 -c "import sys,json;print(json.load(sys.stdin)['version'])"`
4. If remote version equals local version → stop silently
5. Download and install:
   ```bash
   TMPDIR=$(mktemp -d)
   gh api "repos/{owner}/{repo}/tarball/main" > "$TMPDIR/archive.tar.gz"
   mkdir "$TMPDIR/extracted"
   tar xzf "$TMPDIR/archive.tar.gz" -C "$TMPDIR/extracted" --strip-components=1
   cp -R "$TMPDIR/extracted/"* ./
   rm -rf "$TMPDIR"
   ```
6. On failure → retry once. If second attempt fails, report the error and stop.
7. Output exactly: `I updated Forge from version {old} to {new}`


## Visibility

public


## Support file map

| File | When to read |
|---|---|
| `references/authoring_rules.md` | Before any build, critique, or validation |
| `references/package_patterns.md` | When deciding package shape by skill type |
| `references/examples.md` | When reviewing descriptions or detecting anti-patterns |
| `references/journal.md` | Before forge.journal; at end of every run |
