# Nous Research — Skill System Requirements

Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills

Key requirements from the official docs that skilllab should enforce during audit/critique.

## Frontmatter Requirements

### Required Fields
- `name` (1-64 chars, lowercase `[a-z0-9-]`, matches directory name)
- `description` (1-1024 chars, non-empty, includes trigger keywords)

### Hermes-Specific Metadata (`metadata.hermes`)
- `tags: [str]` — array of tag strings for `skills_list` grouping
- `category: str` — controls `skills_list` category grouping. Must be a recognized category
- `config: [{key, description, default}]` — **declares behavioral config keys** surfaced by `hermes config migrate/show`. Despite the historical "env var" wording in older docs, these keys are NOT environment variables. They are stored under `skills.config.<key>` in `config.yaml` and read by the skill at runtime (see Configuration Policy below).
- `fallback_for_toolsets: [str]` — conditional activation (show when toolset unavailable)
- `requires_toolsets: [str]` — conditional activation (show when toolset available)
- `fallback_for_tools: [str]` — same, for individual tools
- `requires_tools: [str]` — same, for individual tools

### Configuration Policy (MANDATORY — enforced at submission)

**Behavioral settings (thresholds, retention windows, feature flags, display prefs, paths) MUST NOT be read from environment variables.** This is the standing `env-var-for-config` policy in the Hermes `AGENTS.md` Contribution Rubric. The hermes-sweeper auto-closes PRs that tell users to "set `X` in your `.env`" or read non-secret config from `GENIE_*`/`HERMES_*`-style env vars.

Correct mechanism (the standard all OCAS skills must follow):

1. **Declare** each behavioral setting in frontmatter under `metadata.hermes.config` with a logical key (e.g. `genie.snapshot_max_age_days`). The storage key becomes `skills.config.genie.snapshot_max_age_days`.
2. **Read** values at runtime from `$HERMES_HOME/config.yaml` under `skills.config.<key>`, falling back to the declared default when unset. Use PyYAML (Hermes already ships it). The shipped `telephony.py` optional-skill is the reference implementation.
3. **Document** the `skills.config.<key>` keys in the SKILL.md Configuration section. Never document env-var names (`GENIE_*`, etc.) as the user-facing control.
4. **Override** via CLI flags where a runtime override is useful (e.g. `--dry-run`), which take precedence over config.yaml.
5. **Environment variables are only acceptable for:** (a) secrets/credentials (and those go in `.env`, declared via `required_environment_variables`), or (b) locating the runtime (`HERMES_HOME`, `HERMES_PROFILE`) — never for behavioral tuning.

Anti-pattern (rejects the PR):
```python
# WRONG — sweeper closes this
threshold = int(os.environ.get("GENIE_SNAPSHOT_MAX_AGE_DAYS", 7))
```
Correct pattern:
```python
# RIGHT — reads config.yaml, falls back to default
def _skill_config(key, default):
    node = _load_root_config()  # yaml.safe_load($HERMES_HOME/config.yaml)
    for part in ("skills", "config", "genie", key):
        node = node.get(part) if isinstance(node, dict) else None
        if node is None:
            return default
    return node
threshold = _skill_config("snapshot_max_age_days", 7)
```

> Note: OCAS skills historically used `GENIE_*` env vars (genie, and others that predate this policy). Before submitting any OCAS skill to the optional-skills catalog, migrate its config layer to the `skills.config.*` mechanism above. The forge audit (`forge_audit_skills.py`) and skilllab critique flag any remaining `GENIE_*`/`*_MAX_AGE_DAYS`-style env reads.


### Optional Fields
- `platforms: [macos | linux | windows]` — OS restriction. Omit = all platforms
- `required_environment_variables:` — formal declaration for secure setup prompts
- `source:` — URL for skills synced from external repos
- `triggers:` — trigger phrases (enables slash command discovery)

### Anti-Patterns
- `category:` at top level → silently ignored, must be `metadata.hermes.category`
- `tags:` only at top level → works but misses Hermes grouping
- Env vars only in body table, not in `metadata.hermes.config` → D1-4 deduction
- `tools:` instead of `allowed-tools:` → silently ignored
- Name with spaces/uppercase → may fail matching
- Name doesn't match directory → activation mismatch

## Directory Structure

```
~/.hermes/skills/<name>/
├── SKILL.md          # Required — main instructions
├── references/       # Additional docs (loaded on demand)
├── templates/        # Output formats
├── scripts/          # Helper scripts
└── assets/           # Supplementary files
```

- No ad-hoc subdirectories
- `includes:` should list `references/**` and `scripts/**` if those directories exist
- Reference files over 100 lines should have a table of contents
- File references one level deep from SKILL.md (A→B→C chains are a D4 failure)

## Progressive Disclosure (Three-Layer Architecture)

- **Layer 1:** Metadata (~100 tokens) — always in context at catalog scan
- **Layer 2:** SKILL.md (<5k tokens) — loaded on skill activation
- **Layer 3:** References (unloaded) — on-demand, per-file, only when relevant

SKILL.md body should be under 500 lines, ideally under 5000 tokens.

## Support File Maps

Must use a "When to read" column with conditional language:
- "Before [action]" — e.g., "Before running genie.py"
- "During [phase]" — e.g., "During Phase 2 discovery"
- "When [condition]" — e.g., "When bot detection blocks access"
- "If [situation]" — e.g., "If VPN is blocked"

Static topic descriptions (e.g., "API error reference") are a D8-3 deduction.

## Skill Bundles

Bundles are YAML files at `~/.hermes/skill-bundles/<slug>.yaml`:
```yaml
name: backend-dev
description: Backend feature work
skills:
  - github-code-review
  - test-driven-development
instruction: |
  Always start by writing failing tests.
```

Fields: `name`, `description`, `skills` (required), `instruction` (optional).

## Conditional Activation

Skills can auto-show/hide based on tool availability:
- `fallback_for_toolsets: [web]` — shown when web toolset is unavailable
- `requires_toolsets: [terminal]` — shown when terminal toolset is available

## Platform-Specific Skills

```yaml
platforms: [macos]        # macOS only
platforms: [macos, linux] # macOS and Linux
```

When set, skill is hidden from `skills_list()` and slash commands on incompatible platforms.

## Secure Setup on Load

Skills can declare required env vars for secure prompting:
```yaml
required_environment_variables:
  - name: TENOR_API_KEY
    prompt: Tenor API key
    help: Get a key from https://developers.google.com/tenor
    required_for: full functionality
```

## Publishing (agentskills.io)

- agentskills.io discovers skills from GitHub repos (no submission API)
- Remove non-standard Hermes extensions before publishing: `metadata.hermes`, `metadata.email` → `metadata.author`, `metadata.openclaw` (legacy), top-level `version` → `metadata.version`
- Required: `name` and `description` in frontmatter