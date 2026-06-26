---
name: infodashboard
description: Guided SOP for setting up and using InfoDashboard from OpenClaw. Use when the user wants to clone the InfoDashboard repo, configure database and LLM keys, start the service, or generate a Streamlit dashboard from a natural-language requirement. Run one phase at a time and ask for confirmation before each state-changing step.
user-invocable: true
metadata: { "openclaw": { "emoji": "🏭" } }
---

# InfoDashboard Skill

Use this as a guided, confirmation-heavy SOP. Do not compress the whole setup into one reply and do not perform state-changing actions without explicit user confirmation.

## Core Rules

- Move one phase at a time.
- Before any state-changing action, ask for confirmation.
- If local state already exists, show what you found and ask whether to keep it.
- InfoDashboard generation uses server-side provider config, not the OpenClaw agent's own model or API key.
- This skill must not rely on any request-time model or provider overrides.
- Only server-side config files (`.env.local`) may control LLM provider selection.
- Do not ask the user to paste API keys or database passwords into chat.
- Prefer guiding the user to edit `.env.local` themselves.
- Do not offer to write secrets into config files on the user's behalf.
- Once setup is complete and the user clearly asks to generate a dashboard, do not ask for a second confirmation before submitting the generation request.

## Optional Skill Config

If present, read defaults from `~/.openclaw/openclaw.json` under:

```jsonc
{
  "skills": {
    "entries": {
      "infodashboard": {
        "enabled": true,
        "config": {
          "repoDir": "/path/to/InfoDashboard",
          "url": "http://localhost:8001"
        }
      }
    }
  }
}
```

Use `repoDir` and `url` only as defaults. Still confirm before acting.

## SOP Phases

### 1. Clone Or Reuse Existing Repo

Load [references/clone.md](references/clone.md).

Establish which InfoDashboard checkout to use. If a checkout already exists, show the path and ask whether to reuse it.

### 2. Configure Environment

Load [references/config.md](references/config.md).

Configure `.env.local` with LLM provider keys and database connection details. This includes verifying that Docker and the frpc SOCKS5 tunnel are in place.

### 3. Start And Verify

Load [references/startup.md](references/startup.md).

Start the FastAPI server and confirm it is healthy at `GET {url}/`.

### 4. Generate A Dashboard

Load [references/generate-flow.md](references/generate-flow.md).

Submit the user's natural-language requirement and follow the SSE stream until a dashboard URL is returned.

## Response Style

- Keep each step short and explicit.
- Prefer 2-3 concrete options when the user must choose.
- Always include the recommended option first and explain why in one sentence.
- After a step completes, say what changed and what the next confirmation is for.
- When returning a dashboard URL, place the raw absolute URL on its own line with no bold, markdown link syntax, code formatting, or tables.
