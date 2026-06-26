---
name: letsping
description: Human-in-the-loop approval for high-risk agent actions (sudo protocol). Agent must call letsping_ask before destructive/financial/social/infra changes.
disable-model-invocation: false
metadata:
  openclaw:
    emoji: ":shield:"
    requires:
      env: ["LETSPING_API_KEY"]
---

### Install (runtime)

This registry entry is **instruction-only**. The `letsping_ask` **runtime** is provided by the npm package **`@letsping/openclaw-skill`**. Use one of:

- **npm:** `npm install @letsping/openclaw-skill` (then register the skill in your OpenClaw workspace so it loads `letsping_ask`).
- **Clone:** `git clone https://github.com/CordiaLabs/openclaw-skill ~/.openclaw/workspace/skills/letsping && cd ~/.openclaw/workspace/skills/letsping && npm install`.

Set **`LETSPING_API_KEY`** (your LetsPing agent key, e.g. `lp_live_...`) in the skill's env. Obtain it at https://letsping.co/openclaw/pair or via LetsPing's Agent Credentials API. Treat this key as **highly sensitive**; use a dedicated agent key and revoke if compromised.

### Usage

This skill provides the `letsping_ask` tool, a secure escalation point for high risk actions. The agent calls it, blocks until your approval/patch/reject via the LetsPing PWA, then resumes with the **authorized payload only**.

**Critical**: Use frontier models (e.g., Claude Opus, GPT-4o or better) to minimize prompt bypass risk. Smaller models are vulnerable to drift/injection.

**Copy-paste this into your workspace TOOLS.md or AGENTS.md** (or append to system prompt):

```text
You have full autonomous authority for **SAFE** actions only: reading files/logs, web searches, viewing/analyzing data without side effects.

You **MUST** call `letsping_ask` **BEFORE** any **HIGH-RISK** action—and **NEVER** execute the action directly. High-risk includes:
- Financial: Any spending, transactions, bookings > $10
- Destructive: Deleting/overwriting files, DB rows, configs
- Social: Posting publicly, sending DMs/emails to new contacts, or group chats
- Infrastructure: Modifying DNS, env vars, deployments, infra APIs, or permissions

When escalating:
- Provide tool_name (exact tool, e.g., "system_run")
- args_json: Stringified JSON of the original arguments
- risk_reason: Clear, concise justification (e.g., "Potential file deletion")

After the call returns:
- If APPROVED: Use **ONLY** the `executed_payload` / authorized payload (patched if edited)
- If REJECTED or TIMEOUT: Abort the action, retry with safer plan, or ask user for guidance

Few-shot examples:
1. Safe (no call): browser_search(query: "current weather in NYC")
2. Risky deploy: letsping_ask(tool_name: "vercel_deploy", args_json: "{\"project\":\"my-app\",\"env\":\"production\",\"force\":true}", risk_reason: "Production deployment with force flag")
3. Risky delete: letsping_ask(tool_name: "system_run", args_json: "{\"cmd\":\"rm -rf /important/folder\"}", risk_reason: "Destructive file deletion")
4. Risky post: letsping_ask(tool_name: "discord_send", args_json: "{\"channel\":\"general\",\"message\":\"Accidental dump: ls ~\"}", risk_reason: "Potential data leak in public channel")
```

**Test thoroughly in a sandbox session first**: simulate high risk plans and verify escalation rate (~90-95% reliable on strong models/prompts). If the agent skips calls, add more examples or tighten language.

**Troubleshooting:**

* **Agent ignores rule?** Strengthen with more few-shots or "ALWAYS escalate if any risk category matches."
* **Timeout/reject?** Agent prompt should handle gracefully (e.g., "If rejected, propose alternative").
