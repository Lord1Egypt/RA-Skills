# Operations reference

All examples use the wrapper at `scripts/imap.sh`. The wrapper reads `IMAP_USER` / `IMAP_PASSWORD` / `IMAP_PROVIDER` from the environment (set up via `references/authentication.md`) and forwards everything else to `myl`.

If the user has aliased the wrapper, replace `bash scripts/imap.sh` with the alias name. A typical setup:

```bash
alias imap='bash ~/.openclaw/skills/imap-client/scripts/imap.sh'
```

…and then `imap --count 5` is enough.

## Listing messages

```bash
# Most recent N messages in INBOX (default folder)
bash scripts/imap.sh --count 10

# Specific folder
bash scripts/imap.sh --folder "INBOX/Archive" --count 20

# When --folder is omitted, myl operates on INBOX. To discover what folders
# exist, run a list against INBOX first; some myl versions surface folder
# listings in the output, others require the `--list-folders` flag if
# present in your version.
```

### Folder names by provider

Folder naming differs per server. When the user names a folder casually ("sent items", "spam", "корзина"), translate to the IMAP path the server expects.

| Provider | Inbox | Sent | Drafts | Archive | Trash | Spam |
|---|---|---|---|---|---|---|
| Gmail | `INBOX` | `[Gmail]/Sent Mail` | `[Gmail]/Drafts` | `[Gmail]/All Mail` | `[Gmail]/Trash` | `[Gmail]/Spam` |
| Yandex | `INBOX` | `Sent` (alias for `Отправленные`) | `Drafts` | n/a | `Trash` | `Spam` |
| Mail.ru | `INBOX` | `Sent` | `Drafts` | `Archive` | `Trash` | `Spam` |
| Fastmail | `INBOX` | `Sent` | `Drafts` | `Archive` | `Trash` | `Junk Mail` |
| iCloud | `INBOX` | `Sent Messages` | `Drafts` | `Archive` | `Deleted Messages` | `Junk` |
| Generic Dovecot | `INBOX` | `Sent` | `Drafts` | (configurable) | `Trash` | `Junk` |

Notes on Russian providers:

- **Yandex** publishes both English (`Sent`, `Drafts`, `Trash`) and Russian (`Отправленные`, `Черновики`, `Удалённые`) folder names; the English ones are aliases that always work, so prefer those.
- **Mail.ru** uses English internal folder names over IMAP, even when the web UI shows Russian labels.
- If a custom folder uses Cyrillic, it may be encoded in modified UTF-7 over IMAP. Pass the **exact string `myl` shows in listings**, not what you see in the web client.

If the first folder guess fails, list the available folders by running with no `--folder` and inspect the output; do not guess repeatedly.

## Searching

`myl --search` issues an IMAP `SEARCH` command. The argument is interpreted by the server, not by `myl`.

```bash
# Match against subject + body (default for most servers)
bash scripts/imap.sh --search "invoice"

# Combine with folder + count
bash scripts/imap.sh --folder "INBOX" --search "Acme" --count 50
```

### What IMAP SEARCH actually supports

Standard IMAP `SEARCH` keys (RFC 3501). Widely supported:

| Key | Meaning | Example |
|---|---|---|
| `FROM "x"` | sender contains x | `FROM "noreply@github.com"` |
| `TO "x"` | recipient contains x | `TO "alice@example.com"` |
| `SUBJECT "x"` | subject contains x | `SUBJECT "invoice"` |
| `BODY "x"` | body contains x | `BODY "API key"` |
| `TEXT "x"` | header or body contains x | `TEXT "kubernetes"` |
| `SINCE 1-Jan-2026` | received on or after date | `SINCE 1-Apr-2026` |
| `BEFORE 1-Apr-2026` | received before date | `BEFORE 1-May-2026` |
| `UNSEEN` | not yet marked read | `UNSEEN` |
| `SEEN` | already read | |
| `FLAGGED` | starred / flagged | |
| `LARGER 10000000` | size in bytes | `LARGER 5000000` |

In practice, the safe approaches are:

1. Pass a single keyword or short phrase: `--search "invoice"`. The server treats this as `TEXT "invoice"`.
2. For complex filters, fetch a reasonable window and post-process locally with `grep` / `awk` / a small Python helper.

What `myl --search` does **not** understand:

- Gmail's web UI operators: `from:`, `has:attachment`, `label:`, `older_than:` — these are Gmail-specific and not part of IMAP SEARCH.
- Yandex's web search syntax (e.g. `from:`, `subject:`) — also web-only.
- Boolean operators like `AND` / `OR` / `NOT` directly in the string. IMAP supports them but with different syntax.

### Cyrillic search terms

Yandex and Mail.ru both support searching for Cyrillic text via IMAP, but the term must be sent in the right charset. `myl` typically forwards the argument as-is and lets the server figure it out:

```bash
bash scripts/imap.sh --search "счёт" --count 20
```

If the server returns no results for a Cyrillic term you know exists, retry with the Latin transliteration of the company name (since most senders include both in subject lines).

## Reading a specific message

Each listing shows a per-folder message ID. Fetch it by passing the ID as a positional argument:

```bash
bash scripts/imap.sh "$MAILID"           # plain text body
bash scripts/imap.sh --html "$MAILID"    # HTML body (if present)
bash scripts/imap.sh --raw "$MAILID"     # full raw RFC 5322 source, including headers
```

For HTML and raw, redirect to a file rather than dumping into the terminal:

```bash
bash scripts/imap.sh --html "$MAILID" > "/tmp/mail-${MAILID}.html"
bash scripts/imap.sh --raw  "$MAILID" > "/tmp/mail-${MAILID}.eml"
```

Tell the user the file path and offer to open or summarise it.

## Marking as seen

```bash
bash scripts/imap.sh --mark-seen --count 10
```

Mutates server state. Only use when the user explicitly asked to mark messages read. Never combine `--mark-seen` with a search / list that the user is just exploring.

## Attachments

```bash
# 1. Open the message — myl shows attachment names in the message detail
bash scripts/imap.sh "$MAILID"

# 2. Fetch a specific attachment by name
bash scripts/imap.sh "$MAILID" "invoice-2026-04.pdf" > ~/Downloads/invoice-2026-04.pdf
```

The second positional argument after `$MAILID` is the attachment filename. Output goes to stdout, so always redirect to a file.

If the attachment name has spaces or special characters, quote it:

```bash
bash scripts/imap.sh "$MAILID" "Q1 report.pdf" > "$HOME/Downloads/Q1 report.pdf"
```

Cyrillic attachment names work but the underlying IMAP encoding (RFC 2047 / RFC 2231) varies. If the literal Cyrillic name doesn't match, retry with the encoded form `myl` showed in the message detail.

## Full flag reference

From the upstream README (`https://github.com/pschmitt/myl`). All of these forward through the wrapper:

| Flag | Purpose |
|---|---|
| `--server HOST` | IMAP server hostname (set via `IMAP_SERVER` env) |
| `--port N` | IMAP server port (set via `IMAP_PORT` env; default 993) |
| `--starttls` | Upgrade plain connection to TLS (set via `IMAP_STARTTLS=1`) |
| `--auto` | Autodiscover server + port (set via `IMAP_PROVIDER=auto`) |
| `--google` | Hardcode Gmail's IMAP settings (set via `IMAP_PROVIDER=gmail`) |
| `--username USER` | Login username (set via `IMAP_USER`) |
| `--password PASS` | Login password (set via `IMAP_PASSWORD`) |
| `--folder NAME` | IMAP folder to operate on (default `INBOX`) |
| `--count N` | Number of messages to fetch in listings |
| `--search QUERY` | Server-side IMAP SEARCH |
| `--mark-seen` | Mark fetched messages as seen (mutates server state) |
| `--html` | When fetching a message, output the HTML body |
| `--raw` | When fetching a message, output the raw RFC 5322 source |
| `--help` | Print help |

For the authoritative list on the user's installed version:

```bash
myl --help
```

## What `myl` does not do

If the user asks for any of these, explain that `myl` is read-only and suggest an alternative:

- **Send mail** — use `msmtp`, `sendmail`, `mutt`, or scripted SMTP via Python's `smtplib` / a small `mailx` wrapper.
- **Move / copy / delete messages** — use `imap-tools` (Python), `imapcli`, or the provider's web UI.
- **Manage folders / labels** — same as above.
- **Sync to local maildir** — use `mbsync` (`isync`), `offlineimap`, or `getmail`.
- **OAuth2 to Gmail / Outlook** — `myl` uses password auth. For OAuth2 the user typically needs Proton Bridge, `mbsync` with an XOAUTH2 helper, or the provider's app-password fallback.
