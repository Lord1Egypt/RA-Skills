---
name: oo-googlechat
description: "Google Chat (workspace.google.com). Use this skill for ANY Google Chat request — reading, creating, and updating data. Whenever a task involves Google Chat, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Google Chat"
  author: "OOMOL"
  version: "1.0.5"
  services: ["googlechat"]
  icon: "https://static.oomol.com/logo/third-party/googlechat.svg"
---

# Google Chat

Operate **Google Chat** through your OOMOL-connected account. This skill calls the `googlechat` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Google Chat. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "googlechat" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "googlechat" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_message` — Send a plain-text message to a Google Chat space, optionally as a reply inside an existing thread. Under user authentication the Chat API only accepts plain text, so cards and attachments are not supported. When thread is provided but messageReplyOption is omitted, this action sends REPLY_MESSAGE_OR_FAIL rather than the Google default, which would silently ignore the thread and start a new one. messageReplyOption only applies to named spaces (spaceType=SPACE). Reusing a requestId returns the message that was already created instead of sending a new one. [write]
- `find_direct_message` — Find the existing direct message space between the authenticated user and one other user, identified by email address or numeric user id. Use this to address a person by identity instead of by an opaque space id: a direct message space has no displayName, so list_spaces can never tell you who a DM is with. Only finds conversations that already exist; it never creates one. Caution when the result is fed to create_message: if the identifier is mistyped but still resolves to another real user this account already has a DM with, this action succeeds and returns that person's space, and the returned space id is opaque, so it cannot be eyeballed to confirm the recipient. The result therefore carries peer, the person the space actually belongs to, named by Google Chat or the Workspace directory: read it back to the user and confirm the name before sending. Nothing enforces that check. Naming the peer needs the chat.memberships.readonly and directory.readonly scopes plus the People API on top of the scope below. When the peer cannot be resolved at all (listing the members or reading your own People id failed), peer is null and peerError says why, while the space itself is still returned. A resolved peer can still be unnamed: displayName is null for an AMBIGUOUS peer, for a BOT or SELF peer Google Chat did not name, and for a HUMAN peer the directory could not name (profileUnavailableReason then says why). Treat a null peer or a null displayName as an unconfirmed recipient.
- `get_direct_message_peer` — Name the other participant of a direct message space. Under user authentication Google Chat may report a member only as users/{id}, so a name or email Chat leaves out is looked up in the Workspace directory through the People API. Use it to tell who a direct message from list_spaces is with. Rejects spaces that are not direct messages. A HUMAN peer that cannot be named still comes back with its users/{id} and a profileUnavailableReason; BOT and SELF peers carry only what Google Chat reports, and an AMBIGUOUS peer has a null user and lists its candidates.
- `get_message` — Retrieve a single Google Chat message by its resource name, or by space and message ID. A name or email Google Chat leaves out for a human sender is filled in from the Workspace directory, which needs the directory.readonly scope and the People API on top of the scope below; without them the sender keeps its users/{id} with a null displayName and a profileUnavailableReason, and the message is still returned.
- `get_space` — Retrieve the details of a single Google Chat space.
- `list_messages` — List the message history of a Google Chat space, with optional filtering, ordering, and pagination. A name or email Google Chat leaves out for a human sender is filled in from the Workspace directory, which needs the directory.readonly scope and the People API on top of the scope below; without them such a sender keeps its users/{id} with a null displayName and a profileUnavailableReason, and the messages are still returned.
- `list_space_members` — List the members of any Google Chat space, including group spaces, with each person's name and email. Like Google Chat's default, it leaves out memberships held through a Google Group and people who were invited but have not joined. Under user authentication Google Chat may report a member only as users/{id}, so every human on a page whose name or email Chat leaves out is looked up in the Workspace directory through the People API in one batch. Returns one page at a time; pass nextPageToken back as pageToken for the next page. Members whose profile cannot be read keep their users/{id} with a null displayName and a profileUnavailableReason.
- `list_spaces` — List the Google Chat spaces the authenticated user is a member of, with optional filtering and pagination.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Google Chat state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Google Chat is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/googlechat
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Google Chat homepage: https://workspace.google.com/products/chat/
- API documentation: https://developers.google.com/workspace/chat/api/reference/rest
