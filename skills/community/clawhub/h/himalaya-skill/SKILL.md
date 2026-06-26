---
name: himalaya
description: |
  Expert guidance for querying, writing, and managing emails using the `himalaya` CLI.
  Use this skill whenever the user wants to list emails, search envelopes, compose messages,
  manage flags/folders, or execute any himalaya command. Also trigger when the user mentions
  "email CLI", "terminal email", "manage emails from command line", or references the
  Himalaya mail client. This skill provides the full query DSL specification, command
  patterns, and best practices for the himalaya email CLI.
---

# Himalaya CLI Expert

This skill makes you an instant expert on the [Himalaya](https://github.com/pimalaya/himalaya)
command-line email client. Himalaya is a stateless CLI (not a TUI) that lets users manage emails
via shell commands.

## When this skill applies

Use this skill for ANY task involving:
- Listing, searching, or sorting emails (`himalaya envelope list|thread`)
- Reading, writing, replying to, or forwarding messages (`himalaya message ...`)
- Managing flags (`himalaya flag ...`)
- Managing folders/mailboxes (`himalaya folder ...`)
- Message templates and attachments (`himalaya template ...`, `himalaya attachment ...`)
- Interpreting or constructing Himalaya query DSL strings

## Architecture overview

Himalaya CLI is organized around nouns:

```
himalaya <noun> <verb> [args...]
```

Key nouns:
- `envelope` (aliases: `envelopes`) — email envelopes (metadata, no body)
- `message` (aliases: `msg`, `msgs`, `messages`) — full email messages
- `flag` (aliases: `flags`) — message flags (seen, answered, flagged, deleted…)
- `folder` (aliases: `folders`, `mailbox`, `mailboxes`, `mbox`, `mboxes`) — mailboxes
- `template` (aliases: `tpl`, `tpls`, `templates`) — message templates
- `attachment` (aliases: `attachments`) — message attachments
- `account` (aliases: `accounts`) — account configuration

Global flags (available on all commands):
- `--config <PATH>` — override config file path
- `--output json` / `--output plain` — choose output format
- `--quiet`, `--debug`, `--trace` — logging levels

Common per-command flags:
- `-a <NAME>` / `--account <NAME>` — target a specific configured account
- `-f <NAME>` / `--folder <NAME>` — target a specific folder

## Querying emails: envelope commands

The most common operation is listing envelopes. Read the full Query DSL reference
(`references/query_dsl.md`) **whenever the user asks anything about search, filter, sort,
or list queries**.

### Essential commands

```bash
# List all envelopes in the default folder
himalaya envelope list

# List envelopes in a specific folder, page 2, 20 per page
himalaya envelope list -f Archives.FOSS --page 2 --page-size 20

# Thread view for envelopes matching a query
himalaya envelope thread subject "product requirement"
```

### Query DSL quick reference

A query string has the form:

```
[filter-query] [order by sort-query]
```

**Filter conditions:**
- `date <yyyy-mm-dd>` — exact date match
- `before <yyyy-mm-dd>` — strictly before date
- `after <yyyy-mm-dd>` — strictly after date
- `from <pattern>` — sender pattern match
- `to <pattern>` — recipient pattern match
- `subject <pattern>` — subject pattern match
- `body <pattern>` — body text match (slower)
- `flag <flag>` — flag match (e.g., `seen`, `deleted`)

**Operators (precedence: `not` > `and` > `or`):**
- `not <condition>`
- `<condition> and <condition>`
- `<condition> or <condition>`

**Sort query:**
- `order by date [asc|desc]`
- `order by from [asc|desc]`
- `order by to [asc|desc]`
- `order by subject [asc|desc]`
- Multiple fields are allowed: `order by from asc date desc`

**Quoting and escaping:**
- Use double quotes for values containing spaces: `subject "meeting notes"`
- Or escape with backslash: `subject meeting\ notes`
- In shell, the entire query may need to be passed as a single string or joined args.

### Query examples (detailed)

```bash
# Unread emails, newest first
himalaya envelope list "not flag seen order by date desc"

# From boss or CEO, sorted by date desc
himalaya envelope list "from boss@example.com or from ceo@example.com order by date desc"

# Subject contains "周报" AND body contains "进度"
himalaya envelope list "subject 周报 and body 进度"

# Date range: after March 31 and before April 11, 2025
himalaya envelope list "after 2025-03-31 and before 2025-04-11"

# Complex grouped condition: (subject urgent OR body error) AND from ops
himalaya envelope list '(subject 紧急 or body 报错) and from ops@example.com'

# Specific folder + pagination + query
himalaya envelope list -f INBOX --page 2 --page-size 20 'subject "release plan" order by date desc'
```

> **Performance tip**: Prefer `from`, `to`, `subject` over `body` because `body` triggers a
> server-side full-text scan.

> **Reference**: For the complete Query DSL specification, IMAP mapping, and compatibility
> notes, read `references/query_dsl.md`.

## Writing and sending emails: message commands

### Composing a new message

Himalaya uses your `$EDITOR` to compose messages from a template.

```bash
# Compose a new message interactively
himalaya message write

# Pre-fill headers via CLI arguments
himalaya message write --to "team@example.com" --subject "Sprint review"

# Compose using a saved template
himalaya message write --template /path/to/template.eml
```

### Reply and forward

```bash
# Reply to message ID 42
himalaya message reply 42

# Reply-all
himalaya message reply 42 --all

# Forward message ID 42
himalaya message forward 42 --to "someone@example.com"
```

### Reading, saving, and exporting

```bash
# Read raw message content
himalaya message read 42

# Save message to local .eml file
himalaya message save 42 --path ./message42.eml

# Export message(s)
himalaya message export 42 --path ./exports/
```

### Message template format

A template is a set of headers followed by a blank line and then the body:

```eml
From: alice@example.com
To: Bob <bob@example.com>
Subject: Hello from Himalaya

Hello, world!
```

Valid headers include: `From`, `To`, `Cc`, `Bcc`, `Reply-To`, `Subject`, `Date`,
`Message-ID`, `In-Reply-To`.

Addresses can be:
- Plain: `user@domain`
- Named: `Name <user@domain>`
- Quoted named: `"Name" <user@domain>`
- Multiple addresses separated by commas.

### Attachments

Attachments are handled via the `attachment` noun or MML syntax in templates.

```bash
# Download attachments from message 42
himalaya attachment download 42 --path ./downloads/
```

MML attachment example inside a template body:

```eml
From: alice@example.com
To: bob@example.com
Subject: Attaching a doc

<#part filename=/path/to/file.pdf><#/part>
```

## Managing emails: flags and folders

### Flags

```bash
# Add flag(s) to envelope(s)
himalaya flag add 42,43 flagged answered

# Remove flag(s)
himalaya flag remove 42 flagged

# Set exact flags (replaces existing)
himalaya flag set 42 seen
```

Common flags: `seen`, `answered`, `flagged`, `deleted`, `draft`.

### Folders

```bash
# List folders
himalaya folder list

# Add a folder
himalaya folder add MyFolder

# Delete a folder
himalaya folder delete MyFolder

# Purge deleted messages from a folder
himalaya folder purge MyFolder

# Expunge a folder
himalaya folder expunge MyFolder
```

## Multi-account workflows

Himalaya supports multiple accounts via TOML config. Target a non-default account with `-a`:

```bash
himalaya envelope list -a work -f INBOX
himalaya message write -a personal --to "friend@example.com"
```

## Output format tips

- Use `--output json` when you need structured data for piping into `jq` or scripts.
- Use `--output plain` (default) for human-readable tables and text.

## Common gotchas

1. **Trailing query args**: `himalaya envelope list` accepts the query as trailing arguments.
   Shell escaping matters. If the query has spaces, quote the entire query string.
2. **Page numbering**: `--page` starts at 1 (not 0).
3. **Date boundaries**: `before 2025-04-01` excludes April 1; `after 2025-04-01` also excludes
   April 1 (Himalaya adjusts internally by adding a day to use `SENTSINCE`).
4. **Config location**: Default is `~/.config/himalaya/config.toml`. Run `himalaya account configure <name>`
   for the wizard.

## External resources

- Repository: https://github.com/pimalaya/himalaya
- Query DSL reference (bundled): `references/query_dsl.md`
