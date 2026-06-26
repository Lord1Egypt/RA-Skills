---
name: oo-agent-mail
description: "AgentMail (agentmail.to). Use this skill for ANY AgentMail request — reading, creating, updating, and deleting data. Whenever a task involves AgentMail, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "AgentMail"
  author: "OOMOL"
  version: "1.0.2"
  services: ["agent_mail"]
  icon: "https://static.oomol.com/logo/third-party/agent_mail.svg"
---

# AgentMail

Operate **AgentMail** through your OOMOL-connected account. This skill calls the `agent_mail` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected AgentMail. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "agent_mail" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "agent_mail" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `batch_get_messages` — Fetch multiple messages from a specific AgentMail inbox by message ID.
- `create_api_key` — Create an AgentMail API key. [write]
- `create_domain` — Create an AgentMail domain. [write]
- `create_draft` — Create a draft in a specific AgentMail inbox. [write]
- `create_inbox` — Create a new AgentMail inbox. [write]
- `create_inbox_api_key` — Create an API key scoped to a specific AgentMail inbox. [write]
- `create_inbox_list_entry` — Create an allow or block list entry scoped to a specific AgentMail inbox. [write]
- `create_list_entry` — Create a global AgentMail allow or block list entry. [write]
- `create_pod` — Create an AgentMail pod. [write]
- `create_pod_api_key` — Create an API key scoped to a specific AgentMail pod. [write]
- `create_pod_domain` — Create an AgentMail domain scoped to a pod. [write]
- `create_pod_inbox` — Create an AgentMail inbox scoped to a pod. [write]
- `create_pod_list_entry` — Create an AgentMail allow or block list entry scoped to a pod. [write]
- `create_webhook` — Create an AgentMail webhook. [write]
- `delete_api_key` — Delete an AgentMail API key. [destructive]
- `delete_domain` — Delete an AgentMail domain. [destructive]
- `delete_draft` — Delete a draft from a specific AgentMail inbox. [destructive]
- `delete_inbox` — Delete an AgentMail inbox. [destructive]
- `delete_inbox_api_key` — Delete an API key scoped to a specific AgentMail inbox. [destructive]
- `delete_inbox_list_entry` — Delete an allow or block list entry scoped to a specific AgentMail inbox. [destructive]
- `delete_inbox_thread` — Delete a thread from a specific AgentMail inbox. [destructive]
- `delete_list_entry` — Delete a global AgentMail allow or block list entry. [destructive]
- `delete_pod` — Delete an AgentMail pod. [destructive]
- `delete_pod_api_key` — Delete an API key scoped to a specific AgentMail pod. [destructive]
- `delete_pod_domain` — Delete an AgentMail domain scoped to a pod. [destructive]
- `delete_pod_inbox` — Delete an AgentMail inbox scoped to a pod. [destructive]
- `delete_pod_list_entry` — Delete an AgentMail allow or block list entry scoped to a pod. [destructive]
- `delete_pod_thread` — Delete an AgentMail thread scoped to a pod. [destructive]
- `delete_thread` — Delete an AgentMail thread. [destructive]
- `delete_webhook` — Delete an AgentMail webhook. [destructive]
- `forward_message` — Forward a specific AgentMail message. [write]
- `get_domain` — Get a single AgentMail domain.
- `get_domain_zone_file` — Get the DNS zone file records needed for an AgentMail domain.
- `get_draft` — Get a draft from a specific AgentMail inbox.
- `get_draft_attachment` — Get metadata and download URL for an attachment on a specific AgentMail draft.
- `get_global_draft` — Get a single AgentMail draft across accessible inboxes.
- `get_global_draft_attachment` — Get metadata and download URL for an attachment on an AgentMail draft.
- `get_inbox` — Get a single AgentMail inbox.
- `get_inbox_list_entry` — Get an allow or block list entry scoped to a specific AgentMail inbox.
- `get_inbox_thread` — Get a single thread from a specific AgentMail inbox.
- `get_inbox_thread_attachment` — Get metadata and download URL for an attachment in an AgentMail inbox thread.
- `get_list_entry` — Get a global AgentMail allow or block list entry.
- `get_message` — Get a single message from a specific AgentMail inbox.
- `get_message_attachment` — Get metadata and download URL for an attachment on a specific AgentMail message.
- `get_organization` — Get the AgentMail organization available to the current API key.
- `get_pod` — Get a single AgentMail pod.
- `get_pod_domain` — Get a single AgentMail domain scoped to a pod.
- `get_pod_domain_zone_file` — Get the DNS zone file records needed for an AgentMail pod domain.
- `get_pod_draft` — Get a single AgentMail draft scoped to a pod.
- `get_pod_draft_attachment` — Get metadata and download URL for an attachment on an AgentMail pod draft.
- `get_pod_inbox` — Get a single AgentMail inbox scoped to a pod.
- `get_pod_list_entry` — Get an AgentMail allow or block list entry scoped to a pod.
- `get_pod_thread` — Get a single AgentMail thread scoped to a pod.
- `get_pod_thread_attachment` — Get metadata and download URL for an attachment in an AgentMail pod thread.
- `get_raw_message` — Get a presigned download URL for the raw EML version of an AgentMail message.
- `get_thread` — Get a single AgentMail thread.
- `get_thread_attachment` — Get metadata and download URL for an attachment in an AgentMail thread.
- `get_webhook` — Get a single AgentMail webhook.
- `list_api_keys` — List AgentMail API keys.
- `list_domains` — List AgentMail domains.
- `list_drafts` — List drafts from a specific AgentMail inbox.
- `list_global_drafts` — List AgentMail drafts across accessible inboxes.
- `list_inbox_api_keys` — List API keys scoped to a specific AgentMail inbox.
- `list_inbox_events` — List events scoped to a specific AgentMail inbox.
- `list_inbox_list_entries` — List allow or block entries scoped to a specific AgentMail inbox.
- `list_inbox_threads` — List threads in a specific AgentMail inbox.
- `list_inboxes` — List inboxes available to the current AgentMail API key.
- `list_list_entries` — List global AgentMail allow or block entries.
- `list_messages` — List messages from a specific AgentMail inbox.
- `list_pod_api_keys` — List AgentMail API keys scoped to a pod.
- `list_pod_domains` — List AgentMail domains scoped to a pod.
- `list_pod_drafts` — List AgentMail drafts scoped to a pod.
- `list_pod_inboxes` — List AgentMail inboxes scoped to a pod.
- `list_pod_list_entries` — List AgentMail allow or block entries scoped to a pod.
- `list_pod_threads` — List AgentMail threads scoped to a pod.
- `list_pods` — List AgentMail pods.
- `list_threads` — List AgentMail threads across accessible inboxes.
- `list_webhooks` — List AgentMail webhooks.
- `query_inbox_metrics` — Query AgentMail metrics scoped to a specific inbox.
- `query_metrics` — Query AgentMail metrics across accessible resources.
- `query_pod_metrics` — Query AgentMail metrics scoped to a pod.
- `reply_all_message` — Reply to all recipients of a specific AgentMail message. [write]
- `reply_to_message` — Reply to a specific AgentMail message. [write]
- `search_inbox_threads` — Search threads in a specific AgentMail inbox.
- `search_messages` — Search messages in a specific AgentMail inbox.
- `search_pod_threads` — Search AgentMail threads scoped to a pod.
- `search_threads` — Search AgentMail threads across accessible inboxes.
- `send_draft` — Send a specific AgentMail draft. [write]
- `send_message` — Send a message from a specific AgentMail inbox. [write]
- `update_domain` — Update an AgentMail domain. [write]
- `update_draft` — Update a draft in a specific AgentMail inbox. [write]
- `update_inbox` — Update an AgentMail inbox display name or metadata. [write]
- `update_inbox_thread` — Update labels on a thread in a specific AgentMail inbox. [write]
- `update_message` — Update labels on a message in a specific AgentMail inbox. [write]
- `update_pod_domain` — Update an AgentMail domain scoped to a pod. [write]
- `update_pod_inbox` — Update an AgentMail inbox scoped to a pod. [write]
- `update_pod_thread` — Update labels on an AgentMail thread scoped to a pod. [write]
- `update_thread` — Update labels on an AgentMail thread. [write]
- `update_webhook` — Update an AgentMail webhook. [write]
- `verify_domain` — Ask AgentMail to verify a domain's DNS records.
- `verify_pod_domain` — Ask AgentMail to verify a pod domain's DNS records.
- `who_am_i` — Get AgentMail identity information for the current API key.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change AgentMail state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — AgentMail is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=agent_mail
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- AgentMail homepage: https://agentmail.to
