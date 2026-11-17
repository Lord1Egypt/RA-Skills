---
name: oo-mymind
description: "mymind (mymind.com). Use this skill for ANY mymind request — reading, creating, updating, and deleting data. Whenever a task involves mymind, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "mymind"
  author: "OOMOL"
  version: "1.0.6"
  services: ["mymind"]
  icon: "https://static.oomol.com/logo/third-party/mymind.svg"
---

# mymind

Operate **mymind** through your OOMOL-connected account. This skill calls the `mymind` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected mymind. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "mymind" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "mymind" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_object_tags` — Add tags to a mymind object. [write]
- `add_object_to_space` — Put a mymind object into a space. [write]
- `create_link` — Link one mymind object to another. [write]
- `create_note` — Create a note in a mind from markdown content. [write]
- `create_object_note` — Attach a markdown note to a mymind object. [write]
- `create_space` — Create a mymind space, optionally seeded with objects. [write]
- `delete_link` — Delete a manual link. A wiki-style link cannot be deleted directly; remove the reference from the source note instead. [destructive]
- `delete_object` — Soft-delete a mymind object. Use restore_object to bring it back. [destructive]
- `delete_object_note` — Delete a note attached to a mymind object. [destructive]
- `delete_space` — Delete a mymind space. The objects it held stay in the mind. [destructive]
- `get_object` — Get one mymind object with its title, summary, tags, spaces, notes, and source.
- `get_object_content` — Get the content body of a mymind object as markdown. Many objects are saved without an inline body — a bookmark or an image is the whole object — and those come back empty rather than as an error.
- `get_space` — Get one mymind space and the objects it holds.
- `list_links` — List the links between objects in a mind, both wiki-style references and manual links.
- `list_objects` — List objects in a mind, optionally narrowed to a text query, a space, specific identifiers, or objects similar to one you already have.
- `list_spaces` — List the spaces in a mind. The objects in each space are returned by get_space.
- `list_tags` — List the tags in a mind, most recently used first.
- `pin_object` — Pin a mymind object, optionally into a specific slot. [write]
- `remove_object_from_space` — Take a mymind object out of a space. The object stays in the mind. [destructive]
- `remove_object_tags` — Remove tags from a mymind object. [destructive]
- `restore_object` — Restore a soft-deleted mymind object. [write]
- `save_url` — Save a URL to a mind. mymind fetches the page itself and fills in the title, summary, tags, and screenshot. [write]
- `search_objects` — Search a mind and return the matching objects with their relevance scores. Supports keyword syntax (quoted phrases, && || -, wildcards, and field filters such as tag:, type:, domain:, created:) and, with semantic enabled, matching by meaning rather than exact terms.
- `unpin_object` — Unpin a mymind object. [destructive]
- `update_object` — Update the title, summary, or completed state of a mymind object. [write]
- `update_object_content` — Replace the content body of a mymind object with markdown. [destructive]
- `update_object_note` — Replace the body of a note attached to a mymind object. [destructive]
- `update_space` — Rename a mymind space or change its colour. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change mymind state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — mymind is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/mymind
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- mymind homepage: https://mymind.com
