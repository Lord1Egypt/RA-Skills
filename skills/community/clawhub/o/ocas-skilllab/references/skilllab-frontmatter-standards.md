# Skilllab Frontmatter Standards

Minimum for authored skills:

```yaml
---
name: <skill-name>
license: MIT
description: >
  What it does. What triggers it. What it does NOT do.
metadata:
  author: Indigo Karasu (indigokarasu)
  version: "3.2.0"
  hermes:
    tags: [tag1, tag2]
    category: <category>
includes:
  - references/**
  - scripts/**
triggers:
  - trigger-phrase-1
  - trigger-phrase-2
---
```

**Required fields:** `name`, `description`

**Hermes-specific fields (always include for agent-authored skills):**
- `metadata.hermes.tags` — array of tag strings for `skills_list` grouping
- `metadata.hermes.category` — string controlling category grouping. Use existing categories: `infrastructure`, `devops`, `productivity`, `creative`, `management`, `software-development`, `mcp`, `media`, `browser-vision`, `frontend-design`, `concept-diagrams`, `csv-parsing`, `database-operations`, `docker-management`, `email-sending`, `json-formatting`, `unit-testing`, `test-driven-development`, `requesting-code-review`, `writing-plans`, `subagent-driven-development`, `simplify-code`, `debugging-hermes-tui-commands`, `hermes-s6-container-supervision`, `ocas-10xeng`, `ocas-10xeng-audit`, `ocas-10xeng-autofix`, `ocas-10xeng-debt`, `ocas-10xeng-help`, `ocas-10xeng-review`, `learn`, `triage`, `grill-me`, `grill-with-docs`, `humanizer`, `minimalist-ui`, `paper-figure`, `prava-pay`, `restaurant-rater`, `shadcn`, `trello`, `util-buy`, `util-draw`, `util-dreamhost`, `util-github`, `util-headhunter`, `util-iamwrite`, `util-rapidapi`, `util-reddit`, `util-telegram-miniapp`, `util-voice-call`, `util-vpn`, `util-web-extract`, `util-wiki`, `vision-analyze`, `web-artifacts-builder`, `web-design-guidelines`, `write-a-skill`, `agent-profile-creator`, `backup-merge-lessons-2026-06`, `captcha-challenge-bypass`, `dashboard-plugin-ui`, `design-references`, `gcloud-cli`, `hermes-dashboard-plugins`, `indigo-list-monitor`, `memory-system-design`, `plugin-diagnostics`, `util-agent-swarm`, `util-cron-monitor`, `util-hermes-ops`, `util-manage`, `util-mask`, `util-vps-cleanup`, `util-warmhands`, `util-web-deployment`, `ocas-autobio`, `ocas-bones`, `ocas-bower`, `ocas-custodian`, `ocas-dispatch`, `ocas-fellow`, `ocas-finch`, `ocas-forge`, `ocas-genie`, `ocas-haiku`, `ocas-imagine`, `ocas-inception`, `ocas-look`, `ocas-lucid`, `ocas-mentor`, `ocas-multipass`, `ocas-praxis`, `ocas-rally`, `ocas-reach`, `ocas-sands`, `ocas-scout`, `ocas-sift`, `ocas-skilllab`, `ocas-spot`, `ocas-styx`, `ocas-tasks`, `ocas-taste`, `ocas-vesper`, `ocas-vibes`, `ocas-voyage`, `ocas-weave`
- `metadata.hermes.config` — declare the skill's **behavioral config keys** here. These are NOT environment variables: they live under `skills.config.<key>` in `config.yaml` and are read by the skill at runtime (never from `GENIE_*`/non-secret env vars — see `nous-skill-requirements.md` Configuration Policy). Secrets go in `.env` via `required_environment_variables` instead.
  ```yaml
  metadata:
    hermes:
      config:
        - key: my.skill.retention_days
          description: "Days before cleanup"
          default: "7"
        - key: my.skill.dry_run
          description: "If true, report only"
          default: "false"
  ```

**Optional fields:**
- `warning: 'FALSE TRIGGER RISK: Has had X% false trigger rate. [Specific guidance].'` — Anti-false-trigger warning placed in frontmatter so it's visible BEFORE the agent loads the full SKILL.md. More effective than burying warnings in the body (a warning at line 178 of 214 didn't prevent 67% FT rate for ocas-vibes). Use for skills with documented false trigger rates >25%.
- `platforms: [macos, linux]` — OS restriction
- `metadata.hermes.fallback_for_toolsets: [web]` — conditional activation
- `metadata.hermes.requires_toolsets: [terminal]` — conditional activation
- `required_environment_variables:` — formal env var declaration for secure setup
- `source:` — URL for skills synced from external repos

**Anti-patterns:**
- `category:` at top level (ignored by Hermes — must be `metadata.hermes.category`)
- `tags:` only at top level without `metadata.hermes.tags` (works but misses Hermes grouping)
- Env vars only in body table, not in `metadata.hermes.config`