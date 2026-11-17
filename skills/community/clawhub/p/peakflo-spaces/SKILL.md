---
name: peakflo-spaces
description: Connect OpenClaw to Spaces by Peakflo, a hosted MCP server for finance and ops work. Hand off one-off or recurring tasks to cloud agents or people, and query workflows, data tables, reports, policy documents and approvals. Sign in with OAuth; no API keys.
homepage: https://spaces.peakflo.ai/docs/mcp/
metadata: {"openclaw":{"emoji":"🗂️"}}
---

# Spaces by Peakflo

Spaces by Peakflo is a hosted (remote) MCP server for finance and operations teams. Use it to:

- **Hand off work** to a cloud agent or a person, one-off or on a schedule (`task_create`).
- **Answer questions about the user's workspace**: workflows and their runs, data tables, aggregated reports, Business Context documents such as policies, and pending approvals.

Server facts:

- URL: `https://api.peakflo.ai/mcp`
- Transport: Streamable HTTP. Set it explicitly; OpenClaw uses SSE when `transport` is omitted.
- Auth: OAuth 2.1 with PKCE (S256) and dynamic client registration. The user signs up or signs in in the browser. There are no API keys or tokens to paste.

## Connect (one time)

If no Spaces tools are available in this session (no `peakflo__…` tools), the `peakflo` server is not set up yet. Give the user the commands below. **The user runs them in their own terminal on the Gateway host. Don't run them yourself:** `openclaw gateway stop` would stop the Gateway that is running this session, and sign-in needs the user's browser.

```bash
openclaw mcp add peakflo \
  --url https://api.peakflo.ai/mcp \
  --transport streamable-http \
  --auth oauth

# Stop the Gateway during sign-in. Sign-in still needs network access and a browser.
# The ";" makes sure the Gateway starts again even if sign-in fails or is cancelled.
openclaw gateway stop; openclaw mcp login peakflo; openclaw gateway start

openclaw mcp doctor peakflo --probe
```

The same definition as config (`mcp.servers` in `openclaw.json`):

```json5
{
  mcp: {
    servers: {
      peakflo: {
        url: "https://api.peakflo.ai/mcp",
        transport: "streamable-http",
        auth: "oauth"
      }
    }
  }
}
```

- `openclaw mcp login peakflo` prints an authorization URL. The user opens it, signs up or signs in, picks a workspace and clicks **Allow access**. OpenClaw catches the loopback redirect and saves the credentials. If the browser cannot reach the callback, use the printed `openclaw mcp login peakflo --code <code>` command.
- In the Control UI, a person with admin access can instead use **+ → Plugins → Add MCP server…** with the same URL, Streamable HTTP and OAuth.
- `doctor --probe` should report the server as ok and list its tools. A warning such as "OAuth credentials are not authorized" means the login step has not finished yet.
- OpenClaw exposes the tools as `peakflo__<tool>`. In this skill, a bare tool name refers to that tool: `task_create` means `peakflo__task_create`, `workflow_execute` means `peakflo__workflow_execute`, and so on. The safety rules below apply to the prefixed names too.

Never ask the user for a password, API key, token or authorization code in chat. Sign-in always happens in the browser.

## Hand off work: `task_create`

Use it when the user wants something done rather than answered: "have someone…", "every Monday…", "hand this off…", "collect…", "follow up with…".

- `title`: short and specific.
- `description`: clear instructions, with everything the assignee needs to do the work.
- `schedule` (optional): `{ "cron": "0 9 * * 1", "timezone": "Asia/Singapore" }`. The timezone is an IANA name and defaults to UTC.
- `assignee` (optional): `{ "kind": "user", "id": "<uuid>" }` for a person, with the ID taken from `users_list`. Use `{ "kind": "agent", "id": "<uuid>" }` only when the user gives you a Spaces agent ID. No tool in this skill lists agents. Never guess an ID, and never put a user ID under `kind: "agent"`.
- `clientRequestId`: generate one per intended task and reuse it if you retry, so a retry does not create a duplicate.

Routing:

- A one-off task with no assignee goes through triage to a suitable agent or person.
- A recurring task runs with the assignee you set. Without one, it goes to the user who created it. Recurring tasks are **not** triaged. So when the user wants someone else to do recurring work ("have someone in finance…"), find that person with `users_list` and set them as `assignee`. If you can't tell who it should be, ask. Don't leave the assignee empty.

Confirm before you create a task. `task_create` is a write: it notifies people, and a recurring task uses credits every time it runs. Show the user the title, the assignee (or "triage" for a one-off), and the schedule in plain words (for example "every Monday at 09:00 Asia/Singapore"). Create the task only after they say yes.

After the call, give the user the task link from the result. Say the task is **queued** or **scheduled**. Never say the work is done.

Examples:

- "Every Monday at 9am Singapore time, have someone in finance send me the AR ageing summary." → `users_list` to find the finance person (ask the user if it's unclear), confirm, then `task_create` with `schedule: { cron: "0 9 * * 1", timezone: "Asia/Singapore" }` and `assignee: { kind: "user", id: "<that person's ID>" }`.
- "Every Friday, remind me to review the payment run." → confirm, then `task_create` with `schedule` and no `assignee`. A recurring task with no assignee goes to the requesting user.
- "Hand off this vendor onboarding: collect the W-9 and bank details from Acme Ltd." → confirm, then a one-off `task_create` with no assignee, which goes through triage.

## Answer from the workspace (read-only)

Look up the answer before you reply. Don't answer from memory.

| Question | Tools |
|---|---|
| Workflows, automations and their runs | `workflow_list`, `workflow_get`, `workflow_execution_list`, `workflow_execution_get_steps` |
| Bills, invoices, payables, receivables, spend | `report_schema` → `report_schema_detail` → `report_query` |
| Custom data | `table_list` → `table_schema` → `table_query` or `table_sql` (read-only SQL) |
| Policies and reference documents | `datastore_list` → `datastore_query` |
| Pending approvals and human tasks | `task_list` |
| Connected apps (accounting, ERP, email) | `integrations_list` → `integration_mcp_tools_list` |

- If a report returns no rows, check the data tables (`table_list`) before you say there is no data.
- An empty result is a valid answer. Report it as empty.
- A missing tool or a permission error means the user has no access. Say so. It does not mean the data doesn't exist.
- The available tools follow the user's workspace role and permissions.

Examples: "Which of my workflows failed last week?", "Show unpaid and overdue bills by vendor.", "What does our expense policy say about client dinners?"

## Safety

- **Confirm before any write.** Before you create a task (`task_create`), run a workflow (`workflow_execute`), complete an approval (`task_complete`), call a connected-app tool that changes data (`integration_mcp_tool_call`), or change or delete table data, show the user exactly what you will do and wait for a yes.
- Every Spaces tool is annotated read-only, destructive or open-world. Treat anything not read-only as a write.
- **Don't start payments, and don't hide indirect ones.** You must not transfer money, make a payment or trade securities on your own. When asked to ("pay vendor X now", "buy 100 shares"), say you can't, and offer to create a task for a person instead. Spaces actions *can* lead to real money movement, though. Completing an approval can resume a workflow that posts entries or releases a payment. A workflow or a connected accounting, ERP or banking app can create or release payments. Before any of these, tell the user plainly that it may move money, and get an explicit yes. Afterwards, report exactly what the tool returned. Never say that no money moved, or that a payment happened, unless the result says so.
- Report results exactly as the tools return them, including failures.
- To disconnect, the user can run `openclaw mcp logout peakflo`, or revoke access in app.peakflo.ai → **Settings → MCP → Connected apps**.

## Links

- Docs: https://spaces.peakflo.ai/docs/mcp/
- Source and other client configs: https://github.com/peakflo/spaces-mcp
- Privacy: https://help.peakflo.co/peakflo-privacy-policy · Terms: https://help.peakflo.co/terms-and-conditions
- Support: https://help.peakflo.co · support@peakflo.co
