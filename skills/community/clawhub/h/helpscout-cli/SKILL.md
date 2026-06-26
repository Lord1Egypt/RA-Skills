---
name: hs
description: CLI for the HelpScout API. Manage conversations, customers, mailboxes, knowledge base articles, and more from the terminal. Covers both Inbox and Docs APIs with full CRUD, PII redaction, permissions, and multiple output formats.
homepage: https://github.com/operator-kit/hs-cli
metadata: {"clawdbot":{"emoji":"📬","requires":{"bins":["hs"]},"install":[{"id":"brew","kind":"brew","formula":"operator-kit/tap/hs","bins":["hs"],"label":"Install hs (brew)"}]}}
---

# hs

Use `hs` to interact with HelpScout from the terminal. Two API namespaces: `hs inbox` (Mailbox API — conversations, customers, users, teams, etc.) and `hs docs` (Docs API — sites, collections, categories, articles).

## Auth

Inbox uses OAuth2 client credentials (App ID + App Secret). Docs uses an API key.

- `hs inbox auth login` — interactive setup, validates against the API
- `hs docs auth login` — prompt for Docs API key, validates
- `hs inbox auth status` / `hs docs auth status` — check stored credentials
- `hs inbox auth logout` / `hs docs auth logout` — remove credentials

Credential resolution order: **OS keyring** → **config file**. For non-interactive auth, use `hs inbox config set --inbox-app-id <id> --inbox-app-secret <secret>`.

## Inbox commands

### Conversations (`conv`)
- `hs inbox conv list --status active --mailbox <id> --tag <name> --assigned-to <uid> --embed threads`
- `hs inbox conv get <id> --embed threads`
- `hs inbox conv create --mailbox <id> --subject "..." --customer <email> --body "..."`
- `hs inbox conv update <id> --status closed --subject "..."`
- `hs inbox conv delete <id>`
- `hs inbox conv threads list <conv-id>`
- `hs inbox conv threads reply <conv-id> --customer <email> --body "..." --status closed`
- `hs inbox conv threads note <conv-id> --body "..."`
- `hs inbox conv tags set <conv-id> --tag billing --tag urgent`
- `hs inbox conv fields set <conv-id> --field <id>=<value>`
- `hs inbox conv attachments upload <conv-id> --thread-id <id> --file ./path`

### Customers (`cust`)
- `hs inbox cust list --query "email:jane@example.com"`
- `hs inbox cust get <id>`
- `hs inbox cust create --first-name Jane --last-name Doe --email jane@example.com`
- `hs inbox cust update <id> --last-name Smith`
- `hs inbox cust delete <id>`

### Mailboxes (`mb`)
- `hs inbox mb list` / `hs inbox mb get <id>`
- `hs inbox mb folders list <mb-id>` / `hs inbox mb custom-fields list <mb-id>`

### Users
- `hs inbox users list --email user@co.com` / `hs inbox users get <id>` / `hs inbox users me`
- `hs inbox users status get <uid>` / `hs inbox users status set <uid> --status away`

### Teams
- `hs inbox teams list` / `hs inbox teams members <team-id>`

### Organizations
- `hs inbox organizations list --query "acme"` / `hs inbox organizations get <id>`
- `hs inbox organizations create --name "Acme Corp"` / `hs inbox organizations delete <id>`

### Tags / Ratings
- `hs inbox tags list` / `hs inbox ratings list`

### Workflows (`wf`)
- `hs inbox wf list` / `hs inbox wf run <id> --conversation-ids id1,id2`
- `hs inbox wf update-status <id> --status active`

### Webhooks (`wh`)
- `hs inbox wh list` / `hs inbox wh get <id>`
- `hs inbox wh create --url https://... --events convo.created --secret s3cret`
- `hs inbox wh delete <id>`

### Saved replies
- `hs inbox saved-replies list --mailbox-id <id>`
- `hs inbox saved-replies create --mailbox-id <id> --name "Greeting" --body "Hello..."`

### Reports
- `hs inbox reports conversations --start 2025-01-01 --end 2025-01-31 --mailbox <id>`
- Subcommands: `chats`, `company`, `conversations`, `customers`, `docs`, `email`, `productivity`, `ratings`, `users`

### Tools
- `hs inbox tools briefing` — daily briefing summary
- `hs inbox tools briefing --assigned-to <uid> --embed threads` — agent-specific briefing with thread content

## Docs commands

### Sites
- `hs docs sites list` / `hs docs sites get <id>`
- `hs docs sites create --subdomain help --title "Help Center"`

### Collections
- `hs docs collections list --site <id>` / `hs docs collections get <id>`
- `hs docs collections create --site <id> --name "Getting Started"`

### Categories
- `hs docs categories list <collection-id>` / `hs docs categories get <id>`
- `hs docs categories create --collection <id> --name "FAQ"`
- `hs docs categories reorder <collection-id> --categories id1,id2,id3`

### Articles
- `hs docs articles list --collection <id>` or `--category <id>`
- `hs docs articles search --query "password reset" --site <id>`
- `hs docs articles get <id>` / `hs docs articles get <id> --draft`
- `hs docs articles create --collection <id> --name "How to reset" --text "Step 1..."`
- `hs docs articles update <id> --text "Updated..." --status published`
- `hs docs articles delete <id>`
- `hs docs articles draft save <id> --text "..."` / `hs docs articles draft delete <id>`
- `hs docs articles revisions list <id>` / `hs docs articles revisions get <id> <rev-id>`
- `hs docs articles upload <id> --file ./image.png`

### Redirects
- `hs docs redirects list <site-id>` / `hs docs redirects find --site <id> --url /old-path`
- `hs docs redirects create --site <id> --url-mapping /old --redirect /new`

### Assets
- `hs docs assets article upload --file ./img.png`
- `hs docs assets settings upload --file ./logo.png`

## Output & global flags

- `--format table|json|json-full|csv` — output format (default: `table`)
- `--no-paginate` — fetch all pages automatically
- `--page <n>` / `--per-page <n>` — pagination (defaults: 1, 25)
- `--debug` — show HTTP request/response details

## Config

- `hs config set --format json --inbox-default-mailbox 12345`
- `hs config get [key]` — print one or all config values
- `hs config path` — print config file location
- Default location: `~/.config/hs/config.yaml` (Linux/macOS), `%AppData%\hs\config.yaml` (Windows)

## PII redaction

Inbox commands redact customer/user PII with deterministic fake identities. Controlled via config key `inbox_pii_mode`.

| Mode | Effect |
|------|--------|
| `off` | No redaction (default) |
| `customers` | Redact customer names, emails, phones |
| `all` | Redact both customers and users |

- `--unredacted` flag on `hs inbox` disables redaction for one call (requires `inbox_pii_allow_unredacted: true` in config)

## Permissions

Allowlist model — restrict which commands an agent can run. Empty policy = unrestricted.

- Set via config key `inbox_permissions` / `docs_permissions` — comma-separated `resource:operation` pairs
- Wildcards: `*:read`, `conversations:*`
- Operations: `read`, `write`, `delete`, `*`
- `hs inbox permissions` — inspect current policy, shows ALLOW/DENY per command

Example: `hs inbox config set --inbox-permissions "conversations:read,customers:read,mailboxes:read"`

## Notes

- Self-update: `hs update`
- Shell completions: `hs completion bash|zsh|fish|powershell`
