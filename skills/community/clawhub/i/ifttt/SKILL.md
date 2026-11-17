---
name: ifttt
description: Connect OpenClaw to IFTTT's hosted MCP server and automate hundreds of services — discover triggers and actions, build and manage Applets, and run actions and queries. Use when the user mentions IFTTT, asks what they can automate, or describes an automation like "when X happens, do Y".
version: 1.0.0
metadata: {"openclaw": {"emoji": "⚡", "homepage": "https://github.com/IFTTT/ifttt-plugins"}}
---

# IFTTT

[IFTTT](https://ifttt.com) is "if this, then that" — automation across hundreds of services, from Gmail and Google Sheets to Philips Hue and Webhooks. This skill connects OpenClaw to IFTTT's hosted MCP server at `https://ifttt.com/mcp` and teaches the agent to discover services, build Applets, and run actions responsibly.

## When to use

- The user mentions IFTTT for the first time or asks what they can automate
- The user describes an automation: "when X happens, do Y"
- IFTTT tools return authentication or "service not connected" errors

## Connect the MCP server

Add the server to the OpenClaw config:

```json
{
  "mcp": {
    "servers": {
      "ifttt": {
        "url": "https://ifttt.com/mcp",
        "transport": "streamable-http",
        "auth": "oauth"
      }
    }
  }
}
```

Reload so the running process picks up the new server, then authenticate:

```sh
openclaw mcp reload
openclaw mcp login ifttt
```

The browser opens IFTTT's authorization page — sign in (or create a free account) and approve access. On a headless install the command prints the authorization URL instead; open it on any device, then finish with `openclaw mcp login ifttt --code <code>`.

## Authenticating

There are two separate layers of authentication. Do not confuse them.

**Layer 1 — connecting the MCP server itself (OpenClaw-managed OAuth).** No IFTTT tool performs this login. If IFTTT tools are unavailable or every call fails with an authentication error:

1. Ask the user to run `openclaw mcp login ifttt` and approve access in the browser. Then stop and wait for the user to confirm before retrying — do not rewrite config files or retry in a loop.
2. Once connected, verify with `get_user_info`. It returns the user's IFTTT plan tier, which gates some features (e.g. Filter Code requires Pro+).

**Layer 2 — connecting individual services (IFTTT-managed).** Once the server is authenticated, each service (Gmail, Dropbox, ...) still needs its own connection on the user's IFTTT account:

1. When a tool reports a service is not connected, call `connect_service` with the `service_slug` — it returns a `connect_url`. Present that URL to the user as a clickable link, wait for them to finish connecting, then retry the original request.
2. If `connect_service` reports `mode: "reconnect"` for a specific account, the account's authorization expired — present the `reconnect_url` and wait for the user to re-authorize before retrying.

## Key concepts

- **Service**: an integration IFTTT supports (Gmail, Google Sheets, Philips Hue, Webhooks, ...). Each service has a unique `slug` (e.g. `google_sheets`). Never guess slugs — always look them up with `search_services` or `get_services`.
- **Trigger**: the "if this" event that starts an Applet (e.g. "New email in inbox").
- **Action**: the "then that" step an Applet performs (e.g. "Add row to spreadsheet").
- **Query**: an optional step that fetches extra data between the trigger and actions.
- **Ingredient**: a data field produced by a trigger or query, usable in downstream action fields.
- **Applet**: a saved automation combining one trigger, optional queries, and one or more actions.

## Tool overview

Discovery (read-only):
- `get_user_info` — account, plan tier, and limits
- `search_services` / `get_services` — find services by keyword or list them
- `get_steps` — fetch triggers, queries, and actions for one or more services in a single call (preferred)
- `get_triggers` / `get_queries` / `get_actions` — per-service, per-type variants
- `my_applets` / `search_applets` / `get_applet` — inspect the user's existing Applets

Connections:
- `connect_service` — returns a `connect_url` (or `reconnect_url`) for linking a service account; see Authenticating

Applet lifecycle:
- `create_applet` / `edit_applet` — build or modify an Applet
- `enable_applet` / `disable_applet` / `remove_applet` — manage Applet state
- `set_applet_filter_code` — add conditional logic (Pro+ only)

Direct execution:
- `run_action` — perform a one-off action immediately (has real-world side effects)
- `run_query` — fetch data from a connected service
- `geocode` — resolve place names to coordinates for location-based triggers

## Building an Applet

1. **Find the services.** Call `search_services` with keywords from the user's request to get exact service slugs. Never guess a slug.
2. **Discover the steps.** Call `get_steps` with the trigger service and action service(s) to fetch available triggers, queries, and actions with their field definitions, ingredients, and a ready-made `step_template`.
3. **Connect missing services.** Discovery results include `connected` and a `connect_url` when a service isn't connected. Present the `connect_url` to the user, wait for confirmation, then re-run discovery to pick up their `account_id`.
4. **Fill the templates.** Copy `step_template` from each chosen step verbatim, then fill in `account_id` and the step's fields. Action and query fields can reference trigger/query ingredients — use them to pass data between steps.
5. **Create.** Call `create_applet` with `name`, an optional but recommended `description`, the `trigger`, and `actions` (plus optional `queries` and `actions_delay` up to 14,145 seconds). The Applet is created and enabled immediately — tell the user this before calling. On success, share the returned `applet_url` so the user can view it.
6. **Handle validation errors.** A failed `create_applet` returns structured `errors`. Fix the referenced fields and retry; don't retry unchanged input.

## Editing

- Call `get_applet` first to see the Applet's current configuration, then `edit_applet` with the changed pieces.
- Applets can only be edited if the user owns them. Editing a published community Applet the user enabled may create the user's own copy — relay that to the user when it happens.

## Filter Code (Pro+ only)

- `set_applet_filter_code` adds conditional logic between trigger and actions.
- Pass a **natural-language prompt** describing the behavior (e.g. "only run on weekdays") — never pass TypeScript/JavaScript directly; the tool generates the code server-side.
- Pass an empty string to clear existing Filter Code.
- If the response includes `made_it_your_own: true`, a new user-owned copy of a community Applet was created — tell the user explicitly and use the new `applet_slug` going forward.

## Testing

- Use `run_query` to preview the data a query step would return.
- Use `run_action` to test an action — but it performs the action for real (sends the email, turns on the lights). Confirm with the user before running actions with visible side effects.
- Location-based triggers need coordinates; use `geocode` to convert place names.

## Guardrails

- Never guess service slugs, trigger/action/query identifiers, or Applet slugs. Always discover them via `search_services`, `get_steps`, `my_applets`, or `get_applet` first.
- If the IFTTT MCP server itself is unauthenticated (tools missing, or every call fails with an auth error), do not try to fix it by rewriting config files and do not retry in a loop. Ask the user to run `openclaw mcp login ifttt`, then wait for their confirmation before retrying.
- `create_applet` enables the Applet immediately. Summarize what the Applet will do (trigger, actions, and any queries or delay) and get the user's confirmation before creating it.
- Confirm with the user before calling `remove_applet` (permanent) or `run_action` (performs the action for real — messages get sent, devices get switched).
- When a tool reports a service is not connected or an account is offline, do not retry blindly. Call `connect_service`, present the returned `connect_url` or `reconnect_url` to the user as a link, wait for them to confirm, then retry the original request.
- Features gated by subscription (e.g. Filter Code requires Pro+): if a tool reports a plan restriction, tell the user which plan is required and link to https://ifttt.com/plans instead of retrying.

## Example invocations

> "When I get an email with an attachment, save it to Dropbox"
>
> "Turn my office lights red whenever CI fails"
>
> "Send me a phone notification every day at 9am with my first calendar event"
>
> "Add a row to my expenses spreadsheet every time I get a receipt email"
>
> "What's the temperature from my weather station right now?"
