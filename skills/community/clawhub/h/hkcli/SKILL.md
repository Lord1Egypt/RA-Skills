---
name: hkcli
description: "Read, search and send Hike Messenger chats via the hkcli command-line tool. Use when the user asks about their Hike messages or wants to message someone on Hike."
homepage: https://vinaycodeaxe.github.io/hkcli/
metadata:
  openclaw:
    emoji: "💬"
    homepage: https://vinaycodeaxe.github.io/hkcli/
    requires:
      bins:
        - hkcli
    install:
      - id: go
        kind: go
        module: github.com/vinaycodeaxe/hkcli/cmd/hkcli@latest
        bins:
          - hkcli
        label: Install hkcli (go)
---

# hkcli

Use `hkcli` when the user asks you to read, search or summarize their Hike chats,
or to send someone a message or file on Hike.
This skill uses the Hike account hkcli is logged in to (by default the store `~/.hkcli`, usually
the user's own account) and only touches Hike when the user asks. It is separate from the Hike
channel plugin, through which people chat with you on your own Hike number; never point hkcli
at that channel's store (`~/.openclaw/hike/...`).

## Safety

- Sending needs an explicit recipient and message text from the user. Do not invent or rewrite the text without showing it.
- Before sending, show the resolved recipient (name and id) and the exact text, and wait for the user to confirm.
- If a name matches several chats or anything is unclear, ask instead of guessing.
- Use `--read-only` when you only need to read. It blocks anything that sends to Hike or changes saved data.
- Never print, copy or upload `~/.hkcli/session.json` (it is the login). Do not run `hkcli auth logout` unless asked.
- Messages are private. Quote only what the user needs.

## Login (the user does this)

Login needs the user's phone, so ask the user to run it in a terminal on this machine:

- `hkcli auth`, then scan the QR code in the Hike app: Settings > Web QR Login.
- Headless machine: `hkcli auth --qr-format png` (saves an image), `--qr-format text`,
  or `hkcli auth --phone +<country code><number>` for an SMS code.
- Check: `hkcli auth status --json`. Exit code 3 from any command means the login is missing or expired.

## Gotchas

- Logging this number out of the Hike app, or switching the app to another number, ends hkcli's
  login too: commands exit with code 3. Ask the user to log in again; do not retry in a loop.
- Hike sends only a few SMS codes per number. After `OTP send limit reached`, tell the user to try
  again later (for example the next day) instead of starting another SMS login.

## Fresh data

- `hkcli sync --once` catches up. Run it before reading if results might be stale.
- If it fails with `store_locked`, a background `hkcli sync` is already keeping data fresh; just read.

## Find chats and messages

- `hkcli chats list --json --limit 20` (filters: `--unread`, `--groups`, `--direct`, `--query "name or number"`)
- `hkcli messages list --chat "<name|+phone|id>" --limit 30 --json`
- `hkcli messages search "words" --limit 20 --json` (add `--chat ...`; end a word with `*` to match prefixes)
- `hkcli messages show --chat <chat id> --id <message id> --json`
- Older history: `hkcli history backfill --chat <chat id> --pages 5`

## Send (only after the user confirms)

- Text: `hkcli send text --to "<name|+phone|id>" --message "Running 10 min late"`
- Multiline: pipe the text in with `--message -`, for example
  `printf 'line one\nline two' | hkcli send text --to <id> --message -`
- Reply: add `--reply-to <message id>`
- File: `hkcli send file --to <id> --file /path/report.pdf --caption "Report"`
- Tell the user the returned message id. If hkcli says Hike did not confirm, do not resend on your own: the message may have gone through, so ask the user.

## Other commands

- Contacts: `hkcli contacts list --query "asha" --json`
- Groups: `hkcli groups list --json`, `hkcli groups info --group "<name|id>" --json`
- Media: `hkcli media download --chat <chat id> --id <message id> --out <folder>`
- Mark read: `hkcli chats mark-read --chat <chat id>` (sends a read receipt; only when asked)
- Health: `hkcli doctor --json` (add `--connect` to test the live connection)

## Notes

- `--to`, `--chat` and `--group` accept an id, a phone number with country code, or a unique name.
  When a name is ambiguous, take the id from `chats list --json`.
- Message ids look like `20:1760000001000` (from Hike) or a UUID (just sent, not yet confirmed).
- `--json` prints `{"success", "data", "error"}`. Errors carry `error.code`, for example
  `auth_required`, `ambiguous`, `not_found`, `read_only` or `store_locked`. `relay_unavailable`
  means nothing was sent and you can retry; after `relay_error` the message may have gone out, so
  check `messages list` before sending again.
- Store: `~/.hkcli` (override with `--store` or `HKCLI_STORE`); one store per Hike account.
- hkcli is unofficial. If Hike changes its servers, commands can fail until hkcli is updated.
- Docs: https://vinaycodeaxe.github.io/hkcli/
