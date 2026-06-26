---
name: inariwatch
description: AI monitoring that fixes your code — query alerts, trigger remediations, rollback deploys, chat with your infrastructure
homepage: https://inariwatch.com
user-invocable: true
metadata: {"openclaw":{"requires":{"env":["INARIWATCH_TOKEN"]},"primaryEnv":"INARIWATCH_TOKEN"}}
---

# InariWatch — AI Monitoring That Fixes Your Code

You are connected to InariWatch via MCP. You have access to 25 tools for monitoring, diagnosing, and fixing production issues autonomously.

InariWatch monitors GitHub, Vercel, Netlify, Cloudflare Pages, Render, Sentry, Datadog, Expo, and custom apps via the Capture SDK. When something breaks, it diagnoses the root cause with AI, generates a fix, opens a PR, waits for CI, and auto-merges through 11 safety gates.

## Available tools

### Check status
- "What's breaking in production?" -> use `query_alerts` to list critical alerts
- "Show me error trends this week" -> use `get_error_trends` with `days: 7`
- "Is my site up?" -> use `get_uptime` to check all monitors
- "Show project status" -> use `get_status` for projects, integrations, and alert counts

### Diagnose issues
- "What caused this error?" -> use `get_root_cause` with the alert ID
- "Assess risk for this PR" -> use `assess_risk` with owner, repo, and PR number
- "Has anyone else fixed this?" -> use `search_community_fixes` with the error message
- "Generate a post-mortem" -> use `get_postmortem` with the alert ID
- "Get build logs" -> use `get_build_logs` for the latest failed deploy

### Fix issues
- "Fix the latest critical alert" -> use `trigger_fix` with the alert ID to start AI remediation
- "Roll back production" -> use `rollback_deploy` with the project ID (works on Vercel, Netlify, Cloudflare Pages, Render)
- "Silence this alert" -> use `silence_alert` with the alert ID
- "Acknowledge this alert" -> use `acknowledge_alert` to mark as read
- "Reopen this alert" -> use `reopen_alert` to reopen a resolved alert

### Monitor and explore
- "Add uptime monitoring for api.example.com" -> use `create_uptime_monitor` with the URL
- "Run a health check" -> use `run_health_check` for all monitors
- "Check if this can be reproduced" -> use `reproduce_bug` with the alert ID
- "Simulate this fix" -> use `simulate_fix` with the alert ID and proposed changes
- "Verify the remediation worked" -> use `verify_remediation` with the session ID
- "Search my codebase for auth logic" -> use `search_codebase` with the query
- "Reindex my codebase" -> use `reindex_codebase` with the project ID
- "Ask about my infrastructure" -> use `ask_inari` with a natural language question

## Important rules

1. **Always confirm before destructive actions.** `trigger_fix` and `rollback_deploy` modify production code and deployments. Ask the user for explicit confirmation before executing these.
2. **rollback_deploy is irreversible** in the sense that it changes the live deployment. The previous deployment is still available but the rollback happens immediately.
3. **Rate limits apply.** Query tools: 200/min. Analysis tools: 30/min. Execution tools (fix, rollback): 5/min. If you hit a limit, wait and retry.
4. **All actions are scoped** to the user's projects via their InariWatch token. You cannot access other users' data.
5. **trigger_fix starts an async pipeline.** It returns a session ID immediately. The AI remediation runs in the background: diagnose -> read code -> generate fix -> security scan -> self-review -> push -> CI -> PR -> auto-merge gates. You can check progress with `verify_remediation`.
6. **Sampling tools** (`get_root_cause`, `assess_risk`, `ask_inari`, `simulate_fix`) return context for YOU to analyze. Process the returned data and provide your own analysis to the user.

## Setup

The user needs an InariWatch account at https://app.inariwatch.com and a token from **Settings -> API Tokens**.

**Option 1 — Auto-detect (recommended):**
```bash
npx @inariwatch/mcp init
```
This detects OpenClaw and configures automatically.

**Option 2 — Manual CLI:**
```bash
openclaw mcp set inariwatch '{"url":"https://mcp.inariwatch.com","transport":"streamable-http","headers":{"Authorization":"Bearer YOUR_TOKEN"}}'
```

**Option 3 — Edit config directly:**
Add to `~/.openclaw/openclaw.json`:
```json
{
  "mcp": {
    "servers": {
      "inariwatch": {
        "url": "https://mcp.inariwatch.com",
        "transport": "streamable-http",
        "headers": {
          "Authorization": "Bearer YOUR_TOKEN"
        }
      }
    }
  }
}
```
