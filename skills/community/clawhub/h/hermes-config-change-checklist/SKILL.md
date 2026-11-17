---
name: hermes-config-change-checklist
description: "Use when modifying, reviewing, or troubleshooting Hermes Agent configuration, providers, models, auxiliary routing, MCP servers, tools, skills, gateway/platform settings, cron jobs, secrets, or profiles. Standardizes pre-change discovery, safe edits, post-change verification, and restart guidance so a config change is provable rather than assumed. Use when a settings edit must be verified before it is called done."
version: 0.1.1
license: MIT-0
platforms: [linux, macos]
metadata:
  openclaw:
    tags: [hermes, configuration, verification, checklist]
  hermes:
    tags: [hermes, configuration, verification, provider, mcp, gateway, checklist]
    related_skills: [hermes-agent, hermes-agent-skill-authoring, mcp-server-integration]
---

# Hermes Config Change Checklist

**Overview (EN).** Turn any Hermes Agent configuration edit into a provable loop:
discover current state, make the narrowest safe change, verify with real commands,
report in a fixed four-section format, and state plainly whether the operator must
restart the gateway. Built for the failure mode where a config file looks right
but the subsystem was never exercised. Applies to providers, models, auxiliary
routing, MCP servers, tools, skills, gateway/platform settings, cron, and profiles.
The rest of this document is in Chinese.

## Overview

Use this skill for any Hermes Agent configuration change or health check. It turns ad-hoc edits into a repeatable loop:

1. discover current state,
2. make the narrowest safe change,
3. verify the result with real commands,
4. report what changed in a fixed format,
5. clearly state whether the operator must restart the gateway.

Important standing rule: **do not execute system-level gateway lifecycle or shutdown commands yourself.** Hand the exact command to the operator and say plainly that you did not run it. The gateway is usually the process serving your own conversation, so a lifecycle command issued from inside it kills the session mid-turn — and often leaves the change applied but unverified.

## When to Use

Use this skill when the user asks to:

- Add, remove, or change Hermes providers, models, model aliases, fallback models, delegation, or auxiliary routing.
- Edit `~/.hermes/config.yaml`, `~/.hermes/gateway-config.yaml`, the official Hermes env file (`hermes config env-path`), compatibility `.secrets` shims, profiles, tools, or skills.
- Configure or verify MCP servers.
- Configure Telegram/Weixin/gateway/platform behavior.
- Add or modify cron jobs, blueprints, webhooks, or plugins.
- Check whether a Hermes setting from OpenClaw/migration still needs work.
- Troubleshoot a Hermes feature not taking effect.

Do not use this skill for ordinary non-Hermes app configuration unless Hermes itself is involved.

## Safety Rules

- **No gateway lifecycle by the agent.** Never run gateway lifecycle, shutdown, reboot, or service-control commands. State the command and that the operator must run it.
- **No secret disclosure.** Do not print full API keys, OAuth tokens, passwords, cookies, or refresh tokens. Show only presence, source, length, or redacted prefix when necessary.
- **Prefer CLI setters.** Use `hermes config set KEY VALUE`, `hermes mcp add/test`, `hermes auth`, and `hermes tools` where possible instead of raw YAML edits.
- **Use profile-safe paths.** Default active profile uses `~/.hermes/`; do not edit another profile under `~/.hermes/profiles/<name>/` unless explicitly asked.
- **Back up risky rewrites.** For broad YAML rewrites, create or rely on `/snapshot`/config snapshot where appropriate before editing.
- **Report blockers honestly.** If a provider API or tool fails, do not invent success; capture the actual error and use an alternative if available.

## Standard Workflow

### 1. Scope the change

Identify exactly what will be affected:

| Target | Common files/commands |
|---|---|
| Main config | `~/.hermes/config.yaml`, `hermes config ...` |
| Gateway/platforms | `~/.hermes/gateway-config.yaml`, `hermes gateway status` |
| Providers/auth | `hermes auth list`, `hermes status --all`, env vars |
| MCP | `hermes mcp list`, `hermes mcp test NAME` |
| Tools/skills | `hermes tools list`, `hermes skills list` |
| Cron | `hermes cron list`, `cronjob` tool |

Completion criterion: every requested setting is mapped to a file, CLI command, or Hermes subsystem.

### 2. Discover current state first

Use read-only checks before editing. Typical commands:

```bash
hermes config path
hermes config check
hermes status --all
hermes auth list
```

For targeted checks:

```bash
hermes mcp list
hermes mcp test <name>
hermes tools list
hermes cron list
```

For YAML inspection, read the relevant file section without exposing secrets.

Completion criterion: you can state the current value/source and whether the requested change is additive, replacement, or cleanup.

### 3. Validate external prerequisites

Before writing config that depends on an API/provider, make a minimal live probe when possible:

- Provider key present and syntactically plausible.
- `/models`, `/key`, or provider equivalent works.
- One tiny chat/completions call works for the chosen model if safe.
- MCP server starts and exposes tools via `hermes mcp test`.
- Scripts referenced by config exist and are executable/readable.

Completion criterion: a real tool output confirms the dependency works, or the final report states the exact blocker.

### 4. Apply the narrowest change

Prefer command-based edits:

```bash
hermes config set section.key value
hermes mcp add <name> --command <cmd>
hermes mcp test <name>
```

Use `patch` / `write_file` only when CLI setters cannot express the change. Never use sed/awk for config edits.

Completion criterion: the command reports success or the file diff shows exactly the intended change.

### 5. Verify immediately

Run the smallest checks that prove the change is valid:

```bash
hermes config check
hermes status --all
```

Then run subsystem-specific checks:

| Change type | Verification |
|---|---|
| Provider/model | tiny model call or `hermes chat -q` where appropriate |
| Auxiliary model | import/use `agent.auxiliary_client.call_llm` or equivalent tiny call |
| MCP | `hermes mcp test NAME` |
| Gateway config | `hermes gateway status` and config syntax checks; do not restart |
| Cron | `hermes cron list` or `cronjob(action='list')` |
| Skill | `skill_view`, frontmatter validation, linked script syntax check |

Completion criterion: at least one post-change command verifies the changed subsystem, not just that the file exists.

### 6. State restart/apply boundary

State whether the change is live now or requires a fresh session/gateway restart:

| Change | Usually needs |
|---|---|
| Current chat model via `/model` | immediate/session-specific |
| `config.yaml` model/provider/auxiliary | new session or gateway restart |
| Tools enabled/disabled | `/reset` / new session |
| Skills added/removed | new session or `/reload-skills` when available |
| MCP config | `/reload-mcp` or gateway restart depending surface |
| Gateway platform config | operator-run `/restart` or the CLI lifecycle command |
| Env/secrets | reload/new process; often gateway restart |

Completion criterion: the final answer includes the exact user-run command if needed, while clearly saying the agent did not run it.

## Required Final Report Format

Use this structure after real changes. The four headings force the distinction between "I edited a file" and "the subsystem actually works":

```markdown
## 已完成
<one-sentence result>

## 改了什么
- <file/setting/command changed>
- <old → new when useful>

## 验证结果
- `<command>` → <success/failure summary>
- <provider/model/MCP health if relevant>

## 现在状态
- <live or pending restart>
- <what the operator should run, if any>
```

For checks that did not change anything, use:

```markdown
## 检查完成
## 发现
## 建议操作
```

## Quick Recipes

### Provider/API key change

1. Check provider appears in `hermes auth list` or env.
2. Probe key/model without printing secrets.
3. Write provider/model config.
4. Verify with a tiny model call.
5. State whether a gateway restart or new session is needed.

### Auxiliary model change

1. Inspect `auxiliary` section.
2. Test candidate models with `agent.auxiliary_client.call_llm` when possible.
3. Keep critical tasks (`compression`, `background_review`, `curator`) on stable models, not flaky free routers, unless the operator explicitly accepts that risk.
4. Write only the selected task slots.
5. Run `hermes config check` and report.

### MCP server change

1. Confirm command/script path exists and env vars are present.
2. Add/update MCP config.
3. Run `hermes mcp test NAME`.
4. Report tool count and errors.
5. State whether `/reload-mcp` or a restart is needed.

### Single skill change

1. Load `hermes-agent-skill-authoring` for standards and pitfalls.
2. Create/edit with Hermes skill frontmatter standards.
3. Add scripts under `scripts/`, references under `references/`.
4. Validate frontmatter and syntax-check scripts.
5. Use `skill_view` to confirm it loads.

### Batch skill library maintenance

For bulk operations — auditing, migrating from another ecosystem, standardizing frontmatter, fixing secrets, or batch-verifying 10+ skills — see the dedicated reference: `references/skill-library-maintenance.md`.

Key phases covered there:
- **Audit & categorize** — count, classify (keep/merge/delete), identify duplicates
- **Delete obsolete** — `skill_manage` with `absorbed_into`
- **Standardize** — frontmatter, path migration, `related_skills`, secrets
- **Fix secrets hygiene** — never use placeholder strings as run-time defaults; shell pattern with empty-string fallback and empty-string check
- **Verify** — bulk frontmatter validation, stale reference scan, script syntax checks, `hermes skills list` smoke test

## Common Pitfalls

1. **Skipping discovery.** Editing config without reading the current setting can overwrite working provider/profile choices.
2. **Trusting key presence as key validity.** A set env var can be a placeholder. Always make a minimal provider call when the task depends on validity.
3. **Restarting for the user.** Do not run lifecycle commands. Report that the operator must do it.
4. **Leaking secrets in logs.** Avoid `env`, full `auth.json`, or raw config dumps containing tokens.
5. **Declaring success after a file write only.** Success requires at least syntax/config validation and, where relevant, a live subsystem probe.
6. **Editing another profile accidentally.** Check active profile and path before writing profile-scoped files.
7. **Using free model routers for critical compression.** Free routers can return empty content, 429, or ignore instructions; keep critical summarization on stable models.
8. **Letting `model.api_key` shadow a custom provider credential.** A direct main-model key is selected as `model_config` before a custom provider's `key_env`; compare masked fingerprints and probe the exact regional endpoint with each credential before changing models. A key accepted by one regional endpoint can be rejected by another.

## Verification Checklist

- [ ] Relevant Hermes skill/docs consulted when needed.
- [ ] Active profile and target files identified.
- [ ] Current state inspected before edit.
- [ ] Secrets were not printed or persisted in unsafe places.
- [ ] External dependencies were live-tested when possible.
- [ ] Config change used `hermes config set` or a targeted patch/write.
- [ ] `hermes config check` or subsystem equivalent ran after change.
- [ ] Provider/MCP/skill/cron-specific verification ran when relevant.
- [ ] Final report used the four sections: 已完成 / 改了什么 / 验证结果 / 现在状态 (done / changed / verified / current state).
- [ ] Restart/apply boundary clearly stated; no forbidden restart executed.

## License and provenance

原创流程文档，无第三方代码，无个人环境信息。文中 `~/.hermes/` 为 Hermes 默认
路径，`<name>` 等为占位符。以 MIT-0 发布。
