---
name: inbox-cleanup
version: 1.0.5
metadata:
  openclaw:
    emoji: 📬
    requires:
      bins:
      - python3
      env:
      - IMAP_PASSWORD
    network:
      outbound: true
      reason: Connects to IMAP server (e.g. Proton Bridge on localhost) to read and
        delete/archive emails.
    primaryEnv: IMAP_PASSWORD
description: IMAP bulk email triage — pattern-based delete/archive with dry-run mode.
  Supports IMAP STARTTLS (e.g. Proton Bridge), dry-run preview, YAML/JSON config for
  patterns, and processes UIDs for reliable bulk ops.
---

# inbox-cleanup

Bulk IMAP email triage: classify → delete/archive by sender domain, subject keywords, or custom patterns.

---

## When to Use This / When NOT to Use This

**Use inbox-cleanup when:**
- You need to bulk-delete or archive 50+ emails matching a pattern (sender domain, subject keyword)
- The inbox has a large backlog from known noisy senders (GitHub notifications, Slack digests, newsletters)
- You want a dry-run preview before committing any destructive action
- You need reproducible triage logic stored as config (not one-off manual clicks)

**Do NOT use inbox-cleanup when:**
- Reading or searching for a specific email — use IMAP tools or webmail directly
- Triaging fewer than ~10 emails — just do it manually
- You want to reply, forward, or compose — this is delete/archive only
- You're unsure what's in the inbox — **always dry-run first**, never run live blind

**Boundary with other skills:** This skill does NOT read email content for decision-making (no NLP/LLM classification). It matches on sender domain and subject string patterns only. For content-aware triage, a different approach is needed.

---

## ⚠️ What NOT to Delete

Some email categories look like noise but must be preserved:

- **Transactional emails** — order confirmations, shipping notices, receipts (needed for expense tracking)
- **Auth codes / OTPs / 2FA emails** — one-time codes, password resets
- **Legal / compliance** — invoices, tax docs, terms-of-service change notices
- **Bank / financial** — statements, transaction alerts
- **Domain / hosting renewals** — expiry notices from registrars, DNS providers

**Safeguard pattern:** Add these sender domains to `leave_domains` in your config. When in doubt, archive instead of delete.

```yaml
leave_domains:
  - ato.gov.au          # Australian Tax Office
  - myob.com            # Accounting
  - godaddy.com         # Domain registrar
  - cloudflare.com      # DNS / hosting
  - stripe.com          # Payments
  - paypal.com          # Payments
  - no-reply@apple.com  # Apple receipts
```

---

## Key Files

- `scripts/inbox_cleanup.py` — main cleanup script (dry-run by default)
- `scripts/config_example.yaml` — pattern config template

## Quick Start

```bash
# Step 1: Always dry-run first — no changes made, just a preview
python3 scripts/inbox_cleanup.py --config my_patterns.yaml --dry-run

# Step 2: Review the output. If it looks right:
python3 scripts/inbox_cleanup.py --config my_patterns.yaml
```

---

## What a Successful Dry-Run Looks Like

When dry-run completes, you'll see output like:

```
[DRY RUN] Would delete 142 emails from github.com
[DRY RUN] Would delete 38 emails from slack.com
[DRY RUN] Would archive 17 emails from notion.so
[DRY RUN] Would archive 9 emails matching keyword "newsletter"
[DRY RUN] Skipping 3 emails from leave_domains (stripe.com, paypal.com)
─────────────────────────────────────────────
Total would-delete: 180
Total would-archive: 26
Total skipped (leave_domains): 3
```

If the numbers look wrong (e.g. 0 matches when you expected hundreds), check:
1. The `IMAP_HOST` / `IMAP_PORT` / `IMAP_USER` env vars are set
2. The sender domains in your config match exactly (e.g. `noreply.github.com` ≠ `github.com`)
3. The script connected to the right IMAP folder (default: INBOX)

---

## Required Env Vars

```bash
IMAP_HOST=127.0.0.1          # IMAP server host (127.0.0.1 for Proton Bridge local proxy)
IMAP_PORT=1143               # Port: 993 = direct SSL, 1143 = Proton Bridge STARTTLS
IMAP_USER=you@example.com    # Your IMAP login username
IMAP_PASSWORD=yourpassword   # IMAP password (use op read for 1Password)
IMAP_STARTTLS=true           # true = STARTTLS upgrade after connect (Proton Bridge); false = SSL-from-start
IMAP_SKIP_CERT_VERIFY=true   # true = accept self-signed cert (required for Proton Bridge)
ARCHIVE_FOLDER=Archive        # Exact IMAP folder name to move archived emails into (must already exist)
```

Or use `--imap-*` CLI flags. See `python3 scripts/inbox_cleanup.py --help`.

---

## Config File Format (YAML)

```yaml
# Sender domains whose emails should be permanently deleted
delete_domains:
  - github.com           # GitHub notifications (Issues, PRs, Actions)
  - noreply.github.com   # GitHub no-reply (different subdomain — list both if needed)
  - slack.com            # Slack digest/notification emails

# Sender domains whose emails should be moved to Archive (not deleted)
archive_domains:
  - notion.so            # Notion share notifications
  - coinbase.com         # Crypto price alerts

# Subject line keywords — emails matching any of these are archived (case-insensitive)
archive_keywords:
  - newsletter           # Matches "The Weekly Newsletter", "Newsletter #42", etc.
  - digest               # "Daily Digest", "Weekly Digest"
  - weekly roundup       # Exact substring match

# Subject line regex patterns — emails matching any of these are deleted
# Note: patterns are Python re.search() — anchored with ^ if you want start-of-line match
delete_subject_patterns:
  - "^\\[GitHub\\]"      # Subjects starting with "[GitHub]"

# Sender domains that should NEVER be touched — overrides all other rules
# Add banks, payment processors, auth providers, registrars here
leave_domains:
  - important-bank.com
  - stripe.com
  - paypal.com
```

---

## Design Notes

- **UIDs not sequence numbers**: The script always uses `UID FETCH`/`UID STORE` to
  avoid message-renumbering bugs when messages are deleted mid-batch.
- **Dry-run by default**: Always preview before committing. Pass `--no-dry-run` to apply.
- **Batch fetching**: Headers fetched in batches of 50 for large inboxes. One-at-a-time
  fetch mode available with `--one-at-a-time` for reliable UID tracking.
- **Progress logging**: Stdout log with counts per domain and final report JSON.
- **STARTTLS support**: Needed for Proton Bridge (port 1143 with self-signed cert).

---

## Secret Management

Credentials via env vars or 1Password:

```bash
# Via env vars
export IMAP_PASSWORD="$(op read 'op://Vault/Email Account/password')"
python3 scripts/inbox_cleanup.py --config patterns.yaml
```

---

## Common Mistakes

1. **Running live without a dry-run first**
   - Deleted emails may not be recoverable from all IMAP servers
   - Always run `--dry-run` first and review the counts

2. **Domain mismatch — listing `github.com` but emails come from `noreply.github.com`**
   - IMAP From headers often use subdomains. List both: `github.com` AND `noreply.github.com`
   - Run dry-run and check the "0 matches" — then inspect an actual email's From header

3. **`ARCHIVE_FOLDER` doesn't exist in the mailbox**
   - The script will error on archive operations if the folder isn't pre-created
   - Create the folder in webmail or your email client first

4. **Proton Bridge not running when script executes**
   - Port 1143 will refuse the connection
   - Ensure Proton Bridge desktop app is open and logged in before running

5. **`leave_domains` not populated**
   - Without `leave_domains`, the script will happily delete emails from payment processors, banks, and auth providers if they match another rule
   - Always populate `leave_domains` before any live run

6. **STARTTLS vs SSL confusion**
   - Direct IMAP SSL (Gmail, Fastmail): `IMAP_PORT=993`, `IMAP_STARTTLS=false`
   - Proton Bridge local proxy: `IMAP_PORT=1143`, `IMAP_STARTTLS=true`, `IMAP_SKIP_CERT_VERIFY=true`
   - Mixing these up causes connection failures or cert errors
