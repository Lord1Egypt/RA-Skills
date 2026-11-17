# Submitting an OCAS skill to the Hermes optional-skills catalog

End-to-end recipe distilled from the genie PR (#50598) salvage. Use this when
packaging any `ocas-*` skill for `NousResearch/hermes-agent`.

## Hard gate: env-var-for-config

The hermes-sweeper auto-closes PRs that read non-secret behavioral config from
environment variables (GENIE_*, <NAME>_MAX_AGE_DAYS, <NAME>_PATH, <NAME>_ENABLED,
etc.). Fix BEFORE opening the PR:

1. Declare every behavioral setting in SKILL.md frontmatter under
   `metadata.hermes.config` with a logical key (`genie.snapshot_max_age_days`).
2. Read it at runtime from `config.yaml` under `skills.config.<key>` via PyYAML.
   Copy `templates/skill_config_resolver.py` into the skill's scripts/.
3. Document the `skills.config.<key>` keys in the SKILL.md Configuration
   section. Never write "set GENIE_X in your .env".
4. CLI flags (e.g. --dry-run) may override config.yaml.
5. Only secrets in .env; only HERMES_HOME / HERMES_PROFILE locate the runtime.

## Gotchas that actually bit us (encode these, don't relearn them)

- **Divergent copies.** A skill can live in several places that drift:
  the running script (`$HERMES_HOME/../<profile>/scripts/<x>.py`, invoked by
  cron via a wrapper .sh), the skill-bundled copy
  (`$HERMES_HOME/../<profile>/skills/ocas-<x>/scripts/<x>.py`), the PR tree
  (`optional-skills/.../scripts/<x>.py`), and possibly a `<fs-root>/<repo>/skills/`
  snapshot. Editing only one leaves the live behavior unchanged. Fix ALL
  relevant copies; verify the one the cron actually runs.
- **The sweeper won't reopen.** `gh pr reopen` fails on sweeper-closed PRs
  ("Could not open the pull request"). Either a maintainer reopens, or open a
  FRESH PR from the updated branch. Don't burn a turn retrying reopen.
- **HTTPS push fails for git, not gh.** `git push` to
  `https://github.com/<agent-handle>/<repo>.git` fails (no credential helper for
  git even though `gh` uses GH_TOKEN fine). Use SSH:
  `git remote set-url origin git@github.com:<agent-handle>/<repo>.git` then push.
  The SSH key is present and works.
- **Audit regex false positives.** When writing a scanner for env-var config
  reads, ALL-CAPS *_PATH (e.g. TOKEN_PATH, DEFAULT_DB_PATH) and snake_case config
  keys containing _DAYS / _AGE_DAYS (e.g. git_clone_max_age_days) are NOT
  violations. Only flag GENIE_* and ALL-CAPS <NAME>_(MAX_AGE_DAYS|DRY_RUN|
  TIER_LIMIT|ENABLED|...) style names. Skip *.bak files.
- **Don't break the running agent mid-fix.** The config-layer change is
  behavioral-source-only; cleanup logic (tiers, safety rules) is untouched.
  Verify with `python3 -m py_compile` + a real run (`--assess --json` shows the
  resolved config) + an end-to-end check that a config.yaml override is applied.

## Verify before pushing

- `python3 ocas-forge/scripts/forge_audit_skills.py` -> 0 blocking issues
  across all 31 ocas-* skills (it flags GENIE_*/env-var config reads + docs).
- `python3 -m pytest <skill>/tests/ -q` (if the skill ships tests).
- Grep the skill tree for `GENIE_` -> must be empty (except the audit tool's
  own pattern references).

## Push + PR

- Commit from the <agent-handle> fork (never directly to NousResearch).
- Open PR against `NousResearch/hermes-agent:main` with the
  `optional-skills/...` path. Description states capability, not implementation;
  <=60 char summary line; no marketing words.