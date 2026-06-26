---
name: find-skills
description: Suggest which patterns / integrations skills apply to a workflow based on its node types.
user-invocable: false
---

# find-skills

## When

While authoring a workflow, you want to know which patterns and integration docs apply.

## How

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/find_skills.py --workflow-key <key> [--env <env>]
```

If `--env` is given, reads the live workflow from n8n; otherwise reads the template at `n8n-workflows-template/<key>.template.json`.

## Side effects

Prints relative paths (one per line) to applicable `skills/patterns/*.md` and `skills/integrations/<service>/*.md` files. The agent is expected to read each suggested skill before adding nodes.

## Behavior

- Walks node `type` fields and node names.
- Maps Microsoft / Gmail / Google Drive / Slack / Notion / Airtable / Redis / Webhook node types to integration service folders.
- Triggers patterns based on node `type` substrings (e.g. `executeWorkflow*` → `subworkflows.md`, `errorTrigger` → `error-handling.md`, `openai`/`anthropic`/`agent` → `llm-providers.md`, "Lock Acquire" / "Lock Release" → `locking.md`).
- Always-on patterns: `validate-deploy`, `multi-env-uuid-collision`, `pindata-hygiene`.
