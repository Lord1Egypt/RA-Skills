# OCAS Skill Compliance Audit Checklist

## Purpose

Use this checklist when auditing an existing OCAS skill package for architecture compliance. This is the standard gate before publishing or syncing a skill to GitHub.

## File Inventory

Every OCAS skill package must contain these files:

| File | Required | Purpose |
|---|---|---|
| `SKILL.md` | Yes | Operational frontmatter + skill body |
| `README.md` | Yes | Human-readable overview |
| `CHANGELOG.md` | Yes | Version history |
| `skill.json` | Yes | Machine-readable metadata + self-update config |
| `.gitignore` | Yes | Exclude artifacts from git |
| `evals.json` | Yes | Evaluation test cases |

Optional (add only when justified):
- `references/*.md` — session-specific detail, schemas, domain knowledge
- `scripts/*.py/*.sh` — deterministic actions the skill invokes
- `templates/*` — starter files meant to be copied and modified
- `assets/*` — reusable operational artifacts
- `evals/evals.json` — duplicate of root evals.json for package discoverability

## Frontmatter Checklist

SKILL.md YAML frontmatter must include:

- [ ] `name` — hyphenated skill identifier
- [ ] `description` — routing logic with trigger phrases, includes "Not for" exclusions
- [ ] `license` — `MIT` for OCAS skills
- [ ] `metadata.author` — `<agent-name>`
- [ ] `metadata.email` — `<agent-email>`
- [ ] `metadata.version` — semver string (e.g. `"1.1.0"`)
- [ ] `metadata.tags` — list of lowercase tags
- [ ] `metadata.category` — skill category (`ocas`, `infrastructure`, `workflow`, etc.)

## Required SKILL.md Sections

### All Skills

1. **Title** — `# Skill Name — Short Description`
2. **When to use** — concrete trigger conditions
3. **When NOT to use** — explicit exclusions with pointers to other skills
4. **Responsibility Boundary** — what this skill owns, what it does NOT own
5. **Main content** — workflow, commands, configuration
6. **Ontology Types** — declare entity extraction + Signal emission behavior (or explicitly state "does not extract entities / does not emit Signals")
7. **Journal Outputs** — which journal type(s) emitted (Observation, Action, Research), file path pattern
8. **Storage Layout** — `{agent_root}/commons/data/{skill-id}/` and `{agent_root}/commons/journals/{skill-id}/` paths
9. **OKRs** — at least one objective with key results and targets
10. **Background Tasks** — cron jobs and heartbeat entries (omit entirely if purely reactive)
11. **Pitfalls** — known issues, edge cases, gotchas
12. **Support File Map** — table of all `references/` files with one-line descriptions

### System Skills (additional)

13. **Commands** — list of invocable commands
14. **Initialization** — first-run setup steps (create directories, write empty files, register jobs)
15. **Self-update** — `self.update` procedure from GitHub source
16. **Optional Skill Cooperation** — other skills this cooperates with

## skill.json Checklist

```json
{
  "name": "ocas-{skill}",
  "version": "X.Y.Z",
  "description": "...",
  "author": "<agent-name>",
  "email": "<agent-email>",
  "skill_type": "shortcut|workflow|system",
  "filesystem": {
    "read": ["{agent_root}/commons/data/{skill-id}/"],
    "write": ["{agent_root}/commons/data/{skill-id}/"]
  },
  "self_update": {
    "source": "https://github.com/<agent-handle>/{repo}",
    "mechanism": "version-checked tarball from GitHub via gh CLI",
    "command": "{skill}.update",
    "requires_binaries": ["gh", "tar", "..."]
  }
}
```

## README.md Checklist

- [ ] Title matching skill name
- [ ] One-line description
- [ ] Overview paragraph
- [ ] Commands list
- [ ] Dependencies
- [ ] Scheduled tasks (if any)
- [ ] Link to CHANGELOG.md

## CHANGELOG.md Checklist

- [ ] Follows semver
- [ ] Dated entries (ISO 8601)
- [ ] Grouped by version: `### Added`, `### Changed`, `### Fixed`, `### Removed`
- [ ] Newest first

## .gitignore Checklist

Exclude at minimum:
- Language artifacts: `__pycache__/`, `*.pyc`, `*.pyo`, `*.pyd`, `*.so`
- Environment: `.env`, `.env.local`, `venv/`, `.venv/`
- OS: `.DS_Store`
- Logs: `*.log`, `*.tmp`

## SKILL.md Body Guidelines (authoring_rules.md Section 8)

- Shortcut skills: 20-120 lines
- Workflow skills: 80-250 lines
- System skills: 150-300 lines
- Code ratio under 15% (fenced-block lines ÷ total lines)
- Under 500 lines absolute maximum
- Extract SQL DDL, Python examples, JSON schemas, default configs, OKR YAML, cron bash, self-update bash into `references/` files
- Replace extracted blocks with one-line pointers

## Required SKILL.md Sections for System Skills (authoring_rules.md end)

System skills must explicitly include:
1. Responsibility boundary
2. Ontology types
3. Commands
4. Domain-specific workflow sections
5. Optional skill cooperation
6. Journal outputs
7. Storage layout (point to `references/config-default.json` for config structure)
8. OKRs
9. Initialization
10. Background tasks (omit if purely reactive)
11. Support file map
12. Self-update command

## Configuration Policy (MANDATORY — blocks submission to Nous optional-skills catalog)

Behavioral settings (thresholds, retention windows, feature flags, display prefs, paths) **MUST NOT** be read from environment variables. This is the standing `env-var-for-config` policy; the hermes-sweeper auto-closes violating PRs.

- [ ] Every behavioral setting is declared in `metadata.hermes.config` with a logical key
- [ ] Skill scripts read values from `$HERMES_HOME/config.yaml` under `skills.config.<key>` (via PyYAML), never `os.environ.get("GENIE_*" / "<NAME>_*")`
- [ ] SKILL.md Configuration section documents `skills.config.<key>` keys, not env-var names
- [ ] CLI flags (e.g. `--dry-run`) override config.yaml where a runtime override is useful
- [ ] Only secrets go in `.env` (declared via `required_environment_variables`); only `HERMES_HOME`/`HERMES_PROFILE` locate the runtime
- [ ] No `GENIE_*`, `*_MAX_AGE_DAYS`, `*_PATH`, `*_ENABLED` (non-secret) env-var reads remain in `scripts/`

**Reference implementation:** the shipped `telephony.py` optional-skill (reads `config.yaml`). OCAS skills that predate this policy (e.g. genie) must be migrated before submission. The automated audit (`forge_audit_skills.py`) flags violations.

## Single Source of Truth (MANDATORY)

An OCAS skill must have exactly ONE canonical copy of each artifact (script + SKILL.md). Divergent copies are a recurring, silent failure mode: a cron `script:` field or a wrapper `.sh` may invoke a *different* file than the skill-bundled one, so the version you test and submit is never the one that actually runs.

Observed incident (ocas-genie, 2026-07): the cron `prompt` was repointed to the skill-bundled script, but the job's actual `script:` was `rr_genie.sh`, which still `exec`-ed the *old, deleted* `profiles/<profile>/scripts/genie.py`. The job would have failed at runtime despite the `prompt` text showing the correct path. Caught only by reading the wrapper end-to-end.

Audit checklist:
- [ ] Exactly one version of each `scripts/*.py` is the runtime source. If a legacy copy also lives under `profiles/<profile>/scripts/`, the cron `script:`/wrapper MUST point at the skill-bundled copy, not the legacy path.
- [ ] The cron job's `prompt` AND its `script:`/wrapper agree on the same path (the `prompt` is NOT authoritative for what executes — read the wrapper).
- [ ] The PR-tree / submission copy is the same bytes as the live profile copy (or generated from it). Diff them before pushing.
- [ ] No `.bak` / `removed-*` / timestamped duplicate scripts linger in `scripts/` — delete after confirming the canonical copy works.
- [ ] When merging two divergent copies, take the UNION of real fixes (e.g. one copy had correct config reads, the other had a bug-fix block). Neither "newest mtime" copy is automatically fully ahead.

## GitHub Sync Checklist

- [ ] `gh repo create <agent-handle>/{repo} --private --description "..."`
- [ ] `git init` (if no repo) or verify existing remote
- [ ] `git remote add origin https://github.com/<agent-handle>/{repo}.git`
- [ ] `git add -A && git commit -m "..."` with conventional commit message
- [ ] `git branch -m main && git push -u origin main`
- [ ] Verify: `gh repo view <agent-handle>/{repo} --json visibility` → `PRIVATE`

## Audit Workflow

1. Read SKILL.md — check frontmatter + all required sections
2. Check file inventory — all required files present
3. Check references — every file in `references/` is referenced from SKILL.md
4. Check skill.json — valid JSON, ConfigBase fields, self_update configured
5. Check .gitignore — minimum excludes present
6. Check evals.json — at least 2 eval cases with expected skills_loaded
7. Apply fixes (add missing files, sections, metadata)
8. Create GitHub repo if needed, push
9. Verify push succeeded and repo is private