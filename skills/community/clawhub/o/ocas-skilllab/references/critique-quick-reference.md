# Critique — Quick Reference

| Command | What it does |
|---------|-------------|
| `critique.assess <path>` | Score only, no changes |
| `critique.score <path>` | Alias for `.assess` |
| `critique.plan <path>` | Score + improvement plan |
| `critique.fix <path>` | Execute a plan |
| `critique.iterate <path>` | Fix-verify loop until 50/50 |
| `critique.run <path>` | Full pipeline |
| `critique.batch [paths]` | Assess multiple skills, ranked table |
| `critique.compare <path> <commit_a> <commit_b>` | Before/after comparison |
| `critique.10khr` | Autonomous library grinding |
| `critique.perfect <skill>` | Grind one skill to 50/50 |
| `critique.evolve <skill>` | Alias for `.perfect` |
| `critique.10khr --report-only` | Score all, no grinding |

## Submission-Gate Checks (Nous optional-skills catalog)

Before opening a PR for any OCAS skill, verify:

- **No `GENIE_*` / non-secret env-var config reads.** Behavioral settings must come from `config.yaml` under `skills.config.<key>` (see `nous-skill-requirements.md` → Configuration Policy). Run `ocas-forge/scripts/forge_audit_skills.py` — it flags violations.
- **Config documented as `skills.config.<key>`, not env-var names**, in the SKILL.md Configuration section.
- **Every behavioral setting declared** in `metadata.hermes.config`.
- Secrets only in `.env` (via `required_environment_variables`); `HERMES_HOME`/`HERMES_PROFILE` only locate the runtime.