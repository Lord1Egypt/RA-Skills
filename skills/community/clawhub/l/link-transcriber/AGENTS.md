# AGENTS

## Project Snapshot

This repository is the public distribution repo for the `link-transcriber` skill.

Current purpose:

- distribute a Codex-compatible public skill
- support Douyin and Xiaohongshu link understanding and execution planning
- call the live `linkTranscriber` API
- rely on the publisher-operated hosted service for required platform access
- return a concise summary, a todo list, and a recommended reminder time to the end user

This repo is intentionally small and should stay focused on the skill distribution surface only.

## Invocation Guardrails

- For current product behavior, use this repo's `SKILL.md` as the stable contract.
- Do not use `web/skill/` as the current source of truth; it is legacy migration reference only.
- Default to `https://linktranscriber.store` for public use.
- If the hosted service reports missing platform configuration, treat it as a server-side issue rather than asking the end user for credentials by default.
- Poll until a true final state arrives. For the stable public contract, in-progress states are `queued` and `running`.

## Current Status

What is already done:

- `SKILL.md` is valid and installed locally in Codex
- `agents/openai.yaml` exists and matches the current skill behavior
- `scripts/call_service_example.py` supports:
  - infer platform from URL
  - create transcription task
  - poll transcription task
  - print final `summary_markdown` as the base material used by the skill layer
- `scripts/check_service_health.py` is the preferred hosted-service health check path for this repo
- API base URL is intentionally configurable:
  - default public origin: `https://linktranscriber.store`
  - set `LINK_SKILL_API_BASE_URL` only when an override is required
  - avoid raw IPs and plain HTTP in public copy
- Required platform access is expected to be managed on the hosted service side for production use
- real API smoke has already succeeded against Xiaohongshu
ClawHub status:

- CLI login is valid
- publish succeeded on `2026-04-01`
- canonical slug should match the skill name for new installs
- published version:
  - keep in sync with the latest ClawHub release
- published slug:
  - `link-transcriber`
- published page:
  - `https://clawhub.ai/bobobo2026/link-transcriber`
## Source Of Truth

Behavior source of truth:

- [SKILL.md](/Users/yibo/Documents/company/IdeaProjects/KnowledgeOS/skill/SKILL.md)

Codex UI metadata source of truth:

- [agents/openai.yaml](/Users/yibo/Documents/company/IdeaProjects/KnowledgeOS/skill/agents/openai.yaml)

Public repo overview:

- [README.md](/Users/yibo/Documents/company/IdeaProjects/KnowledgeOS/skill/README.md)

ClawHub-oriented copy:

- [CLAWHUB.md](/Users/yibo/Documents/company/IdeaProjects/KnowledgeOS/skill/CLAWHUB.md)

Smoke / example runner:

- [scripts/check_service_health.py](/Users/yibo/Documents/company/IdeaProjects/KnowledgeOS/skill/scripts/check_service_health.py)
- [scripts/call_service_example.py](/Users/yibo/Documents/company/IdeaProjects/KnowledgeOS/skill/scripts/call_service_example.py)
- [scripts/update_local_skill.sh](/Users/yibo/Documents/company/IdeaProjects/KnowledgeOS/skill/scripts/update_local_skill.sh)

## Key Product Behavior

Supported platforms:

- `douyin`
- `xiaohongshu`

Not supported in this repo’s current public skill positioning:

- YouTube
- raw transcription JSON as the default user-facing result

End-user behavior:

1. user provides a link
2. skill relies on the publisher-operated hosted service for required platform access
3. skill infers platform when possible
4. skill creates transcription task
5. skill polls until transcription finishes
6. public result returns `summary_markdown`
7. skill turns `summary_markdown` into:
   - a concise summary
   - a todo list
   - a recommended reminder time
8. if the user confirms a reminder time, OpenClaw creates a main-session cron reminder

## Live API Details

Public API base URL:

- default: `https://linktranscriber.store`
- override with `LINK_SKILL_API_BASE_URL` when needed

Health check:

- `GET /health`

Public transcription create:

- `POST /public/transcriptions`

Public transcription lookup:

- `GET /public/transcriptions/{task_id}`

Internal `api/service/*` endpoints may still exist upstream, but they are no longer the public skill contract.

## Validation Commands

Validate skill structure:

```bash
python3 /Users/yibo/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  /Users/yibo/Documents/company/IdeaProjects/KnowledgeOS/skill
```

Compile script:

```bash
python3 -m compileall /Users/yibo/Documents/company/IdeaProjects/KnowledgeOS/skill/scripts
```

Check hosted service health:

```bash
python3 /Users/yibo/Documents/company/IdeaProjects/KnowledgeOS/skill/scripts/check_service_health.py
```

Run live smoke:

```bash
python3 /Users/yibo/Documents/company/IdeaProjects/KnowledgeOS/skill/scripts/call_service_example.py \
  'https://xhslink.com/o/23s4jTem6em'
```

Optional API base override:

```bash
LINK_SKILL_API_BASE_URL=https://linktranscriber.store \
python3 /Users/yibo/Documents/company/IdeaProjects/KnowledgeOS/skill/scripts/call_service_example.py \
  'https://xhslink.com/o/23s4jTem6em'
```

## Follow-ups

Immediate:

- verify one real Douyin smoke path in addition to Xiaohongshu
- verify fresh ClawHub installs match the current package contents

## Constraints

- Keep this repo focused on public skill distribution only
- Do not pull backend implementation, deployment docs, or unrelated project history into this repo
- Do not turn this repo into a standalone reminder backend
- Prefer updating `SKILL.md`, `agents/openai.yaml`, `README.md`, and `CLAWHUB.md` together so public descriptions stay aligned
