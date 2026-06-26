---
name: imap-client
description: 'Read, search, and download email over IMAP from the command line using the `myl` CLI client. Use this skill whenever the user wants to interact with their mailbox from a terminal — checking the inbox, listing or searching messages, reading a specific email, opening HTML or raw source, or saving attachments. Trigger on any of these cues even when `myl` is not named explicitly — "check my email", "look in my inbox", "search my mail for X", "find the email from Y", "download the attachment", "is there an email about Z", "read the latest message", "show me unread", "connect to my IMAP server", "imap.gmail.com", "imap.yandex.com", "imap.yandex.ru", "imap.mail.ru", "imap.fastmail.com", "Yandex Mail", "Mail.ru", "Gmail IMAP", "проверить почту", "новые письма", "найти письмо", and similar. Also trigger when the user asks to script or automate any of the above. Do not trigger for outgoing mail (sending, SMTP, drafting) — `myl` is read-only — or for desktop/GUI mail clients.'
license: MIT
homepage: https://github.com/codd-tech/imap-client
metadata: {"openclaw":{"emoji":"📬","requires":{"bins":["myl"],"env":["IMAP_USER","IMAP_PASSWORD"]},"primaryEnv":"IMAP_PASSWORD","install":[{"id":"pipx","kind":"pipx","package":"myl","bins":["myl"],"label":"Install myl via pipx"}]}}
---

# imap-client

Read mailboxes over IMAP from the terminal using `myl`, a small Python CLI client. Maintained and distributed by [codd-tech](https://github.com/codd-tech/imap-client). Designed to drop into [OpenClaw](https://openclaw.ai) and any other AgentSkills-compatible runtime (Claude Code, generic).

`myl` is read-only and intentionally minimal: it lists, searches, and fetches messages and attachments. It does not send mail, manage folders, or modify state beyond optionally marking messages as seen.

## How credentials reach this skill

This is the most important section. **You do not type passwords on the command line.** Credentials live in environment variables that the runtime injects per agent run. The skill reads them and assembles the right `myl` flags through the wrapper at `{baseDir}/scripts/imap.sh`.

The variables the wrapper expects:

| Variable | Required | Purpose |
|---|---|---|
| `IMAP_USER` | yes | Login (usually full email address) |
| `IMAP_PASSWORD` | yes | App-specific password (see `references/authentication.md`) |
| `IMAP_PROVIDER` | no | One of `auto` (default), `gmail`, `yandex`, `mailru`, `manual` |
| `IMAP_SERVER` | only with `manual` | IMAP host |
| `IMAP_PORT` | no | Defaults to 993 |
| `IMAP_STARTTLS` | no | `1` to add `--starttls` (use only with port 143) |

**Set them once, use them every session.** How depends on the runtime — `references/authentication.md` covers OpenClaw's `skills.entries.imap-client.env`, generic shell `export`, and a `~/.config/imap-client/credentials` fallback file. Do not invent your own scheme; use one of those three.

If the wrapper detects `IMAP_USER` or `IMAP_PASSWORD` is missing, it prints the setup instructions and exits without contacting any server. That's the signal to stop and walk the user through credential setup before retrying.

## Workflow at a glance

1. **Check that `myl` is installed.** OpenClaw gates this skill on `requires.bins: ["myl"]`, so it shouldn't load without it. For non-OpenClaw runtimes, run `bash {baseDir}/scripts/check_myl.sh`. If missing, follow `references/installation.md`.
2. **Confirm credentials are configured.** Run `bash {baseDir}/scripts/imap.sh --count 1 >/dev/null` once. Success means the env vars are wired and the connection works. Failure means walk the user through `references/authentication.md`.
3. **Run the requested operation** through the wrapper. Listing, searching, fetching by ID, getting HTML, saving raw `.eml`, or pulling an attachment.
4. **Summarise the result.** Don't dump full raw email bodies into the chat unless the user asked.

Every `myl` example in this skill goes through `{baseDir}/scripts/imap.sh`, which expands env vars into the right `myl` flags. You do not need to remember `--google` vs `--auto` vs `--server`/`--port`; the wrapper picks based on `IMAP_PROVIDER`.

## When to read what

| Task involves… | Read |
|---|---|
| Detecting or installing `myl`, OpenClaw `requires.bins` gating | `references/installation.md` |
| Setting up credentials, choosing connection mode, app passwords for Gmail / Yandex / Mail.ru / iCloud / Fastmail | `references/authentication.md` |
| Any specific CLI flag, listing, searching, fetching, attachments, provider-specific folder names | `references/operations.md` |
| Multi-step recipes (e.g. "find the invoice from Acme last month and save the PDF") | `references/recipes.md` |
| Errors like SSL failures, "command not found", autodiscovery failing, "AUTHENTICATIONFAILED", env vars not visible to the wrapper | `references/troubleshooting.md` |

## Principles

### 1. Credentials must not appear in agent-generated commands or logs

**Do not** generate commands like `myl --password hunter2` or `myl --password "$IMAP_PASSWORD"` directly — the first hardcodes the secret in shell history and conversation logs; the second exposes it there too and adds no benefit over the wrapper. Always use the wrapper:

```bash
bash {baseDir}/scripts/imap.sh --count 5
```

The wrapper reads credentials from env vars and passes them to `myl` via `--username`/`--password` flags. This means the password **is** briefly visible in `/proc/<pid>/cmdline` and `ps` output to other processes on the same host while `myl` runs — the same exposure as running `myl` directly with env-var expansion. The wrapper's benefit is narrower: the password value never appears in commands the agent generates, in shell history, or in conversation logs. On shared or multi-user machines this argv exposure should be understood as a residual risk.

### 2. Default to small result sets

When the user's intent is exploratory ("any new mail?"), pass `--count 5` or `--count 10`. Only fetch larger windows on explicit request. This keeps output readable and avoids dumping sensitive content the user didn't ask to see.

### 3. Don't mark as seen by accident

`--mark-seen` mutates state on the server. Only pass it when the user explicitly asked to mark messages read. Listing or reading without this flag is non-destructive.

### 4. Render long bodies to a file, summarise in chat

When the user fetches a long message or HTML email, save the raw output to a file (e.g. `/tmp/email-<id>.eml` or `.html`) and give the user a 2–4 sentence summary plus the file path. Do not paste a 500-line HTML body into the conversation.

### 5. Search syntax is server-side IMAP, not Gmail's web UI

`--search "important"` issues an IMAP `SEARCH` command. It does not understand Gmail's `from:`, `has:attachment`, or `label:` operators. For complex filtering, fetch a reasonable window with `--count` and filter the listing locally. See `references/operations.md` for what IMAP `SEARCH` supports.

### 6. Never echo, summarise, or persist the password

When summarising what you did, refer to the credential as `IMAP_PASSWORD` or "the password from your OpenClaw config", never the literal value. If the user pastes a password into chat by mistake, treat it as compromised: tell them to rotate it and update their config. Do not write it to any artifact.

## Quick decision tree

```
User asked something email-related from the CLI
  │
  ├─ Is `myl` installed and on PATH?  ── No  ──► references/installation.md
  │   │
  │   Yes
  │   ▼
  ├─ Does the wrapper smoke-test pass?
  │     bash {baseDir}/scripts/imap.sh --count 1 >/dev/null
  │   │                       No  ──► references/authentication.md
  │   Yes
  │   ▼
  ├─ What does the user want?
  │   ├─ Browse / list           ──► imap.sh --count N [--folder F]
  │   ├─ Search                  ──► imap.sh --search "TERM" [--count N]
  │   ├─ Read one message        ──► imap.sh "$MAILID"
  │   ├─ Read HTML version       ──► imap.sh --html "$MAILID"  → save to file
  │   ├─ Save raw .eml           ──► imap.sh --raw "$MAILID" > file.eml
  │   ├─ Get attachment          ──► imap.sh "$MAILID" "$ATT_NAME" > file
  │   └─ Anything multi-step     ──► references/recipes.md
  │
  └─ Errors? ─────────────────────► references/troubleshooting.md
```

## Output style

After running the wrapper, present results in this shape:

- **One-line status** of what just ran (e.g. "Listed the 10 most recent messages in INBOX").
- **A compact table or bullet list** of message metadata (date, from, subject, ID).
- **Any file paths** where larger output was saved.
- **Suggested next actions** (e.g. "Want me to open #4582 or save its attachments?").

Keep it scannable.

