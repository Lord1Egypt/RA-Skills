---
name: memory-consolidate
version: 1.0.0
description: >
  Persistent memory system for OpenClaw agents: reads session logs, extracts
  facts/decisions/solutions, manages temperature-based lifecycle, and generates
  MEMORY_SNAPSHOT.md injected into every session. ALWAYS use this skill when
  the user mentions: memory consolidation, 记忆整理, agent memory, MEMORY_SNAPSHOT,
  memory health, SNR, signal noise ratio, semantic pipeline, memory cron, session
  log extraction, facts not being saved, memory stale or missing, 内存优化,
  optimize agent memory, install memory, memory not working, memory consolidate
  报错, cron 怎么配 (when related to memory), 每天自动整理记忆, or any question
  about why the agent forgets things between sessions.
  Also activate when user says memory is stale, missing, or broken.
---

# memory-consolidate

Scripts live in the directory containing this SKILL.md. No copying needed.
`OPENCLAW_WORKSPACE` (default: `~/.openclaw/workspace`) tells scripts where to read/write.

## Install

Create required directories:

```bash
mkdir -p $OPENCLAW_WORKSPACE/memory/structured/{archive,candidates,semantic}
```

Patch OpenClaw config to inject snapshot into agent sessions:

```
gateway config.patch path="hooks.internal" raw='{"enabled":true,"entries":{"bootstrap-extra-files":{"enabled":true,"paths":["MEMORY_SNAPSHOT.md"]}}}'
```

Add daily cron (read timezone from USER.md, default UTC):

```
cron add job={
  "name": "Memory Consolidation (daily)",
  "schedule": {"kind": "cron", "expr": "0 3 * * *", "tz": "<tz_from_USER.md>"},
  "payload": {
    "kind": "agentTurn",
    "message": "bash $OPENCLAW_WORKSPACE/scripts/memory_consolidate_report.sh",
    "thinking": "off",
    "timeoutSeconds": 300
  },
  "sessionTarget": "isolated",
  "delivery": {"mode": "announce"}
}
```

Run initial consolidation and verify:

```bash
bash $OPENCLAW_WORKSPACE/scripts/memory_consolidate_report.sh
```

## Semantic Pipeline (LLM-powered)

`memory_consolidate_report.sh` runs the full pipeline including a semantic consolidation step powered by `claude-haiku-4-5-20251001` via the `tui` provider. This is auto-configured from `openclaw.json` — no manual API key setup needed. The LLM step clusters related memories, deduplicates, and improves signal quality in MEMORY_SNAPSHOT.md.

## Identity

Auto-detected from `IDENTITY.md` (assistant name) and `USER.md` (owner name, timezone, language). No config needed if these files exist with `- **Key:** Value` format.

## Config

Edit `config.yaml` in the directory containing this SKILL.md:

- `ingest.agent_ids` — which agents to scan (default: `"main"`, or `["main", "worker"]`)
- `ingest.session_hours` — lookback window (default: 24)
- `tag_rules` — project keyword → tag mapping
- `temperature.age_lambda` — decay speed (default: 0.07)

## Health check

```bash
python3 $OPENCLAW_WORKSPACE/scripts/memory_consolidate_observe.py
```

🟢 healthy / 🟡 watch / 🔴 needs tuning

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Snapshot shows "Assistant"/"User" | Ensure IDENTITY.md/USER.md have `**Name:**` format |
| LLM semantic step fails | Check `tui` provider config in `openclaw.json` has `baseUrl` and `apiKey` |
| Semantic pipeline degraded | Run `memory_candidate_extract.py`, check import errors |
| SNR too low | Increase `temperature.age_lambda` in config.yaml |
| No cold items after 2 weeks | Increase `age_lambda` (0.07 default should work) |
| Memory not updating | Verify `OPENCLAW_WORKSPACE` env var is set and cron job is active |
