---
name: oo-listmonk
description: "Listmonk (listmonk.app). Use this skill for ANY Listmonk request — reading, creating, updating, and deleting data. Whenever a task involves Listmonk, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Listmonk"
  author: "OOMOL"
  version: "1.0.2"
  services: ["listmonk"]
  icon: "https://static.oomol.com/logo/third-party/listmonk.svg"
---

# Listmonk

Operate **Listmonk** through your OOMOL-connected account. This skill calls the `listmonk` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Listmonk. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "listmonk" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "listmonk" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `blocklist_subscribers` — Blocklist one or more listmonk subscribers. Blocklisted subscribers are unsubscribed from every list and never receive campaigns. [destructive]
- `cancel_campaign` — Cancel a running or paused campaign permanently. A cancelled campaign cannot be resumed. [destructive]
- `create_campaign` — Create a listmonk campaign as a draft. Nothing is sent: use send_campaign_test to preview it by email, then schedule_campaign or start_campaign to send it. Setting sendAt here only stores the time; the campaign is not scheduled until schedule_campaign runs. [write]
- `create_list` — Create a listmonk mailing list. [write]
- `create_subscriber` — Create a listmonk subscriber and optionally subscribe it to lists. Double opt-in lists send a confirmation email unless preconfirmSubscriptions is true. [write]
- `delete_campaign` — Permanently delete one listmonk campaign. [destructive]
- `delete_subscriber` — Permanently delete one listmonk subscriber and its subscriptions. [destructive]
- `get_campaign` — Fetch one listmonk campaign with its status, schedule, target lists, body, and delivery counters.
- `get_campaign_analytics` — Fetch campaign analytics over a date range: daily view, click, or bounce counts, or per-link click counts (type links).
- `get_campaign_preview` — Render the campaign body inside its template and return the HTML preview, exactly as recipients would see it.
- `get_list` — Fetch one listmonk list.
- `get_profile` — Fetch the listmonk user profile of the connected API user, including its role and permissions.
- `get_running_campaign_stats` — Fetch live delivery stats (sent, to_send, rate, started_at) for currently running campaigns, optionally narrowed to specific campaign IDs.
- `get_subscriber` — Fetch one listmonk subscriber with attributes and list subscriptions.
- `get_template` — Fetch one listmonk template including its body.
- `list_campaigns` — List listmonk campaigns, optionally filtered by a name/subject search, statuses, or tags, with paging.
- `list_lists` — List listmonk mailing lists with subscriber counts, optionally filtered by name, status, or tags.
- `list_subscribers` — Query listmonk subscribers, optionally filtered by list membership and an SQL expression over the subscribers table, with paging.
- `list_templates` — List listmonk templates (campaign, visual campaign, and transactional) to pick a templateId for campaigns.
- `manage_subscriber_lists` — Add subscribers to lists, remove them from lists, or mark their subscriptions as unsubscribed. status is required when action is add. [write]
- `pause_campaign` — Pause a running campaign. It can be resumed later with start_campaign. Only running campaigns can be paused. [write]
- `schedule_campaign` — Schedule a draft or paused campaign to be sent automatically at sendAt: stores sendAt on the campaign, then changes its status to scheduled. A campaign that is already scheduled is simply moved to the new time. SENDS EMAIL TO ALL SUBSCRIBERS OF THE TARGET LISTS - confirm with the user before executing. [write]
- `send_campaign_test` — Send the campaign as it is currently saved to specific test addresses only (not to the lists). Each address must already exist as a subscriber in listmonk. [write]
- `start_campaign` — Start sending a draft or paused campaign immediately (status running); a paused campaign resumes where it stopped. SENDS EMAIL TO ALL SUBSCRIBERS OF THE TARGET LISTS - confirm with the user before executing. [write]
- `unschedule_campaign` — Unschedule a scheduled campaign by moving it back to draft, so it is not sent at its sendAt. The stored sendAt is kept; only scheduled campaigns can be unscheduled. [write]
- `update_campaign` — Update a draft, scheduled, or paused listmonk campaign. Only the provided fields change; target lists and attachments are preserved unless listIds is given. Pass sendAt null to clear a stored send time; listmonk rejects every update while the stored send time is in the past. [write]
- `update_list` — Update one listmonk list. Only the provided fields change; the current name and tags are preserved when omitted. [write]
- `update_subscriber` — Update one listmonk subscriber. Only the provided fields change: the current subscriber is read first and merged, so omitted fields and list subscriptions are preserved. Passing listIds replaces the subscriber's list subscriptions; attribs replaces all attributes. Unless preconfirmSubscriptions is true, an instance with opt-in confirmations enabled emails the subscriber again for every double opt-in list that is still unconfirmed. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Listmonk state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Listmonk is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/listmonk
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Listmonk homepage: https://listmonk.app
- API documentation: https://listmonk.app/docs/apis/apis/
