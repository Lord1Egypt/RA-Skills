# LetsPing OpenClaw Adapter

OpenClaw skill that sends high risk tool calls through LetsPing for human approval.

This package provides a `letsping_ask(tool_name, args_json, risk_reason)` skill for OpenClaw agents. It routes high risk actions through LetsPing so a human can approve, reject, or patch the payload before the agent proceeds.

The skill authenticates to LetsPing with a single agent key; the LetsPing service handles storage and delivery of approval requests.

## Installation

**Option A — npm (recommended):**

```bash
npm install @letsping/openclaw-skill
```

Then register the skill in your OpenClaw workspace so the gateway loads the `letsping_ask` tool.

**Option B — clone into workspace:**

```bash
git clone https://github.com/CordiaLabs/openclaw-skill ~/.openclaw/workspace/skills/letsping
cd ~/.openclaw/workspace/skills/letsping
npm install
```

Restart the OpenClaw gateway.

## Configuration

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "letsping": {
        "env": {
          "LETSPING_API_KEY": "lp_live_..."
        }
      }
    }
  }
}
```

- **`LETSPING_API_KEY`** (required): Your LetsPing agent key. Obtain it at https://letsping.co/openclaw/pair or via LetsPing’s Agent Credentials API.
- Treat this key as **highly sensitive**. Use a dedicated agent key and revoke it if compromised.

## Usage

Add the following to your agent's system prompt or `AGENTS.md`:

```
You have full authority for safe actions: reading files, logs, web searches, data analysis without side effects.

You MUST call letsping_ask BEFORE any high-risk action. NEVER execute high-risk actions directly.

High-risk includes:
- Financial: Spending money, bookings, transactions > $10
- Destructive: Delete/overwrite files, DB rows, configs
- Social: Posting, sending DMs/emails to new/public contacts
- Infrastructure: Modifying DNS, env vars, deployments, infra APIs

Provide:
- tool_name: exact tool name
- args_json: stringified JSON of arguments
- risk_reason: clear justification

After call:
- APPROVED: Use ONLY authorized_payload (may be patched)
- REJECTED or timeout: Abort, retry safely, or ask for guidance

Example:
letsping_ask(tool_name: "vercel_deploy", args_json: "{\"project\":\"my-app\",\"env\":\"production\",\"force\":true}", risk_reason: "Production deployment with force flag")
```

## Security model

The skill sends approval requests to LetsPing over HTTPS, authenticated with `LETSPING_API_KEY`. Protect this key: use a dedicated agent key, avoid committing it, and revoke it if compromised.

## How it works

1. Agent calls `letsping_ask` for a high-risk action.
2. Skill sends the request to LetsPing (authenticated with `LETSPING_API_KEY`).
3. LetsPing notifies the paired device; human reviews, optionally edits, then approves or rejects.
4. On approval, the skill returns the (possibly patched) payload to the agent.
5. Agent resumes using only the authorized payload.

Default timeout: 10 minutes.

## Troubleshooting

- Skill not loading: Check gateway logs (`openclaw gateway --log-level debug`). Ensure `npm install` succeeded.
- Agent skips call: Use strong models (Claude Opus, GPT-4o). Add more prompt examples.
- No notifications: Verify pairing and browser permissions.
- Timeout errors: Agent should handle gracefully.

Issues/PRs: https://github.com/CordiaLabs/openclaw-skill

https://letsping.co

## When you should not use this

- You do not use OpenClaw. In that case prefer the core SDKs or other framework adapters.
- You want LetsPing to replace OpenClaw's own permissions or user auth. This skill only governs specific tool calls, it does not manage identities inside OpenClaw.
- You need full prompt logging. The skill focuses on high risk actions, and payloads are encrypted end to end.