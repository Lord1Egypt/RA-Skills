---
name: helmet
version: 0.3.1
description: Manage your Helmet library accounts (Helsinki capital region) from an AI agent — renew loans, place and cancel holds, view fines, and search the catalog across one card or a whole family at once.
metadata:
  openclaw:
    requires:
      bins:
        - helmet
      configPaths:
        - ~/.config/helmet/config.json
    install:
      - id: node
        kind: node
        package: "@helmet-ai/helmet"
        bins:
          - helmet
        label: Install Helmet CLI (npm)
    credentials:
      note: >-
        Requires ~/.config/helmet/config.json created by running
        `helmet login` interactively once per library card. Stores library
        card number and PIN for each saved profile.
---

# Helmet Library Skill

Access the **Helmet library system** (Helsinki Metropolitan Area libraries) from an AI agent. Query loans, renew books, check holds and fines — for one account or many family accounts at once, via the `helmet` CLI with `--json` output.

## What you can ask your agent

- "Is anything overdue for me or the kids at the library?"
- "Renew everything that's due this week."
- "How many holds do I have, and which are ready for pickup?"
- "Place a hold on *Dog Man Scarlet Shedder*."
- "Cancel my hold on the Finnish language audiobook."
- "Do I owe any fines right now?"
- "Search the Helmet catalog for 'Tove Jansson'."

## Quick Start

```bash
# Install
npm install -g @helmet-ai/helmet

# First-time login — run once per library card (saves credentials locally)
helmet login

# Full account overview (single account)
helmet summary --json

# Family overview (all saved profiles)
helmet summary --all-profiles --json
```

### Preflight (recommended before bulk queries)

```bash
helmet status --json
helmet status --all-profiles --json
```

Verifies each saved profile's session is live. Exit code `0` means authenticated; `2` means the user needs to run `helmet login`. Run this once at the start of a multi-step task to avoid partial failures halfway through.

## Profiles

The CLI stores one or more library accounts as *profiles*. Use these when acting for a user or a family:

- **One profile saved** — commands run against it by default.
- **Multiple profiles saved** — commands run against the last-used profile unless you pass `--profile` or `--all-profiles`.

### Profile selection flags

| Flag | Purpose |
|------|---------|
| `--profile <selector>` | Target one profile. Selector is any of: display name (`Alice`), unique display-name prefix (`al`), card number, or full id (`helmet\|<card>`). |
| `--all-profiles` | Fan out across every saved profile. Works on `summary` and `loans list`. Mutually exclusive with `--profile`. |

`--all-profiles` is **not** supported on `loans renew`, `holds place`, `holds cancel` (all destructive — always target one profile), `search` (unauthenticated), or `login`.

### Fan-out JSON shape

`--all-profiles --json` wraps output in a per-profile array. Each row is independent: one profile failing does not block others.

```json
[
  {"profile": {"id": "helmet|...", "displayName": "Alice"}, "ok": true,  "data": { /* same shape as single-profile --json */ }},
  {"profile": {"id": "helmet|...", "displayName": "Bob"},   "ok": false, "error": "AuthenticationError: ...", "errorCode": "AUTH_REQUIRED"}
]
```

Exit code is `0` if at least one profile succeeded, `1` if all failed. When reporting partial failures to the user, key on `errorCode` (stable) rather than the free-form `error` string (which embeds the raw exception message).

### `helmet profiles list --json`

Enumerate saved profiles. Returns `id`, `displayName`, `cardNumber`, and `lastUsedAt` for each.

### `helmet profiles rename <selector> <new-name>` / `helmet profiles remove <selector>`

Local-only management of saved profiles (no Helmet API calls).

## Session cache

Each profile's authenticated cookie jar is persisted at `~/.config/helmet/sessions/<id>.json` (mode 0600). The first command per profile walks the full Finna login handshake (~2.7s); subsequent commands skip straight to the data request (~1.3s). Stale cookies are handled transparently — if Finna redirects to the login page, the session auto-re-authenticates using the stored PIN. You do not need to manage the cache explicitly; it is cleared automatically on `helmet login`, `helmet profiles remove`, or an unrecoverable `AuthenticationError`.

## Commands

All commands accept `--json` for machine-readable output. Always use `--json` when calling from an agent.

### `helmet summary --json`

Returns a complete account snapshot: loans (with overdue/due-soon flags), holds (with pickup-ready status), and fines. **Start here** — one call gives you everything needed for triage. Add `--profile <selector>` for a specific person or `--all-profiles` for a whole family.

### `helmet loans list --json`

List checked-out items with title, author, due date, due status (`ok`, `due`, `overdue`), and whether renewable. Supports `--profile` and `--all-profiles`.

### `helmet loans renew <id> --json`

Renew a specific loan by its ID. Returns success/failure with new due date or error code. **Requires** `--profile <selector>` when multiple profiles exist (the CLI will not auto-pick a profile for destructive operations).

### `helmet loans renew --all --json`

Renew every renewable item on one profile. Same profile-targeting rule as above — pass `--profile <selector>` explicitly.

### `helmet holds list --json`

List current holds. `helmet holds` (no subcommand) is an alias. Each row has shape:

```json
{
  "id": "12345678",
  "title": "Sample Book Title",
  "author": "Last, First",
  "pickupLocation": "Sample Branch",
  "queuePosition": null,
  "pickupDeadline": "15.1.2026",
  "createdDate": "1.1.2026",
  "shelfLocation": "A 000",
  "status": "available_for_pickup",
  "cancelable": true,
  "fetchedAt": "2026-01-01T12:00:00.000Z"
}
```

Field meanings:
- `status`: `"pending"` (in queue) / `"in_transit"` (on its way to the pickup branch) / `"available_for_pickup"` (arrived — the user must go collect it).
- `pickupDeadline` (Finnish "nouto viimeistään"): the date the hold will be cancelled and passed to the next patron if uncollected. **Only populated when `status === "available_for_pickup"`** — `null` otherwise. Date is in Finnish format `D.M.YYYY`. **If the user misses this date, Helmet charges a no-pickup fee and may suspend borrowing for a period** — agents should surface this date prominently in reminders.
- `shelfLocation` (Finnish "Varaushylly"): the exact shelf code inside the branch where the arrived hold is waiting (e.g. `A 000`). Only populated for arrived holds. Include it in pickup reminders so the user can walk straight to the shelf.
- `createdDate` (Finnish "Luotu"): when the hold was placed. Informational, not actionable.
- `queuePosition`: for pending holds, the user's position in the reservation queue (`null` once the hold is in transit or arrived).

### `helmet holds place <record-id> [--comment <text>] --json`

Place a title-level hold on a Helmet catalog record. The `record-id` comes from `helmet search` (e.g. `helmet.2613471`). The CLI uses the default pickup location preselected by Helmet in the hold form. The `--comment` field is used only for bookmobile pickup stops. Returns `{ success, message }`; on success, message is typically `"Varauspyyntö onnistui."`. **Requires** `--profile <selector>` when multiple profiles exist — the CLI will not auto-pick a profile for a destructive/state-changing operation.

### `helmet holds cancel <hold-id> --json`

Cancel an active hold. The `hold-id` is the `id` field from `helmet holds list --json`. Returns `{ success, message }`; on success, message is typically `"1 varaus(ta) poistettu."`. Same profile-targeting rule as `place` — pass `--profile <selector>` explicitly.

### `helmet fines --json`

List individual fines and total amount owed.

### `helmet search <query> --json`

Search the Helmet catalog. Unauthenticated — `--profile` has no effect and `--all-profiles` is rejected.

### `helmet status [--json] [--all-profiles]`

Lightweight preflight: reports whether the selected profile (or all profiles) has a live authenticated session. Exit code `0` if authenticated, `2` if `helmet login` is needed. With `--json`:

```json
{
  "version": "0.3.0",
  "profile": {"id": "helmet|...", "displayName": "Alice"},
  "authenticated": true,
  "checkedAt": "2026-04-14T12:34:56Z"
}
```

On `--all-profiles`, emits `{version, checkedAt, profiles: [...]}` where each row carries `authenticated: bool` and, on failure, `errorCode: "AUTH_REQUIRED"`. Run this before multi-step tasks.

### `helmet version` / `helmet --version` / `helmet -V`

Print the CLI version (e.g. `0.3.0`). No auth, no network. Useful when an agent needs to record which helmet build produced a report.

## Handling authentication errors

When the stored session expires, the PIN has changed, or Finna invalidates the session for any reason, `helmet` exits with **code 2** and (with `--json`) emits:

```json
{
  "ok": false,
  "errorCode": "AUTH_REQUIRED",
  "errorName": "AuthenticationError",
  "message": "Helmet session expired and re-authentication failed — run `helmet login` to refresh credentials.",
  "recovery": "Run `helmet login` to refresh your library credentials."
}
```

On `--all-profiles`, one row may fail with `errorCode: "AUTH_REQUIRED"` while others succeed. Report the affected person by `displayName` and continue with the rest.

### Agent recovery procedure

1. **Detect** — check the exit code (2 = auth) or the `errorCode: "AUTH_REQUIRED"` field in the JSON output.
2. **Report** — tell the user which profile(s) need re-authentication, referring to them by `displayName` (not card number).
3. **Do NOT run `helmet login` yourself.** It is interactive and prompts for a PIN that only the user knows. Ask the user to run `helmet login` locally.
4. **Retry** the original command after the user confirms they've re-logged in. The CLI's stale session cache is cleared automatically when auth fails, so the retry will attempt a fresh login.
5. **Do NOT loop.** If the retry still returns `AUTH_REQUIRED`, stop and ask the user — do not keep retrying. The most likely cause is a changed PIN that the stored credential no longer matches, which only a fresh `helmet login` can fix.

## Triage Guidance

When reporting to the user, prioritize items by actionability:

| Priority | Condition | Action |
|----------|-----------|--------|
| URGENT | Overdue items (`dueStatus: "overdue"`) | Renew immediately or alert user |
| URGENT | Fines > 0 EUR | Alert user — fines block borrowing |
| URGENT | Ready-for-pickup hold whose `pickupDeadline` is today, tomorrow, or in the past | Alert user to collect **today** — missing the deadline cancels the hold and charges a no-pickup fee |
| HIGH | Loans due within 3 days (`dueStatus: "due"` or in `loansDueSoon`) | Renew if possible, otherwise warn |
| HIGH | Ready-for-pickup hold (`status: "available_for_pickup"`) with `pickupDeadline` within 7 days | Remind user to pick up. Always cite the exact deadline date and the `shelfLocation` so they can go straight to the shelf at `pickupLocation`. |
| MEDIUM | Loans due within 7 days | Mention in summary |
| LOW | Holds with queue position ≤ 2 | Mention — pickup may come soon |

### Formatting hold reminders for users

When surfacing a ready-for-pickup hold, prefer a line like:

> *"Pick up **Sample Book Title** at **Sample Branch** (shelf **A 000**) by **15.1.2026** — otherwise the hold is cancelled and a no-pickup fee applies."*

Always include: title, `pickupLocation`, `shelfLocation` (when present), and `pickupDeadline`. Dates are already in Finnish `D.M.YYYY` format — keep them as-is; do not reformat to ISO unless the user is clearly a developer consuming JSON.

### Recommended workflow (single person)

1. Run `helmet summary --json` (or with `--profile <name>`).
2. Check for URGENT items first — auto-renew overdue loans if renewable.
3. Surface HIGH items prominently.
4. Mention MEDIUM/LOW items briefly.
5. If renewals fail, include the error code in your report.

### Recommended workflow (family)

1. Run `helmet summary --all-profiles --json` — one call covers everyone.
2. Flatten rows where `ok: true`. For each `ok: false` row, mention the person's name and that their data could not be fetched (don't abort the whole report).
3. Group findings **by urgency first, by person second** — one overdue book across any family member is more actionable than "here is Alice's summary, here is Bob's summary".
4. For renewals, issue one `helmet loans renew --all --profile <name>` per person that has renewable overdue loans. **Never fan out renew.**
5. Prefer referring to people by `displayName` in user-facing output; keep `id` for internal routing.

## Scripts

The wrapper script at `scripts/helmet-cli.sh` can be used as a fallback when the `helmet` binary is not on PATH:

```bash
bash skills/helmet/scripts/helmet-cli.sh summary --all-profiles --json
```

## Troubleshooting

**Empty `holds` / `loans` / `fines` arrays with no error** — this was a bug in **helmet ≤ 0.1.1** where an expired session was parsed as "no data" instead of raising an auth error. Upgrade to 0.2.0+:

```bash
npm install -g @helmet-ai/helmet@latest
helmet --version   # must be ≥ 0.2.0
```

If you still see empty results after upgrading, run `helmet status --json` — if it reports `authenticated: false`, the user needs to run `helmet login`. Real empty results (no holds, no loans) after 0.2.0 are legitimate; only pre-0.2.0 masked auth failures as empty.
