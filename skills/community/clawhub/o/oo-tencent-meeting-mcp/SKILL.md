---
name: oo-tencent-meeting-mcp
description: "Tencent Meeting MCP (meeting.tencent.com). Use this skill for ANY Tencent Meeting MCP request — reading, creating, updating, and deleting data. Whenever a task involves Tencent Meeting MCP, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Tencent Meeting MCP"
  author: "OOMOL"
  version: "1.0.2"
  services: ["tencent_meeting_mcp"]
  icon: "https://static.oomol.com/logo/third-party/tencent_meeting_mcp.svg"
---

# Tencent Meeting MCP

Operate **Tencent Meeting MCP** through your OOMOL-connected account. This skill calls the `tencent_meeting_mcp` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Tencent Meeting MCP. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "tencent_meeting_mcp" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "tencent_meeting_mcp" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `apply_record_permission_commit` — Submit a recording-access request only after prepare has displayed the preview and the user has explicitly confirmed. Use the same meeting_record_id; refresh an expired preview first. [write]
- `apply_record_permission_prepare` — Preview a recording-access request. Show the meeting, owner, applicant, and requested permission to the user before submitting.
- `call_tool` — Call a tool discovered by list_tools using its current argument schema. This can modify or delete business data. Confirm meeting changes and cancellations with the user. Preview recording-access requests with apply_record_permission_prepare and obtain user confirmation before commit. Submit feedback only with explicit consent. Async tools may require get_job_result. [destructive]
- `cancel_meeting` — Cancel a meeting, one recurring occurrence, or the whole series after showing the meeting and obtaining user confirmation. [destructive]
- `get_meeting` — Get meeting details by meeting_id. Resolve a meeting code with get_meeting_by_code first.
- `get_meeting_by_code` — Resolve a meeting code to meeting_id and meeting details. Accept the meeting-code formats supported by Tencent Meeting.
- `get_meeting_invitees` — List invited meeting members, preserving pagination cursors.
- `get_meeting_participants` — List meeting participants. Pass next_page_token as page_token while has_more is true. Recurring meetings require sub_meeting_id; time filters apply to non-recurring meetings and cover at most 90 days.
- `get_record_addresses` — Get recording download URLs. Return the URLs without downloading the media. A permission failure does not automatically submit an access request.
- `get_records_list` — List recordings by meeting ID, meeting code, or time range. Without a meeting ID or code, supply both times; the range must not exceed 31 days or start more than one year ago.
- `get_smart_minutes` — Get AI meeting minutes, optionally translated into a supported language. Supply the recording file ID, not the meeting recording ID.
- `get_transcripts_details` — Get transcript text starting at a paragraph ID returned by get_transcripts_paragraphs. Omit limit to request all remaining paragraphs.
- `get_transcripts_paragraphs` — Get transcript paragraph identifiers for a recording file. Use get_transcripts_details to retrieve the text.
- `get_user_ended_meetings` — List ended meetings, optionally filtered by time. Use get_user_meetings separately for upcoming and ongoing meetings.
- `get_user_meetings` — List upcoming and ongoing meetings. Use get_user_ended_meetings separately for ended meetings.
- `get_waiting_room` — List members in the meeting waiting room, preserving pagination cursors.
- `list_tools` — Discover current Tencent Meeting MCP tools and their live schemas, including capabilities not exposed as dedicated actions.
- `schedule_meeting` — Schedule a normal or recurring meeting. Supply the subject and intended start/end times; omitted options use Tencent Meeting defaults. [write]
- `search_transcripts` — Search a recording transcript using the upstream text parameter. Preserve the keyword encoding required by the current tool schema.
- `update_meeting` — Update a meeting after showing the existing meeting and obtaining user confirmation. Omitted fields are left to the provider; do not supply unrelated changes. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Tencent Meeting MCP state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Tencent Meeting MCP is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/tencent_meeting_mcp
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Tencent Meeting MCP homepage: https://meeting.tencent.com/
- API documentation: https://meeting.tencent.com/support/topic/2233/index.html
