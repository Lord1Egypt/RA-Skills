# Setup, administration, and writes

Use this reference for access setup and workspace-changing workflows. For answering customer questions, start with the guide in `../SKILL.md`.

## Choose the interface

Use the highest-level interface already available:

1. If suitable `outlit_*` MCP or Pi tools are present, call them.
2. Otherwise, if the `outlit` CLI is installed, use it.
3. Otherwise, guide setup:
   - Coding agents: run `outlit onboard --agent <agent> --json`. Outside CI, it can start browser approval when no key is available, install the skill, validate access, and return next actions.
   - Skills only: run `outlit --skill` to print the current skill with no install, or `outlit setup --yes` / `outlit setup skills` to install a stub that points at it.
   - MCP clients: use the workspace URL from **Settings > CLI & MCP** and complete OAuth in the client. Do not hardcode a shared endpoint, bearer header, or API key into remote MCP configuration.

Tool availability depends on the MCP server or Pi tool policy. If a named tool is absent, use the CLI only where your policy permits, or ask the user to enable the appropriate toolset. `outlit_list_toolsets` shows the toolsets and their URLs; `outlit_load_toolset` returns tool descriptions and input schemas.

## Administration and write chooser

Read-tool CLI equivalents are in `../SKILL.md`; this table covers administration and writes.

| Need | Tool when exposed | CLI |
|------|-------------------|-----|
| Customer ownership and access | `outlit_set_customer_owner`, `outlit_set_customer_access` | `outlit customers set-owner`, `outlit customers set-access` |
| Browse automation destinations | `outlit_list_destinations` | `outlit destinations list` (`--ids` for specific ones) |
| Configure automation destinations | `outlit_create_destination`, `outlit_update_destination` | `outlit destinations create/update` |
| Archive a destination | `outlit_archive_destination` (preview, then confirm) | `outlit destinations archive` |
| Integration readiness or setup | `outlit_list_integrations`, `outlit_setup_integration`, `outlit_get_setup_session` | `outlit integrations list/setup`, `outlit setup-sessions get` |
| Activation setting | `outlit_get_settings`, `outlit_preview_activation`, `outlit_update_settings` | `outlit settings get`, `outlit activation preview`, `outlit settings update --activation-event` |
| Workspace timezone and default owner | `outlit_get_settings`, `outlit_update_settings` | `outlit settings get/update` |
| Workspace Features | `outlit_list_features`, `outlit_create_feature`, `outlit_archive_feature` | `outlit features list/create/archive` |
| Diagnose possible identity splits | `outlit_get_identity` | `outlit identity get <customer>` |
| Browse saved merge suggestions and history | `outlit_list_merge_suggestions` | `outlit merge-suggestions list` |
| Reject a saved suggestion | `outlit_reject_merge_suggestion` | `outlit merge-suggestions reject <suggestionId>` |
| Preview or execute a customer merge | `outlit_merge_customers` | `outlit customers merge <survivorId> <duplicateId>` |
| Track a merge operation | `outlit_get_merge` | `outlit merges get <operationId>` |
| Attention Inbox tasks | `outlit_list_tasks`, `outlit_get_task`, `outlit_act_on_task`, `outlit_undo_task_action` | `outlit tasks list/get/act/undo` |
| See or load toolsets | `outlit_list_toolsets`, `outlit_load_toolset` | n/a |

`outlit customers set-access` grants or changes a member's role (`viewer`, `editor`), and `--role none` removes it. The primary owner changes only through `outlit customers set-owner`.

Customer-associated people belong to customer accounts. Workspace members are internal Outlit users used for ownership and access actions. Do not substitute one ID type for the other.

The task tools read a person's own Attention Inbox. List and read work with OAuth or a personal key with customer read access; acting and undoing require a signed-in person through OAuth. A workspace API key has no task list. Acting on or undoing a task is a write: do it only when the user asks. Admins can pass `filters.owner` with a teammate's member ID to list that teammate's `today` or `open` tasks.

Retired tool names may answer as aliases during their published compatibility windows. Use the current names in this guide. Aliases ending 2026-12-11 include `outlit_list_users`, `outlit_get_customer_relationship`, `outlit_get_customer_features`, `outlit_get_customer_credits`, `outlit_list_crm_fields`, `outlit_schema`, the renamed admin/identity tools, and earlier CLI spellings; CLI aliases print `Renamed: use …` to stderr.

## Writes

Treat write operations as changes to the user's workspace. Assign owners, change access, configure integrations, reject merge suggestions, merge customer records, act on tasks, or mutate destinations, activation, settings, and Features only when the user explicitly asks.

Writes take `idempotencyKey` (tool input) or `--idempotency-key` (CLI). A retry with the same key and input returns the first result. Several admin writes preview first and require the returned preview token before execution; follow the tool's `next` call rather than reconstructing it.

## Identity and customer merges

Use `outlit_get_identity` when asked whether a customer is split. Its candidates and shared participants are leads, not proof, and an empty or incomplete result does not prove that no split exists. Do not combine evidence across records merely because they look related.

Merging is dangerous and has no supported undo. Execute only when the user authorized it and the records are certainly the same customer. Similar names, related domains, shared participants, a suggested match, or parent/subsidiary relationships are insufficient. The merge command defaults to preview; execution requires explicit permission, the reviewed preview token, and a stable idempotency key. Any pair involving an `individual` requires an eligible saved suggestion.

Read [the identity and merge workflow](identity.md) before previewing, rejecting, executing, retrying, or tracking a merge. It includes the five tool contracts, CLI examples, and asynchronous status handling.

Outlit-owned Churn and Renewal agents receive only the identity diagnostic for their assigned customer. Outlit-owned agents, including the Slack assistant acting for an admin, cannot reject suggestions or execute merges. Do not switch to CLI, API keys, or another identity to bypass an agent's tool policy or permissions. Customer-controlled agents may use the public tools within their granted authority.

## Authorization

Outlit API keys are independent workspace principals. They do not inherit their creator's human permissions or customer access. Key presets are Read only, Read and write, Personal CLI, Full workspace access, and Custom. Browser onboarding issues a Personal CLI key: read grants plus creator-owned integration setup, with Feature management when the creator has that permission. It does not grant general workspace integration administration.

Current read grants are:

- `customer_intelligence:read`
- `workspace_members:read`
- `analytics:read`
- `destinations:read`
- `behavior_metrics:read`
- `integrations:read`
- `activation:read`
- `workspace_settings:read`

Current write or setup grants are:

- `destinations:manage`
- `behavior_metrics:manage`
- `integrations:connect_own`
- `integrations:manage`
- `activation:manage`
- `workspace_settings:manage`
- `customer_access:manage`
- `customer_identity:review`
- `customer_identity:merge`
- `traffic_logs:write`

Identity diagnostics, saved suggestions, merge previews, and merge status require `customer_intelligence:read` for API keys. Rejection requires `customer_identity:review`; execution requires `customer_identity:merge`. The merge grant is excluded from Full workspace access and default presets; an admin must explicitly select it in a Custom key. OAuth MCP inherits the user's current permissions and record access.

A valid key can still receive `403` when it lacks the required grant. Do not retry that failure. Ask a workspace admin to review the key under **Settings > API Keys**. Remote MCP OAuth uses the signed-in user's current workspace authorization instead of an Outlit API key.

## CLI setup

Install the CLI:

```bash
curl -fsSL https://outlit.ai/install.sh | bash
# Alternatives:
npm install -g @outlit/cli
brew install outlitai/tap/outlit
```

Credential resolution order is `--api-key`, `OUTLIT_API_KEY`, then stored credentials. `--api-key` exists for compatibility, but do not use it in agent or CI commands because command arguments can expose the key; inject `OUTLIT_API_KEY` from the environment or secret store instead.

```bash
outlit onboard --agent <agent> --json
outlit auth login --browser --json
outlit auth status
outlit auth whoami
outlit doctor --json
```

Use `outlit auth login --browser` for browser approval. For CI or another non-interactive environment, inject `OUTLIT_API_KEY` from the environment or secret store. `outlit --skill` prints the current skill with no auth or network. `outlit setup --yes` and `outlit setup skills` install a stub skill that runs it, but do not configure MCP clients or integrations.

If `onboard` is unavailable, run `outlit upgrade`, then run `outlit --skill`, or use `outlit setup <agent>` / `outlit setup skills` to install the stub.

## CLI output behavior

- Interactive terminal: readable tables, spinners, and colors.
- Piped output, `--json`, CI, or `TERM=dumb`: JSON.
- Successful JSON is written to stdout. JSON errors are written to stderr with a nonzero exit status.

Agents should check the exit status and capture stderr instead of assuming every JSON payload is on stdout.

## MCP setup

Get the workspace URL from **Settings > CLI & MCP**:

```text
https://mcp.outlit.ai/w/<workspace-slug>/mcp
```

Add that URL directly to the MCP client and complete OAuth. Verify the connection with one of the tools actually exposed by the client.

With no query parameter the connection lists every tool. For the slim list, add `?toolsets=core,work,meta` to the URL (toolsets: `core`, `work`, `identity`, `admin`, `meta`). A connection still answers a call to any public tool its grants allow. Call `outlit_list_toolsets` to see what a toolset holds and the URL that lists it, and `outlit_load_toolset` for the tools' full descriptions and input schemas.

## Pi and tool packages

```bash
pi install npm:@outlit/pi
export OUTLIT_API_KEY=ok_your_api_key
pi
```

`@outlit/pi` registers the default customer-intelligence reads plus `outlit_list_toolsets` and `outlit_load_toolset` unless a custom policy is supplied. SQL and the broader public catalog are not enabled by default. Use `analyticalToolNames` for the default reads plus SQL, `piToolNames` for the Pi-supported public catalog, or the extension's `toolsets` option when the agent should receive those capabilities.

For custom TypeScript clients, `@outlit/tools` exports `publicToolContracts`, `publicToolNames`, `consumerToolPolicies`, `defaultToolNames`, `analyticalToolNames`, `piToolNames`, `cliToolNames`, `allPublicToolNames`, and `sqlToolNames`.

## Integrations

Use `setup` to connect or repair a data source; use `list` to inspect readiness. The current CLI exposes three commands:

```text
outlit integrations setup <provider>
outlit integrations list [provider]
outlit setup-sessions get <id>
```

Interactive `setup` negotiates capabilities first. It can securely prompt for a credential, open a validated browser handoff, or ask the user to confirm a CRM or Mixpanel mapping.

Do not ask the user to paste provider secrets into chat. Do not put secrets in model-visible tool calls, command arguments, logs, shell history, or process listings. When automation must supply provider configuration, have the user run the command in a trusted local terminal and send one strict JSON object through stdin:

```bash
printf '%s\n' '{"credentials":{"apiKey":"<provider-api-key>"}}' \
  | outlit integrations setup fireflies --config-stdin --json
```

Use `--accept-recommended` only to accept the exact CRM recommendation returned by the current setup response. Explicit mappings also go through `--config-stdin`.

JSON mode never prompts, opens a browser, or polls. It returns the setup result, including any handoff or required next step. `list` reports configuration readiness as `not_connected`, `awaiting_auth`, `setup_required`, `ready`, or `requires_intervention`; for a connected integration its connection section also reports when data was last received, sync status, and whether the sync has an error. `setup-sessions get` reports a browser sign-in that setup started (`pending`, `connected`, `expired`, or `failed`), using the `sessionId` its handoff returned.

Disconnect integrations through the Outlit web app. The CLI does not expose destructive integration removal.

## Troubleshooting

- Missing API key: use `outlit onboard --agent <agent> --json`, `outlit auth login`, or set `OUTLIT_API_KEY`. CI requires a key.
- Valid key but `403`: inspect the key's grants under **Settings > API Keys**.
- Setup issues: run `outlit doctor --json` and `outlit integrations list [provider] --json`.
- Stale CLI or missing current commands: run `outlit upgrade`.
- MCP auth issues: use the workspace URL and OAuth flow. Do not assume remote MCP requires an API key.
- Empty or missing data: first check that the customer, window, filters, and tool are the ones that would hold the answer. If the answer depends on integration data flow, inspect the integration's connection status; do not treat an unavailable section or an unconnected source as proof of absence.
