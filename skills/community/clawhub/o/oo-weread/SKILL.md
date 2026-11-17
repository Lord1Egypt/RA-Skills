---
name: oo-weread
description: "WeRead (weread.qq.com). Use this skill for ANY WeRead request — searching and reading data. Whenever a task involves WeRead, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "WeRead"
  author: "OOMOL"
  version: "1.0.2"
  services: ["weread"]
  icon: "https://static.oomol.com/logo/third-party/weread.png"
---

# WeRead

Operate **WeRead** through your OOMOL-connected account. This skill calls the `weread` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected WeRead. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "weread" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "weread" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_book` — Get book details by ID.
- `get_reading_progress` — Get reading progress. Progress 1 means 1%; completion requires progress 100 and finishTime.
- `get_reading_stats` — Get reading statistics for one period. Durations are seconds; annual mode covers only the selected calendar year.
- `get_review` — Get a single thought or review with optional comments and likes.
- `get_shelf` — Read the shelf. Visible entries equal books.length + albums.length + 1 when mp is nonempty; bookCount excludes audio and mp.
- `get_underline_stats` — Get chapter highlight popularity statistics without source text.
- `list_book_reviews` — List public book reviews. Continue with the last idx and returned synckey. Content is nested at reviews[].review.review.
- `list_chapters` — List a book's chapter table of contents.
- `list_highlight_reviews` — List thoughts on specified highlight ranges, preserving per-range pagination.
- `list_highlights` — List personal highlights in a book, excluding reading-position bookmarks. Query list_my_reviews as well to retrieve all exportable note content.
- `list_my_reviews` — List personal thoughts, chapter comments and book reviews. Continue with the returned synckey while hasMore is 1.
- `list_notebooks` — List notebook summaries. Next lastSort is the final book's sort. Total notes include reviewCount + noteCount + bookmarkCount.
- `list_popular_highlights` — Get up to 20 popular highlights with source text. The upstream result is fixed-size and does not support pagination.
- `list_recommendations` — List personalized book recommendations. Continue with the last book's searchIdx as maxIdx.
- `list_similar_books` — List similar books. Defaults to count 12 and maxIdx 0; continue with the last idx and returned sessionId.
- `search` — Search WeRead. Choose scope explicitly; use the last searchIdx as maxIdx for the next page. Response group scope may differ from request scope.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change WeRead state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — WeRead is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/weread
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- WeRead homepage: https://weread.qq.com/
- API documentation: https://github.com/Tencent/WeChatReading/tree/main/skills
