---
name: gog-complete
description: "Google Workspace CLI for Gmail, Calendar, Chat, Classroom, Drive, Docs, Slides, Sheets, Forms, Apps Script, Contacts, Tasks, People, Admin, Groups, and Keep."
homepage: https://gogcli.sh
metadata:
  {
    "openclaw":
      {
        "emoji": "🎮",
        "requires": { "bins": ["gog"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "steipete/tap/gogcli",
              "bins": ["gog"],
              "label": "Install gog (brew)",
            },
          ],
      },
  }
---

# gog

Use `gog` for Gmail, Calendar, Chat, Classroom, Drive, Docs, Slides, Sheets, Forms, Apps Script, Contacts, Tasks, People, Admin, Groups, and Keep. Requires OAuth setup or service account auth.

## Setup (once)

```bash
gog auth credentials /path/to/client_secret.json
gog auth add you@gmail.com --services gmail,calendar,drive,contacts,docs,sheets
gog auth list
```

Set default account to avoid repeating `--account`:

```bash
export GOG_ACCOUNT=you@gmail.com
```

## Agent Behavior Rules

- Always confirm before sending mail, creating events, or deleting anything.
- Prefer `--json` plus `--no-input` for scripting and automation.
- Use `gog gmail search` for threads; use `gog gmail messages search` when individual messages are needed.
- Prefer plain text for email. Use `--body-file` for multi-paragraph. Use `--body-html` only when rich formatting is required.
- `--body` does not unescape `\n`. For multi-line use a heredoc or `--body-file -` (stdin).
- Set `GOG_ACCOUNT` to avoid repeating `--account` on every command.
- Use `GOG_HELP=full gog --help` if you need to discover subcommands not documented here.

## CRITICAL: Self-Discovery on Failure

The CLI evolves frequently. Flags and subcommands may change between versions. **If any command fails** (unknown flag, unknown command, wrong syntax):

1. Run `gog <group> --help` to see available subcommands and their aliases.
2. Run `gog <group> <subcommand> --help` to see the exact flags accepted.
3. Navigate deeper: `gog <group> <sub> <sub> --help` until you find the correct syntax.
4. Never assume a flag exists — verify with `--help` first if unsure.
5. Use `gog schema <command>` for machine-readable command/flag schema (JSON).

Example self-discovery flow:
```bash
# Command fails
gog calendar events create --title "Test"   # ERROR: unknown flag --title

# Discover correct subcommand
gog calendar --help                          # Shows: create (add,new) <calendarId> [flags]

# Discover correct flags
gog calendar create --help                   # Shows: --summary, --from, --to, etc.

# Use correct syntax
gog calendar create primary --summary "Test" --from 2026-04-04T21:00:00Z --to 2026-04-04T22:00:00Z
```

This self-discovery pattern applies to ALL command groups. Always fall back to `--help` navigation.

## Global Flags

- `-a, --account <email|alias|auto>` — Account override
- `-j, --json` — JSON stdout (best for parsing)
- `-p, --plain` — Stable TSV stdout (no colors)
- `--results-only` — JSON mode: emit only primary result (drops nextPageToken etc.)
- `--select <fields>` — JSON mode: select comma-separated fields (dot paths supported)
- `-n, --dry-run` — Do not make changes; print intended actions and exit
- `-y, --force` — Skip confirmations
- `--no-input` — Never prompt (CI/agent mode)
- `-v, --verbose` — Debug logging
- `--color <auto|always|never>`
- `--out` / `--output` — Output file path
- `--out-dir` / `--output-dir` — Output directory (attachments)
- `--enable-commands <csv>` — Allowlist top-level commands (sandboxing)
- `--version` — Print version

## Top-Level Aliases

These shortcuts avoid typing the full `<group> <command>` path:

- `gog send` → `gog gmail send`
- `gog ls` / `gog list` → `gog drive ls`
- `gog search` / `gog find` → `gog drive search`
- `gog download` / `gog dl` → `gog drive download`
- `gog upload` / `gog up` / `gog put` → `gog drive upload`
- `gog open` / `gog browse` → Print web URL for a Google ID
- `gog login` → `gog auth add`
- `gog logout` → `gog auth remove`
- `gog status` / `gog st` → `gog auth status`
- `gog me` / `gog whoami` → `gog people me`

## Command Group Aliases

- `gog cal` → `gog calendar`
- `gog drv` → `gog drive`
- `gog mail` / `gog email` → `gog gmail`
- `gog doc` → `gog docs`
- `gog slide` → `gog slides`
- `gog sheet` → `gog sheets`
- `gog form` → `gog forms`
- `gog contact` → `gog contacts`
- `gog task` → `gog tasks`
- `gog person` → `gog people`
- `gog group` → `gog groups`
- `gog class` → `gog classroom`
- `gog script` / `gog apps-script` → `gog appscript`

## Environment Variables

- `GOG_ACCOUNT` — Default account
- `GOG_ACCESS_TOKEN` — Direct access token (CI; ~1h, no refresh)
- `GOG_CLIENT` — OAuth client name
- `GOG_JSON` / `GOG_PLAIN` — Default output format
- `GOG_COLOR` — Color mode
- `GOG_TIMEZONE` — Default timezone (IANA, `UTC`, or `local`)
- `GOG_ENABLE_COMMANDS` — Command allowlist
- `GOG_KEYRING_BACKEND` — Force keyring (`auto`/`keychain`/`file`)
- `GOG_KEYRING_PASSWORD` — Password for file keyring (CI)

## Authentication Commands

```bash
# Credentials
gog auth credentials <path>
gog auth credentials list
gog --client <name> auth credentials <path>
gog --client <name> auth credentials <path> --domain example.com

# Add account
gog auth add <email>
gog auth add <email> --services gmail,calendar,drive,contacts,docs,sheets
gog auth add <email> --services drive --drive-scope full|readonly|file
gog auth add <email> --services gmail --gmail-scope full|readonly
gog auth add <email> --services gmail --extra-scopes <scope-uri>
gog auth add <email> --readonly
gog auth add <email> --services user --force-consent

# Headless / remote flows
gog auth add <email> --services user --manual
gog auth add <email> --services user --remote --step 1
gog auth add <email> --services user --remote --step 2 --auth-url '<url>'
gog auth add <email> --listen-addr 0.0.0.0:8080 --redirect-host gog.example.com

# Direct access token
gog --access-token "$(gcloud auth print-access-token)" gmail labels list

# Service accounts (Workspace domain-wide delegation)
gog auth service-account set <email> --key <path>
gog auth service-account status <email>
gog auth service-account unset <email>
gog auth keep <email> --key <path>

# Keyring
gog auth keyring
gog auth keyring file|keychain|auto

# Management
gog auth list
gog auth list --check
gog auth status
gog auth services
gog auth remove <email>
gog auth manage
gog auth tokens

# Aliases
gog auth alias set <alias> <email>
gog auth alias list
gog auth alias unset <alias>
```

## Config Commands

```bash
gog config path
gog config list
gog config keys
gog config get <key>
gog config set <key> <value>
gog config unset <key>
```

Config (JSON5) supports: `keyring_backend`, `default_timezone`, `account_aliases`, `account_clients`, `client_domains`.

## Gmail

### Search & Read

```bash
gog gmail search 'newer_than:7d' --max 10
gog gmail messages search 'in:inbox from:ryanair.com' --max 20
gog gmail messages search 'newer_than:7d' --max 3 --include-body --json
gog gmail thread get <threadId>
gog gmail thread get <threadId> --download
gog gmail thread get <threadId> --download --out-dir ./attachments
gog gmail get <messageId>
gog gmail get <messageId> --format metadata
gog gmail attachment <messageId> <attachmentId>
gog gmail attachment <messageId> <attachmentId> --out ./file.bin
gog gmail url <threadId>
```

### Send & Compose

```bash
gog gmail send --to a@b.com --subject "Hi" --body "Hello"
gog gmail send --to a@b.com --subject "Hi" --body-file ./message.txt
gog gmail send --to a@b.com --subject "Hi" --body-file -
gog gmail send --to a@b.com --subject "Hi" --body "Plain" --body-html "<p>Hello</p>"
gog gmail send --reply-to-message-id <msgId> --quote --to a@b.com --subject "Re: Hi" --body "Reply"
gog gmail send --to a@b.com --subject "Hello" --body-html "<p>Hi!</p>" --track
```

### Drafts

```bash
gog gmail drafts list
gog gmail drafts create --to a@b.com --subject "Draft" --body "Body"
gog gmail drafts create --reply-to-message-id <msgId> --quote --subject "Re: Hi" --body "Reply"
gog gmail drafts update <draftId> --subject "New" --body "Updated"
gog gmail drafts update <draftId> --to a@b.com --subject "New" --body "Updated"
gog gmail drafts update <draftId> --reply-to-message-id <msgId> --quote --subject "Re: Hi" --body "Reply"
gog gmail drafts update <draftId> --quote --subject "Re: Hi" --body "Reply"
gog gmail drafts send <draftId>
```

### Thread & Message Modification

```bash
gog gmail thread modify <threadId> --add STARRED --remove INBOX
gog gmail labels modify <threadId> --add STARRED --remove INBOX
gog gmail batch delete <msgId1> <msgId2>
gog gmail batch modify <msgId1> <msgId2> --add STARRED --remove INBOX
```

### Labels

```bash
gog gmail labels list
gog gmail labels get INBOX --json
gog gmail labels create "My Label"
gog gmail labels rename "Old Label" "New Label"
gog gmail labels delete <labelIdOrName>
```

### Filters

```bash
gog gmail filters list
gog gmail filters create --from 'noreply@example.com' --add-label 'Notifications'
gog gmail filters delete <filterId>
gog gmail filters export --out ./filters.json
```

### Settings

```bash
gog gmail autoforward get
gog gmail autoforward enable --email forward@example.com
gog gmail autoforward disable
gog gmail forwarding list
gog gmail forwarding add --email forward@example.com
gog gmail sendas list
gog gmail sendas create --email alias@example.com
gog gmail vacation get
gog gmail vacation enable --subject "Out of office" --message "..."
gog gmail vacation disable
```

### Delegation (Workspace)

```bash
gog gmail delegates list
gog gmail delegates add --email delegate@example.com
gog gmail delegates remove --email delegate@example.com
```

### Watch (Pub/Sub)

```bash
gog gmail watch start --topic projects/<p>/topics/<t> --label INBOX
gog gmail watch serve --bind 127.0.0.1 --token <shared> --hook-url <url>
gog gmail watch serve --bind 0.0.0.0 --verify-oidc --oidc-email <svc@...> --hook-url <url>
gog gmail watch serve --bind 127.0.0.1 --token <shared> --fetch-delay 5 --hook-url <url>
gog gmail watch serve --bind 127.0.0.1 --token <shared> --exclude-labels SPAM,TRASH --hook-url <url>
gog gmail history --since <historyId>
```

### Email Tracking

```bash
gog gmail track setup --worker-url https://gog-email-tracker.<acct>.workers.dev
gog gmail send --to a@b.com --subject "Hello" --body-html "<p>Hi!</p>" --track
gog gmail track opens <tracking_id>
gog gmail track opens --to recipient@example.com
gog gmail track status
```

### Email Formatting Guide

- Prefer plain text for emails. Use `--body-file` for multi-paragraph (or `--body-file -` for stdin).
- Same `--body-file` pattern works for drafts and replies.
- `--body` does not unescape `\n`. For inline newlines, use a heredoc or `$'Line 1\n\nLine 2'`.
- Use `--body-html` only when rich formatting is needed.
- HTML tags: `<p>` paragraphs, `<br>` line breaks, `<strong>` bold, `<em>` italic, `<a href="url">` links, `<ul>`/`<li>` lists.
- `--track` requires exactly 1 recipient and `--body-html`. Use `--track-split` for per-recipient tracking.

Example (plain text via stdin):

```bash
gog gmail send --to recipient@example.com \
  --subject "Meeting Follow-up" \
  --body-file - <<'EOF'
Hi Name,

Thanks for meeting today. Next steps:
- Item one
- Item two

Best regards,
Your Name
EOF
```

Example (HTML):

```bash
gog gmail send --to recipient@example.com \
  --subject "Meeting Follow-up" \
  --body-html "<p>Hi Name,</p><p>Next steps:</p><ul><li>Item one</li><li>Item two</li></ul><p>Best,<br>Your Name</p>"
```

## Calendar

### List & View

```bash
gog calendar calendars
gog calendar subscribe <calendarId>
gog calendar acl <calendarId>
gog calendar colors
gog calendar time --timezone America/New_York
gog calendar users
gog calendar alias                    # Manage calendar aliases

# Events
gog calendar events <calendarId> --today
gog calendar events <calendarId> --tomorrow
gog calendar events <calendarId> --week
gog calendar events <calendarId> --days 3
gog calendar events <calendarId> --from today --to friday
gog calendar events <calendarId> --from today --to friday --weekday
gog calendar events <calendarId> --from <iso> --to <iso>
gog calendar events --all
gog calendar events --calendars 1,3
gog calendar events --cal Work --cal Personal

# Single event
gog calendar event <calendarId> <eventId>
gog calendar get <calendarId> <eventId>
gog calendar get <calendarId> <eventId> --json

# Search
gog calendar search "meeting" --today
gog calendar search "meeting" --tomorrow
gog calendar search "meeting" --days 365
gog calendar search "meeting" --from <iso> --to <iso> --max 50

# Team
gog calendar team <group-email> --today
gog calendar team <group-email> --week
gog calendar team <group-email> --freebusy
gog calendar team <group-email> --query "standup"
```

### Create & Update

```bash
gog calendar create <calendarId> --summary "Meeting" --from <iso> --to <iso>
gog calendar create <calendarId> --summary "Sync" --from <iso> --to <iso> --attendees "a@x.com,b@x.com" --location "Zoom"
gog calendar create <calendarId> --summary "Meeting" --from <iso> --to <iso> --event-color 7
gog calendar create <calendarId> --summary "Meeting" --from <iso> --to <iso> --send-updates all
gog calendar create <calendarId> --summary "Pay" --from <iso> --to <iso> --rrule "RRULE:FREQ=MONTHLY;BYMONTHDAY=11" --reminder "email:3d" --reminder "popup:30m"
gog calendar create <calendarId> --summary "Meeting" --from <iso> --to <iso> --with-meet
gog calendar create <calendarId> --summary "Meeting" --from <iso> --to <iso> --description "Notes" --visibility private --transparency free
gog calendar create <calendarId> --summary "Meeting" --from <iso> --to <iso> --guests-can-invite --guests-can-modify --guests-can-see-others
gog calendar create <calendarId> --summary "Meeting" --from <iso> --to <iso> --attachment <url> --source-url <url> --source-title "Source"
gog calendar create <calendarId> --summary "Meeting" --from <iso> --to <iso> --private-prop key=value --shared-prop key=value

# Special types: Focus Time
gog calendar create primary --event-type focus-time --from <iso> --to <iso>
gog calendar create primary --event-type focus-time --from <iso> --to <iso> --focus-auto-decline --focus-decline-message "Focusing" --focus-chat-status "doNotDisturb"

# Special types: Out of Office
gog calendar create primary --event-type out-of-office --from <date> --to <date> --all-day
gog calendar create primary --event-type out-of-office --from <date> --to <date> --all-day --ooo-auto-decline --ooo-decline-message "I'm away"

# Special types: Working Location
gog calendar create primary --event-type working-location --working-location-type office --working-office-label "HQ" --from <date> --to <date>
gog calendar create primary --event-type working-location --working-location-type office --working-office-label "HQ" --working-building-id "B1" --working-floor-id "3" --working-desk-id "3A" --from <date> --to <date>
gog calendar create primary --event-type working-location --working-location-type home --from <date> --to <date>
gog calendar create primary --event-type working-location --working-location-type custom --working-custom-label "Coffee Shop" --from <date> --to <date>

# Shortcuts (same flags apply)
gog calendar focus-time --from <iso> --to <iso>
gog calendar focus-time --from <iso> --to <iso> --focus-auto-decline --focus-decline-message "Focusing" --focus-chat-status "doNotDisturb"
gog calendar out-of-office --from <date> --to <date> --all-day
gog calendar out-of-office --from <date> --to <date> --all-day --ooo-auto-decline --ooo-decline-message "I'm away"
gog calendar working-location --type office --office-label "HQ" --from <date> --to <date>
gog calendar working-location --type home --from <date> --to <date>
gog calendar working-location --type custom --custom-label "Coffee Shop" --from <date> --to <date>

# Update
gog calendar update <calendarId> <eventId> --summary "Updated" --from <iso> --to <iso>
gog calendar update <calendarId> <eventId> --event-color 4
gog calendar update <calendarId> <eventId> --send-updates externalOnly
gog calendar update <calendarId> <eventId> --add-attendee "a@x.com,b@x.com"

# Delete
gog calendar delete <calendarId> <eventId>
gog calendar delete <calendarId> <eventId> --send-updates all --force
```

### Invitations & Availability

```bash
gog calendar respond <calendarId> <eventId> --status accepted|declined|tentative
gog calendar respond <calendarId> <eventId> --status declined --send-updates externalOnly
gog calendar propose-time <calendarId> <eventId>
gog calendar propose-time <calendarId> <eventId> --open
gog calendar propose-time <calendarId> <eventId> --decline --comment "Can we do 5pm?"
gog calendar freebusy --calendars "primary,work@x.com" --from <iso> --to <iso>
gog calendar freebusy --cal Work --from <iso> --to <iso>
gog calendar conflicts --calendars "primary,work@x.com" --today
gog calendar conflicts --all --today
```

### Calendar Colors Reference

Use `gog calendar colors` to list. Add with `--event-color <id>`.

| ID | Hex |
|----|---------|
| 1 | #a4bdfc |
| 2 | #7ae7bf |
| 3 | #dbadff |
| 4 | #ff887c |
| 5 | #fbd75b |
| 6 | #ffb878 |
| 7 | #46d6db |
| 8 | #e1e1e1 |
| 9 | #5484ed |
| 10 | #51b749 |
| 11 | #dc2127 |

### Calendar Notes

- Search defaults to 30 days ago through 90 days ahead unless `--from/--to/--today/--week/--days` is set.
- JSON output includes `startDayOfWeek`, `endDayOfWeek`, `timezone`, `startLocal`, `endLocal` convenience fields.
- Set `GOG_CALENDAR_WEEKDAY=1` to default `--weekday` for event output.
- Default: no attendee notifications unless `--send-updates` is passed.
- `--add-attendee` adds without replacing existing attendees/RSVP state.

## Time

```bash
gog time now
gog time now --timezone UTC
```

## Drive

### List & Search

```bash
gog drive ls --max 20
gog drive ls --parent <folderId> --max 20
gog drive ls --all --max 20
gog drive ls --no-all-drives
gog drive search "invoice" --max 20
gog drive search "invoice" --no-all-drives
gog drive search "mimeType = 'application/pdf'" --raw-query
gog drive get <fileId>
gog drive url <fileId>
gog drive copy <fileId> "Copy Name"
```

### Upload & Download

```bash
gog drive upload ./file.pdf --parent <folderId>
gog drive upload ./file.pdf --replace <fileId>
gog drive upload ./report.docx --convert
gog drive upload ./chart.png --convert-to sheet
gog drive upload ./report.docx --convert --name report.docx
gog drive download <fileId> --out ./file.bin
gog drive download <fileId> --format pdf --out ./exported.pdf
gog drive download <fileId> --format docx --out ./doc.docx
gog drive download <fileId> --format pptx --out ./slides.pptx
```

### Organize

```bash
gog drive mkdir "Folder"
gog drive mkdir "Folder" --parent <parentId>
gog drive rename <fileId> "New Name"
gog drive move <fileId> --parent <destId>
gog drive delete <fileId>
gog drive delete <fileId> --permanent
```

### Permissions & Sharing

```bash
gog drive permissions <fileId>
gog drive share <fileId> --to user --email user@x.com --role reader|writer
gog drive share <fileId> --to domain --domain example.com --role reader
gog drive unshare <fileId> --permission-id <permId>
gog drive drives --max 100
```

## Docs

```bash
gog docs info <docId>
gog docs cat <docId>
gog docs cat <docId> --max-bytes 10000
gog docs cat <docId> --tab "Notes"
gog docs cat <docId> --all-tabs
gog docs create "My Doc"
gog docs create "My Doc" --file ./doc.md
gog docs create "My Doc" --pageless
gog docs copy <docId> "Copy"
gog docs list-tabs <docId>

# Export
gog docs export <docId> --format pdf|docx|txt|md|html --out ./file

# Edit
gog docs update <docId> --text "Append text"
gog docs update <docId> --text "Tab text" --tab-id t.notes
gog docs update <docId> --file ./insert.txt --index 25 --pageless
gog docs write <docId> --text "Replace all"
gog docs write <docId> --text "Tab replace" --tab-id t.notes
gog docs write <docId> --file ./body.txt --append --pageless
gog docs find-replace <docId> "old" "new"
gog docs find-replace <docId> "old" "new" --tab-id t.notes

# Sed-style editing (sedmat syntax)
gog docs sed <docId> 's/pattern/replacement/g'
gog docs sed <docId> 's/hello/**hello**/'              # bold
gog docs sed <docId> 's/hello/*hello*/'                 # italic
gog docs sed <docId> 's/hello/~~hello~~/'               # strikethrough
gog docs sed <docId> 's/hello/`hello`/'                 # monospace
gog docs sed <docId> 's/hello/__hello__/'               # underline
gog docs sed <docId> 's/word/[word](https://url)/'     # link
gog docs sed <docId> 's/{{IMG}}/![](https://url/img.png)/'
gog docs sed <docId> 's/{{IMG}}/![](https://url/img.jpg){width=600}/'
gog docs sed <docId> 's/{{TABLE}}/|3x4|/'              # 3-row 4-col table
gog docs sed <docId> 's/|1|[A1]/**Name**/'             # set cell
gog docs sed <docId> 's/|1|[1,*]/**&**/'               # bold entire row
gog docs sed <docId> 's/|1|[row:+2]//'                 # insert row
gog docs sed <docId> 's/|1|[col:$+]//'                 # append column
```

## Slides

```bash
gog slides info <presentationId>
gog slides create "My Deck"
gog slides copy <presentationId> "Copy"
gog slides list-slides <presentationId>
gog slides add-slide <presentationId> ./slide.png --notes "Speaker notes"
gog slides update-notes <presentationId> <slideId> --notes "Updated"
gog slides replace-slide <presentationId> <slideId> ./new.png --notes "New"
gog slides export <presentationId> --format pdf|pptx --out ./file
gog slides create-from-markdown "Deck" --content-file ./slides.md
gog slides create-from-template <templateId> "Report" --replace "name=John" --replace "date=2026-02-15"
gog slides create-from-template <templateId> "Report" --replacements replacements.json
```

## Sheets

### Read & Metadata

```bash
gog sheets metadata <spreadsheetId>
gog sheets get <spreadsheetId> 'Sheet1!A1:B10'
gog sheets get <spreadsheetId> 'Sheet1!A1:D10' --json
gog sheets get <spreadsheetId> MyNamedRange
```

### Create & Export

```bash
gog sheets create "My Sheet" --sheets "Sheet1,Sheet2"
gog sheets copy <spreadsheetId> "Copy"
gog sheets export <spreadsheetId> --format pdf|xlsx --out ./file
```

### Write & Modify

```bash
gog sheets update <spreadsheetId> 'A1' 'val1|val2,val3|val4'
gog sheets update <spreadsheetId> 'A1' --values-json '[["a","b"],["c","d"]]'
gog sheets update <spreadsheetId> 'Sheet1!A1:B2' --values-json '[["A","B"],["1","2"]]' --input USER_ENTERED
gog sheets update <spreadsheetId> 'Sheet1!A1:C1' 'data' --copy-validation-from 'Sheet1!A2:C2'
gog sheets update <spreadsheetId> MyNamedRange 'new|row|data'
gog sheets append <spreadsheetId> 'Sheet1!A:C' 'new|row|data'
gog sheets append <spreadsheetId> 'Sheet1!A:C' --values-json '[["x","y","z"]]' --insert INSERT_ROWS
gog sheets append <spreadsheetId> 'Sheet1!A:C' 'data' --copy-validation-from 'Sheet1!A2:C2'
gog sheets append <spreadsheetId> MyNamedRange 'new|row|data'
gog sheets clear <spreadsheetId> 'Sheet1!A1:B10'
gog sheets clear <spreadsheetId> MyNamedRange
```

### Find/Replace, Notes & Links

```bash
gog sheets find-replace <spreadsheetId> "old" "new"
gog sheets find-replace <spreadsheetId> "old" "new" --sheet Sheet1 --match-entire
gog sheets find-replace <spreadsheetId> "old" "new" --sheet Sheet1 --regex
gog sheets notes <spreadsheetId> 'Sheet1!A1:B10'
gog sheets update-note <spreadsheetId> 'Sheet1!A1' --note ''
gog sheets links <spreadsheetId> 'Sheet1!A1:B10'
```

### Formatting

```bash
gog sheets format <spreadsheetId> 'Sheet1!A1:B2' --format-json '{"textFormat":{"bold":true}}' --format-fields 'userEnteredFormat.textFormat.bold'
gog sheets format <spreadsheetId> MyNamedRange --format-json '...' --format-fields '...'
gog sheets merge <spreadsheetId> 'Sheet1!A1:B2'
gog sheets unmerge <spreadsheetId> 'Sheet1!A1:B2'
gog sheets number-format <spreadsheetId> 'Sheet1!C:C' --type CURRENCY --pattern '$#,##0.00'
gog sheets freeze <spreadsheetId> --rows 1 --cols 1
gog sheets resize-columns <spreadsheetId> 'Sheet1!A:C' --auto
gog sheets resize-rows <spreadsheetId> 'Sheet1!1:10' --height 36
gog sheets read-format <spreadsheetId> 'Sheet1!A1:B2'
gog sheets read-format <spreadsheetId> 'Sheet1!A1:B2' --effective
```

### Named Ranges

```bash
gog sheets named-ranges <spreadsheetId>
gog sheets named-ranges get <spreadsheetId> MyRange
gog sheets named-ranges add <spreadsheetId> MyRange 'Sheet1!A1:B2'
gog sheets named-ranges add <spreadsheetId> MyCols 'Sheet1!A:C'
gog sheets named-ranges update <spreadsheetId> MyRange --name NewName
gog sheets named-ranges delete <spreadsheetId> MyRange
```

### Structure

```bash
gog sheets insert <spreadsheetId> "Sheet1" rows 2 --count 3
gog sheets insert <spreadsheetId> "Sheet1" cols 3 --after
gog sheets add-tab <spreadsheetId> <tabName>
gog sheets rename-tab <spreadsheetId> <oldName> <newName>
gog sheets delete-tab <spreadsheetId> <tabName>
gog sheets delete-tab <spreadsheetId> <tabName> --force
```

### Sheets Notes

- Values can be passed via `--values-json` (recommended) or as inline pipe-delimited rows.
- Use `--input USER_ENTERED` so Sheets parses formulas/numbers; default is `RAW`.
- Named ranges work in `get`, `update`, `append`, `clear`, and `format`.

## Forms

```bash
gog forms get <formId>
gog forms create --title "Check-in" --description "Friday update"
gog forms update <formId> --title "Sync" --quiz true
gog forms add-question <formId> --title "What shipped?" --type paragraph --required
gog forms move-question <formId> 3 1
gog forms delete-question <formId> 2 --force
gog forms responses list <formId> --max 20
gog forms responses get <formId> <responseId>
gog forms watch create <formId> --topic projects/<p>/topics/<t>
gog forms watch list <formId>
gog forms watch renew <formId> <watchId>
gog forms watch delete <formId> <watchId>
```

## Apps Script

```bash
gog appscript get <scriptId>
gog appscript content <scriptId>
gog appscript create --title "Helpers"
gog appscript create --title "Bound" --parent-id <driveFileId>
gog appscript run <scriptId> myFunction --params '["arg1", 123, true]'
gog appscript run <scriptId> myFunction --dev-mode
```

## Contacts

### Personal & Other Contacts

```bash
gog contacts list --max 50
gog contacts search "Ada" --max 50
gog contacts get people/<resourceName>
gog contacts get user@example.com
gog contacts other list --max 50
gog contacts other search "John" --max 50
```

### Create & Update

```bash
gog contacts create --given "John" --family "Doe" --email "john@x.com" --phone "+1234567890" --address "Address" --relation "spouse=Jane"
gog contacts update people/<resourceName> --given "Jane" --email "jane@x.com" --address "Address" --birthday "1990-05-12" --notes "Note" --relation "friend=Bob"
gog contacts get people/<resourceName> --json | jq '...' | gog contacts update people/<resourceName> --from-file -
gog contacts delete people/<resourceName>
```

### Workspace Directory

```bash
gog contacts directory list --max 50
gog contacts directory search "Jane" --max 50
```

## Tasks

```bash
# Lists
gog tasks lists --max 50
gog tasks lists create <title>

# Tasks
gog tasks list <tasklistId> --max 50
gog tasks get <tasklistId> <taskId>
gog tasks add <tasklistId> --title "Task"
gog tasks add <tasklistId> --title "Weekly" --due 2025-02-01 --repeat weekly --repeat-count 4
gog tasks add <tasklistId> --title "Daily" --due 2025-02-01 --repeat daily --repeat-until 2025-02-05
gog tasks add <tasklistId> --title "Biweekly" --due 2025-02-01 --recur-rrule "FREQ=WEEKLY;INTERVAL=2" --repeat-count 3
gog tasks update <tasklistId> <taskId> --title "New title"
gog tasks done <tasklistId> <taskId>
gog tasks undo <tasklistId> <taskId>
gog tasks delete <tasklistId> <taskId>
gog tasks clear <tasklistId>
```

Tasks Notes: Google Tasks treats due dates as date-only. `--repeat*`/`--recur*` materialize concrete tasks (not true API recurrence).

## Chat (Workspace only)

```bash
# Spaces
gog chat spaces list
gog chat spaces find "Engineering"
gog chat spaces create "Engineering" --member alice@x.com --member bob@x.com

# Messages
gog chat messages list spaces/<spaceId> --max 5
gog chat messages list spaces/<spaceId> --thread <threadId>
gog chat messages list spaces/<spaceId> --unread
gog chat messages send spaces/<spaceId> --text "Done!" --thread spaces/<spaceId>/threads/<threadId>

# Reactions
gog chat messages reactions list spaces/<spaceId>/messages/<msgId>
gog chat messages react spaces/<spaceId>/messages/<msgId> "👍"
gog chat messages reactions delete spaces/<spaceId>/messages/<msgId>/reactions/<reactionId>

# Threads & DMs
gog chat threads list spaces/<spaceId>
gog chat dm space user@company.com
gog chat dm send user@company.com --text "ping"
```

## Classroom (Workspace for Education)

### Courses

```bash
gog classroom courses list
gog classroom courses list --role teacher
gog classroom courses get <courseId>
gog classroom courses create --name "Math 101"
gog classroom courses update <courseId> --name "Math 102"
gog classroom courses archive <courseId>
gog classroom courses unarchive <courseId>
gog classroom courses url <courseId>
```

### Roster & Members

```bash
gog classroom roster <courseId>
gog classroom roster <courseId> --students
gog classroom students add <courseId> <userId>
gog classroom teachers add <courseId> <userId>
```

### Coursework & Materials

```bash
gog classroom coursework list <courseId>
gog classroom coursework get <courseId> <courseworkId>
gog classroom coursework create <courseId> --title "HW1" --type ASSIGNMENT --state PUBLISHED
gog classroom coursework update <courseId> <courseworkId> --title "Updated"
gog classroom coursework assignees <courseId> <courseworkId> --mode INDIVIDUAL_STUDENTS --add-student <studentId>
gog classroom materials list <courseId>
gog classroom materials create <courseId> --title "Syllabus" --state PUBLISHED
```

### Submissions

```bash
gog classroom submissions list <courseId> <courseworkId>
gog classroom submissions get <courseId> <courseworkId> <submissionId>
gog classroom submissions grade <courseId> <courseworkId> <submissionId> --grade 85
gog classroom submissions return <courseId> <courseworkId> <submissionId>
gog classroom submissions turn-in <courseId> <courseworkId> <submissionId>
gog classroom submissions reclaim <courseId> <courseworkId> <submissionId>
```

### Announcements & Topics

```bash
gog classroom announcements list <courseId>
gog classroom announcements create <courseId> --text "Welcome!"
gog classroom announcements update <courseId> <announcementId> --text "Updated"
gog classroom announcements assignees <courseId> <announcementId> --mode INDIVIDUAL_STUDENTS --add-student <studentId>
gog classroom topics list <courseId>
gog classroom topics create <courseId> --name "Unit 1"
gog classroom topics update <courseId> <topicId> --name "Unit 2"
```

### Invitations & Guardians

```bash
gog classroom invitations list
gog classroom invitations create <courseId> <userId> --role student
gog classroom invitations accept <invitationId>
gog classroom guardians list <studentId>
gog classroom guardians get <studentId> <guardianId>
gog classroom guardians delete <studentId> <guardianId>
gog classroom guardian-invitations list <studentId>
gog classroom guardian-invitations create <studentId> --email parent@example.com
gog classroom profile get
gog classroom profile get <userId>
```

## People

```bash
gog people me
gog people get people/<userId>
gog people search "Ada Lovelace" --max 5
gog people relations
gog people relations people/<userId> --type manager
```

## Keep (Workspace only)

```bash
gog keep list --account you@domain.com
gog keep get <noteId> --account you@domain.com
gog keep search <query> --account you@domain.com
gog keep create --title "Todo" --item "Milk" --item "Eggs" --account you@domain.com
gog keep create --title "Note" --text "Remember" --account you@domain.com
gog keep delete <noteId> --account you@domain.com --force
gog keep attachment <attachmentName> --account you@domain.com --out ./file.bin
```

## Admin (Workspace only)

```bash
gog admin users list --domain example.com
gog admin users get user@example.com
gog admin users create user@example.com --given Ada --family Lovelace --password 'TempPass123!'
gog admin users suspend user@example.com --force
gog admin groups list --domain example.com
gog admin groups members list engineering@example.com
gog admin groups members add engineering@example.com user@example.com --role MEMBER
gog admin groups members remove engineering@example.com user@example.com --force
```

## Groups (Workspace)

```bash
gog groups list
gog groups members engineering@company.com
```

## Agent Commands

```bash
# Run gog as an autonomous agent (MCP / tool-use mode)
gog agent --help                      # discover all agent sub-flags
gog agent run --instructions "..."    # run agent with instructions
gog agent run --instructions-file ./plan.md
```

## Schema & Utilities

```bash
gog schema                            # list available schemas
gog schema <resource>                 # show schema for a resource
gog open <url>                        # open a Google resource URL
gog exit-codes                        # list all exit codes and meanings
```

## Shell Completions

```bash
gog completion bash > $(brew --prefix)/etc/bash_completion.d/gog
gog completion zsh > "${fpath[1]}/_gog"
gog completion fish > ~/.config/fish/completions/gog.fish
gog completion powershell | Out-String | Invoke-Expression
gog completion powershell >> $PROFILE
```

## Output Formats

- Default: human-friendly tables with colors on TTY.
- `--plain`: stable TSV (tabs preserved; best for piping).
- `--json`: JSON on stdout (best for scripting).
- Hints/progress go to stderr. Colors auto-disabled for `--json`/`--plain`.

## Best Practices & Gotchas

- Always confirm before sending mail, creating events, or deleting resources.
- `gog gmail search` returns one row per **thread**; use `gog gmail messages search` when you need every individual **message**.
- For multi-line email bodies, always use `--body-file`. `--body` treats content as a single line.
- Sheets `--values-json` is recommended over pipe-delimited inline syntax.
- Docs supports export/cat/copy/write/sed. In-place structural edits use `gog docs sed` (sedmat syntax).
- Calendar `--send-updates` is opt-in: no notifications sent by default.
- Service account domain delegation takes precedence over OAuth when configured.
- `gog` supports command allowlists (`--enable-commands` / `GOG_ENABLE_COMMANDS`) for sandboxed agent runs.
- Credentials stored in OS keyring or encrypted local storage. Use `GOG_KEYRING_BACKEND=file` + `GOG_KEYRING_PASSWORD` for CI.