---
name: idea-capture
description: Capture or update an idea, append an update log, and write a session summary for later retrieval.
---

# Idea Capture

Use this skill when the user wants to save or update an idea/project discussion.

## Storage
- Main idea doc: `ideas/<idea-id>.md`
- Session summaries: `ideas/summaries/<idea-id>/<timestamp>.md`
- Human index: `ideas/INDEX.md`
- Machine catalog: `ideas/catalog.json`

## Inputs
Provide what you have:
- `title`
- `summary`
- `notes`
- `tags`
- `mode`: `create` | `update` | `auto`
- optional `idea_id`
- optional `source`
- optional open questions / next steps

## Matching rules
- `update`: require an existing match
- `auto`: prefer `idea_id`, then normalized title/slug, else create
- avoid duplicate idea files when a clear match exists

## Behavior
Use `scripts/idea_capture.py` for the write/update work.

Example:
```bash
python3 skills/idea-capture/scripts/idea_capture.py \
  --title "Desktop Pet OpenClaw" \
  --summary "Turn OpenClaw into a desktop pet assistant" \
  --notes "Need create/update/session-summary support." \
  --tags ai,desktop,agent \
  --mode auto \
  --source qqbot
```

## Expected result
Report:
- idea id
- created vs updated
- changed files
- session summary path

## Guardrails
- Keep the main idea doc readable.
- Preserve update history.
- Put chronology in update logs / session summaries, not in long repeated prose.
