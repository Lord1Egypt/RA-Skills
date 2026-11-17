---
name: outlook-contacts
license: MIT
description: |
  Read and write the signed-in user's Microsoft 365 / Outlook.com personal contacts via Microsoft Graph.
  No mail, no files, no directory access. This skill has its own contacts-scoped device-code
  login and token store.
  Use when the user wants to list/search Outlook.com contacts, find phone numbers, or look up email addresses.
  Trigger keywords: "outlook contacts", "ms contacts", "graph contacts", "我的联系人", "查联系人", "outlook 联系人".
metadata:
  openclaw:
    emoji: "👤"
    requires:
      bins: ["bash", "jq", "curl", "python3"]
    network:
      allow:
        - "https://login.microsoftonline.com"
        - "https://graph.microsoft.com"
    files:
      write:
        - "~/.outlook-contacts/"
---

# Outlook Contacts (Microsoft Graph, read & write)

A **contacts read-and-write** Microsoft Graph skill. Reads and writes the signed-in user's personal contacts
through `/me/contacts`. **Does not access mail/files/directory.**

This skill has its own device-code login and token store (`~/.outlook-contacts/`).
The consent requests exactly three delegated Microsoft Graph scopes:

| Scope | Why |
|---|---|
| `offline_access` | refresh_token for headless operation |
| `https://graph.microsoft.com/User.Read` | display signed-in account UPN |
| `https://graph.microsoft.com/Contacts.ReadWrite` | read and write personal contacts |

All write operations (create, update, delete) default to **dry-run**; you must pass `--apply` to execute.

## ⚠️ Safety rules

1. **Every write defaults to dry-run.** Pass `--apply` to execute. Create/update print the JSON payload first.
2. **Delete always shows the contact first**, then asks for a typed `YES` confirmation (or `--yes` for non-interactive use).
3. **No secrets in logs.** Tokens are never echoed; error bodies are sanitized.
4. **Token & config live under `~/.outlook-contacts/`** (chmod 700 dir, chmod 600 files).

## First-time setup

You need a **public client** application registration in Entra ID (Azure AD) with
"Allow public client flows" = **Yes** and device-code flow enabled. This skill uses
the **device code flow** so it works on a headless host.

Azure app registration steps (bring your own — required once):

1. Portal → **Microsoft Entra ID** → **App registrations** → **New registration**.
2. Supported account types: **"Accounts in any organizational directory and personal Microsoft accounts"**.
3. No redirect URI needed. In the app → **Authentication** → set **"Allow public client flows"** = **Yes**.
4. Copy the **Application (client) ID** — that is the `--client-id` below. No client secret is required.

The setup script requests exactly these delegated Microsoft Graph scopes:
`offline_access`, `User.Read`, `Contacts.ReadWrite`.

```bash
cd ~/.openclaw/skills/outlook-contacts
./scripts/setup-device-code.sh --client-id 12345678-1234-1234-1234-123456789012
# follow the printed URL, enter the code, finish the browser sign-in
```

The script writes:

| File | Mode | Content |
|---|---|---|
| `~/.outlook-contacts/config.json` | 600 | client_id, tenant, authority, scopes, graph_base |
| `~/.outlook-contacts/tokens.json` | 600 | access_token, refresh_token, expires_at, scope |

> **Important:** never commit `~/.outlook-contacts/` to git. Use `--force` to overwrite.

## Reading contacts

```bash
# List all contacts (paginated, max 200 per page)
./scripts/contacts-read.sh list --format summary

# Search contacts by name, email, or company
./scripts/contacts-read.sh search "jane" --format summary

# Filter by specific field
./scripts/contacts-read.sh list --filter "contains(displayName,'Zhang')" --format json

# Limit results
./scripts/contacts-read.sh list --limit 20 --format summary

# Raw JSON output
./scripts/contacts-read.sh list --format raw
```

`--format` options:

- `summary` (default) — compact table: name, email, phone, company, title
- `json` — pretty-printed full Graph JSON
- `simple` — one line per contact: "name <email> 📞phone"
- `raw` — single-line JSON array

### Format examples

**summary** (default):
```
NAME                 EMAIL                        PHONE            COMPANY         TITLE
----------------------------------------------------------------------------------------------------

Zhang San            zhang@example.com            13812345678      ABC Corp        Manager
Li Si                li@example.com               13987654321      -               -

Total: 2 contacts
```

**simple** — one line per contact with optional phone icon:
```
Zhang San <zhang@example.com> 📞13812345678
Li Si <li@example.com>
```

### Search syntax

The `search` subcommand uses Microsoft Graph's `$search` query parameter on the
`displayName` and `emailAddresses` fields:

```bash
./scripts/contacts-read.sh search "Wang" --format simple
./scripts/contacts-read.sh search "gmail.com" --format summary
```

### Filtering

The `--filter` option passes an OData `$filter` expression directly:

```bash
./scripts/contacts-read.sh list --filter "jobTitle eq 'Professor'" --format summary
./scripts/contacts-read.sh list --filter "startswith(givenName,'X')" --format json
```

## Writing contacts

**⚠️ Safety: every write defaults to dry-run. Pass `--apply` to execute.**

```bash
# Get a single contact (read-only, no --apply needed)
./scripts/contacts-write.sh get --contact-id "AAMk..."

# Update a contact (dry-run by default; see payload before applying)
./scripts/contacts-write.sh update --contact-id "AAMk..." \
  --email "new@example.com" --phone "13812345678"

# Actually update (after confirming dry-run output looks correct)
./scripts/contacts-write.sh update --contact-id "AAMk..." \
  --email "new@example.com" --phone "13812345678" --apply

# Create a new contact
./scripts/contacts-write.sh create --display-name "Zhang San" \
  --email "zhang@example.com" --phone "13912345678" --apply

# Delete a contact (always shows the contact first, then asks for YES confirmation)
./scripts/contacts-write.sh delete --contact-id "AAMk..." --apply
```

### Update fields available

- `--display-name` — full display name
- `--given-name` — first name
- `--surname` — last name
- `--email` — primary email (replaces existing email array)
- `--phone` — mobile phone number
- `--company` — company name
- `--job-title` — job title
- `--notes` — personal notes

## Token management

```bash
./scripts/token.sh status
./scripts/token.sh refresh
./scripts/token.sh scopes
./scripts/token.sh clear --yes-i-really-mean-it
```

## Files in this skill

| Path | Purpose |
|---|---|
| `SKILL.md` | this file |
| `scripts/setup-device-code.sh` | one-time device-code flow sign-in |
| `scripts/token.sh` | inspect / refresh / clear stored tokens |
| `scripts/_lib.sh` | shared helpers (sourced; not for direct use) |
| `scripts/contacts-read.sh` | `list` / `search` contacts via `/me/contacts` |
| `scripts/contacts-write.sh` | `get` / `update` / `create` / `delete` contacts |

## Troubleshooting

- **`token scope does not include Contacts.ReadWrite`** — re-run `./scripts/setup-device-code.sh --force` to re-authenticate.
- **Empty results** — check that contacts exist in Outlook.com under "People".
- **`401 Unauthorized`** — run `scripts/token.sh refresh --force`; if that fails, re-run `scripts/setup-device-code.sh --force`.
