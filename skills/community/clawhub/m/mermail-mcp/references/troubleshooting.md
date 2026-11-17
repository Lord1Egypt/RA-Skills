# Mermail MCP verification and recovery

Read this reference after configuration to verify the selected profile or diagnose initialization, discovery, scope, and argument failures.

## Verification contract

For API-key mode, run from the skill directory:

```bash
node scripts/check-connection.mjs
```

The script requires `MERMAIL_API_KEY`; it does not validate OAuth sessions. It calls MCP `initialize`, then `tools/list`, rejects duplicate or malformed tool entries, and checks required canaries by catalog name only. Canary write tools are never invoked.

For OAuth mode, use the client's MCP status and tool catalog. Confirm:

1. `initialize` returned Mermail server information.
2. `tools/list` returned the intended profile.
3. One read-only `list_workspaces` or `list_mailboxes` call succeeded in the selected workspace.

## Catalog expectations

- The full API-key profile currently has a base catalog of 83 tools, including 82 business definitions plus `prepare_destructive_action`. Future releases may add tools.
- Compatibility verification: the bundled script accepts at least the 63-tool full-catalog floor plus required canaries so it can diagnose gradual deployments while still warning when the current 83-tool base is absent.
- Full-profile member OAuth: includes the base catalog and may add `get_paybox_connection`, safe invocation status, MCP App resources, and model-visible live `paybox_*` tools through the workspace owner's active connection.
- Full-profile owner OAuth: additionally exposes owner-only connect/reauth behavior and legacy Agent Wallet compatibility tools. When a member sees `OWNER_ACTION_REQUIRED`, do not invent a handoff or reconnect the host connector; the workspace owner must connect or repair PayBox in Mermail.
- `agent-inbox`: exactly 12 tools: `get_api_credit_usage`, `list_workspaces`, `get_workspace`, `list_email_domains`, `list_workspace_mailboxes`, `list_mailboxes`, `create_mailbox`, `get_mailbox`, `list_emails`, `search_emails`, `get_email`, and `get_email_context`. This is a provisioning-plus-safe-read profile, not a read-only profile: `create_mailbox` is the sole scoped provisioning write and must not be called to test connectivity.

Wallet tools, `prepare_destructive_action`, send, delete, Composio, mailbox-agent, and workspace-admin tools must remain absent from `agent-inbox`. A hidden tool call against that profile must fail rather than escaping the profile.

## Failure matrix

| Symptom | Meaning | Safe recovery |
| --- | --- | --- |
| `MERMAIL_API_KEY` missing | Launching process lacks API-key secret | Set it in that process environment and restart |
| Invalid workspace API key format | Wrong value or accidental prefix | Correct the secret source without pasting it into chat |
| `401` with `WWW-Authenticate` | Missing/expired/revoked credential or OAuth login required | Authenticate or replace a revoked key; do not retry writes |
| OAuth loop or cleared Cursor credential | Client/browser consent state is stale | Remove and re-add the MCP entry, log out in browser if needed, authenticate again |
| `403` | Workspace mismatch, role, policy, or missing `mcp:tools` | Verify selected workspace and permission; do not switch silently |
| `402` | Developer access or credits exhausted | Report plan/credit blocker and stop |
| `429` | RPM window exhausted | Wait for the window; never rotate keys to bypass it |
| Missing expected tool | Wrong profile, API-key wallet limitation, role, stale catalog, or older deployment | Identify which boundary applies before reconnecting |
| Transport/initialize failure | URL, network, TLS, protocol, or client transport issue | Verify exact endpoint and Streamable HTTP support |

## Stale client tool registry

Claude web may show **Finding tools** or `Tool 'Mermail:<name>' not found` even when the server catalog is healthy. Treat this as a stale or unloaded connector registry:

1. Confirm the production server card still advertises the bare protocol name.
2. Disable/re-enable or disconnect/reconnect Mermail and complete OAuth again if prompted.
3. Start a new chat after reconnecting.
4. Smoke-test the exact host-qualified read-only mailbox-list identifier exposed by that host.
5. Retry the original domain workflow only after discovery succeeds.

Do not retry under a guessed namespace. Do not manually add, strip, or invent a prefix.

## Argument and domain validation

If discovery succeeds but a call is rejected, inspect the live input schema. Pass `query` and `body` as native JSON objects; never send an escaped string such as `"{\"folder\":\"inbox\"}"`. For newest-first email lists use separate `sortColumn: "date"` and `sortDirection: "DESC"` fields.

Write tools may return `code: "validation_failed"` with a `details` array. Correct only the named fields without changing the target or intended effect. Send/reply/forward accept `body.html` and/or `body.text` plus `body.from`; drafts and schedule use string `body.body`. Continue through `mermail-compose-email`, not this connection skill.

After a reconnect, never replay a write whose prior result is uncertain. Read authoritative state once and return to the owning domain skill.

MCP is a stateless POST endpoint. An unauthenticated GET may return an OAuth discovery challenge and an authenticated GET may return `405`; neither replaces `initialize` followed by `tools/list`. Accept both `application/json` and `text/event-stream` responses.
