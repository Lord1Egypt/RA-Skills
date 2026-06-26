---
name: oo-trello
description: "Trello (trello.com). Use this skill for ANY Trello request — reading, creating, updating, and deleting data. Whenever a task involves Trello, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Trello"
  author: "OOMOL"
  version: "1.0.1"
  services: ["trello"]
  icon: "https://static.oomol.com/logo/third-party/trello.svg"
---

# Trello

Operate **Trello** through your OOMOL-connected account. This skill calls the `trello` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Trello. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "trello" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "trello" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_card_attachment_url` — Attach an external URL to a Trello card. [write]
- `add_card_comment` — Add a comment action to a Trello card. [write]
- `add_card_label` — Add a Trello label to a card. [write]
- `add_card_member` — Assign a Trello member to a card. [write]
- `add_checkitem` — Add a check item to a Trello checklist. [write]
- `archive_card` — Archive a Trello card. [write]
- `archive_list` — Archive a Trello list. [write]
- `create_board` — Create a Trello board. [write]
- `create_card` — Create a Trello card in a list. [write]
- `create_checklist` — Create a Trello checklist on a card. [write]
- `create_list` — Create a Trello list on a board. [write]
- `get_board` — Get a Trello board by ID.
- `get_card` — Get a Trello card by ID or short link.
- `get_member` — Get a Trello member, defaulting to the authenticated member.
- `list_board_cards` — List Trello cards on a board.
- `list_board_labels` — List Trello labels on a board.
- `list_board_lists` — List Trello lists on a board.
- `list_board_members` — List Trello members on a board.
- `list_card_checklists` — List Trello checklists on a card.
- `list_card_comments` — List comment actions on a Trello card.
- `list_member_boards` — List Trello boards visible to a member.
- `move_card` — Move a Trello card to another list. [write]
- `remove_card_label` — Remove a Trello label from a card. [destructive]
- `remove_card_member` — Remove a Trello member from a card. [destructive]
- `search` — Search Trello cards, boards, members, and organizations.
- `update_card` — Update a Trello card by ID or short link. [write]
- `update_checkitem_state` — Update a Trello check item state on a card. [write]
- `update_list` — Update a Trello list name or position. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Trello state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Trello is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/app-connections?provider=trello
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Trello homepage: https://trello.com
