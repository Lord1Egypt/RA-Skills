# Okki Go Update Notification Scripts

These scripts manage automatic update notifications for the Okki Go skill.

## Compact Output Contract

Normal OKKI Go tool output must be compact and user-facing. Raw API JSON, long email bodies, full profile objects, full local state, and internal identifiers must not be streamed into the model unless the user explicitly asks for raw/debug output. For large raw data, save it to a local file and return a path plus a short summary.

Default private raw files should live under `/private/tmp/okki-go-batches`. Compact mode is a presentation filter, not data deletion: wrapper scripts save raw records or mappings when the compact output would otherwise omit private fields.

Compact wrapper stdout includes routing-critical fields such as `truncated`, `available`, `next_offset`, `discovery_health`, and `next_action`. Company discovery also includes `display_table_markdown`, a fixed Markdown result table rendered by scripts, and opaque `selection_handle` for preparing paid unlock plans. Debug fields such as `batch_id`, `raw_path`, `private_mapping_saved`, and `output_budget` appear only with `--debug-metadata`. Batch-producing scripts update a latest batch pointer with a default 24h TTL for free follow-up compatibility, but paid unlock execution should use prepared unlock plans. For company discovery, `target_count` defaults to 30; `low_yield_batch_streak` counts consecutive low-yield displayed result batches, not result rows or chat turns.

Default visible caps:

| Output type | Default visible cap | Raw handling |
|---|---:|---|
| Company rows | 30 by default, requested count when provided, hard cap 100 | Save raw batch file |
| Contacts | 20 visible, hard cap 100 | Save contact batch file |
| profileEmails | 20 visible per company, hard cap 100 | Save company contact file |
| Email task list | 20 tasks | Save raw status file |
| Email task detail mails | Show aggregate + failed rows first | Save full detail file |
| Single email body | Hidden unless explicitly requested | Truncate to 500 chars or save file |
| Viewed/Profile state | Counts/redacted fields only | Full state only under explicit debug/export |

## Prospecting Wrappers

Context Firewall preflight for large files, cross-skill output, stale prior state, or risky paid/send/write scope:

```bash
node scripts/okki-envelope.js validate --file /private/tmp/okki-go-context/envelope.json --compact
```

This command validates schema, action gates, confirmation scope, expiration, and supported fields. It never calls OKKI APIs and must run before high-risk action wrappers when an Action Envelope is used.

Single-page company search:

```bash
node scripts/search-companies.js \
  --json '<search-advanced payload>' \
  --compact \
  --locale '<user-locale>' \
  --target-count 30 \
  --fields company_name,country_name,has_email,has_whatsapp,employees_count,founding_time,company_type,fit \
  --limit-output 50 \
  --save-raw /private/tmp/okki-go-batches/search-raw.json
```

`--compact` omits `domain`, raw IDs, website/homepage/URL/link fields, exact email counts, and exact WhatsApp counts from stdout, then writes row-to-domain mapping plus raw records to `--save-raw`. Search rows expose `has_email` and `has_whatsapp` booleans to avoid presenting free-search counts as confirmed unlocked contact totals. Company discovery stdout also includes `display_table_markdown` with localized fixed columns: `row`, `company_name`, `country_name`, `company_type`, `fit`, `has_email`, `more_info`. `more_info` displays WhatsApp availability, employee count, and founding time with labels. `--locale` adds localized `country_name` values and display-table labels for user-facing display while preserving `country_code` for internal workflow use.

Batch discovery for "more", pagination-heavy, or count-based requests:

```bash
node scripts/discover-companies-batch.js \
  --plan /private/tmp/de-autoglass-plan.json \
  --target-count N \
  --save-batch /private/tmp/okki-go-batches/de-autoglass-20260604.json \
  --compact \
  --locale '<user-locale>'
```

The numeric values in examples are placeholders; scripts use the requested target count and generic row selectors such as `1,3,7-9`.

The batch script scans configured pages, deduplicates by domain then company name, saves private mapping, updates the latest batch pointer, creates a `selection_handle`, and emits compact rows plus scanned/deduped/returned counts.

Free company search retries one transient busy/rate-limit/upstream failure before surfacing the error. Batch discovery defaults to serial requests so large or split searches do not spike the upstream portrait-recall flow-control resource. Search wrappers split `companyTypeKeywords` to one value per API request to reduce enhanced-recall ES rewrite pressure. They reject compound phrases such as `汽车玻璃供应商` before API calls and require the caller to rewrite product/industry/application words into target-buyer `productKeywords` or `industryKeywords` plus pure role `companyTypeKeywords`. Use `--concurrency` only for internal debugging or a known-safe environment.

Prepare selected rows before asking for explicit credit confirmation:

```bash
node scripts/prepare-unlock-plan.js \
  --selection-handle HANDLE \
  --rows ROWS \
  --compact \
  --locale '<user-locale>' \
  --debug-metadata
```

Prepare a processed target set when recommendations, filtering, ranking, multi-page consolidation, or user edits produce the final companies to unlock:

```bash
node scripts/prepare-unlock-plan.js \
  --selection-set-file /private/tmp/okki-go-batches/final-unlock-targets.json \
  --compact \
  --locale '<user-locale>' \
  --debug-metadata
```

Unlock the prepared plan after explicit credit confirmation:

```bash
node scripts/unlock-companies.js \
  --plan PLAN_ID \
  --mark-unlocked \
  --compact \
  --locale '<user-locale>' \
  --artifact-dir '<agent-visible-output-dir>'
```

`prepare-unlock-plan.js` freezes row selections or a processed target set into an opaque `unlock_plan_id` without calling paid APIs. Normal output shows `selected_companies` and `max_credit_cost`; the plan id and target-set fingerprint are only under `debug_metadata` for the agent to use after confirmation. If the user changes the final targets before confirmation, prepare a new plan; active-plan state rejects the old one. `unlock-companies.js --plan` reads that frozen mapping, calls paid `/companies/unlock`, fetches profile/profileEmails/balance for successful rows, uses `mark-unlocked-batch` only for successful rows, and emits charge/balance/company summaries. Compact output hides `raw_path` unless `--debug-metadata` is explicit; it never prints `domain` or `companyHashId`. The only valid source for `companyHashId` is the `/companies/unlock` response; never use free-search ID/raw `id`, domain, row number, or model memory as `companyHashId`. The skill workflow must still ask explicit paid confirmation before calling it.

After unlock, normal compact output uses script-rendered `unlock_details_markdown` plus compatibility `company_details`, not a model-built unlock-result table. The script shows at most the first 5 successful company details in stdout and writes all successful company details plus any failure/not-executed rows to a Markdown document at `details_markdown_path`. The top summary shows planned, success, failure, charge, and balance; failed or not-executed rows appear only when present. `next_action` is `draft_outreach` when at least one company succeeds. The Markdown document is the user-facing full-detail artifact; raw JSON remains for debug/recovery only. Unlocked details may show `display_website`, derived from profile website, profile domain, or the saved search domain.

Details Markdown artifact path order is `--markdown-file`, then `--artifact-dir`, then `OKKIGO_ARTIFACT_DIR`, then current working directory `okki-go-artifacts/`, then internal temporary storage. `unlock-companies.js` preflights the selected details Markdown path before paid API calls. If an explicit or default artifact path is not writable, it falls back to internal temporary storage and emits a warning. If no details Markdown path is writable, it exits before paid API calls with `DETAILS_MARKDOWN_PRECHECK_FAILED`, `paid_api_called: false`, `unlock_executed: false`, `next_action: "authorize_artifact_dir"`, and a recovery suggestion.

`--mark-unlocked` is local viewed-state bookkeeping for `${XDG_CONFIG_HOME:-$HOME/.config}/okki-go/viewed.json`; it is not part of the paid unlock transaction. In restricted sandboxes, callers can preflight that file or its parent directory and request file_system write permission before running a confirmed unlock. If the local state write fails after the unlock API succeeds, `unlock-companies.js` still exits 0, preserves `charged_count`, `charged`, `balance`, and the saved raw file, and emits `state_update_failed` plus a warning. Do not retry `/companies/unlock` to repair local viewed state.

Cross-company contact search after first-session paid confirmation:

```bash
node scripts/search-contacts.js \
  --json '{"title":"Procurement Manager","country_codes":"DE","has_email":1,"size":20}' \
  --save-batch /private/tmp/okki-go-batches/contacts-de-procurement-20260604.json \
  --compact
```

Default visible size is 20; requested contact search size may be up to 100. Internal contact IDs are saved in the raw file, not stdout. Phone numbers are hidden unless `--include-phone` is used because the user requested phone/contact details.

Email status:

```bash
node scripts/email-status.js tasks --json '{"page":1,"page_size":20}' --compact
node scripts/email-status.js task --task-id 1001 --compact
node scripts/email-status.js mails --json '{"statuses":"failed","page":1,"page_size":20}' --compact
node scripts/email-status.js mail --mail-id 2001 --compact
```

Email bodies are omitted by default. Use `--include-body` only when the user explicitly asks to view the body; the preview is capped at 500 characters and raw detail is saved to a file.

Email send after explicit recipient and content confirmation:

```bash
node scripts/send-email.js batch --json '<payload>' --mapping-file /private/tmp/okki-go-batches/email-send.json --compact
node scripts/send-email.js personalized --file /private/tmp/personalized-send.json --compact
```

Post-send output summarizes task IDs/counts and mapping path. It does not echo full email bodies or all recipient variables.

Compact viewed state writes:

```bash
node scripts/okki-state.js viewed mark-unlocked --domain a.de --country-code DE --compact
node scripts/okki-state.js viewed mark-unlocked-batch --json '[{"domain":"a.de","country_code":"DE"}]'
node scripts/okki-state.js viewed classify --results-file /tmp/results.json --compact
```

## File Overview

| File | Platform | Description |
|------|----------|-------------|
| `enable-notifications.sh` | macOS / Linux | Enable/manage update notifications |
| `enable-notifications.ps1` | Windows | Enable/manage update notifications (PowerShell) |
| `check-update.sh` | macOS / Linux | Manually check for updates |
| `check-update.ps1` | Windows | Manually check for updates (PowerShell) |
| `post-install.sh` | macOS / Linux | Post-install initialization (optional) |
| `post-install.ps1` | Windows | Post-install initialization (optional) |

## Quick Start

### First Use After Installation

**Recommended:** Run the post-install initialization script (guided setup)

**macOS / Linux:**
```bash
bash scripts/post-install.sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy Bypass -File scripts\post-install.ps1
```

This script will:
1. Confirm the skill installation location
2. Ask whether to enable update notifications
3. Guide you through API Key configuration

### Enable Notifications Manually

**macOS / Linux:**
```bash
bash scripts/enable-notifications.sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy Bypass -File scripts\enable-notifications.ps1
```

**Windows (Git Bash):**
```bash
bash scripts/enable-notifications.sh
```

### Check for Updates Manually

**macOS / Linux:**
```bash
bash scripts/check-update.sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-update.ps1
```

## Features

### After Enabling Notifications

- **Check frequency**: Every Monday at 10:00 AM automatically
- **Notification content**:
  - Current version vs. latest version
  - Changelog preview
  - One-command update
- **Delivery method**: OpenClaw message push

### Management Options

After running the `enable-notifications` script, you can choose:

1. **Disable notifications** - Turn off update reminders completely
2. **Change frequency** - Switch to daily/weekly/monthly checks
3. **Check now** - Immediately check for updates
4. **Exit** - Make no changes

## Customize Check Frequency

Adjust the check frequency by modifying the cron job:

| Frequency | Cron Expression | Description |
|-----------|----------------|-------------|
| Daily | `0 10 * * *` | Every day at 10:00 AM |
| Weekly | `0 10 * * 1` | Every Monday at 10:00 AM (default) |
| Monthly | `0 10 1 * *` | 1st of every month at 10:00 AM |

Run the management script and choose option 2 to change it.

## FAQ

### Q: How should I configure the OKKI Go API Key?
A: Prefer the Codex-style local login helper. Run it from the installed OKKI Go skill directory:

```bash
printf '%s\n' 'sk-xxx' | node scripts/okki-auth.js login --with-api-key
```

This stores the key in `${XDG_CONFIG_HOME:-$HOME/.config}/okki-go/credentials.json` and writes non-secret source metadata to `auth-source.json`. Both files use mode `0600`.

Explicit platform/environment sources are still supported:

1. Platform secrets/config injection as `OKKIGO_API_KEY`
2. Environment variable: `export OKKIGO_API_KEY="sk-xxx"`
3. Legacy local fallback file: `~/.config/okki-go/credentials.json` with mode `0600`

The runtime resolver does not scan platform-specific config directories. Platforms should inject `OKKIGO_API_KEY` or register a non-secret source during setup.

Verify without printing the secret:

```bash
bash scripts/resolve-api-key.sh --check
bash scripts/resolve-api-key.sh --source
node scripts/okki-auth.js status --json
node scripts/okki-auth.js doctor --json
```

### Q: "openclaw command not found"?
A: Make sure OpenClaw is installed:
```bash
npm install -g openclaw
```

### Q: Not receiving notifications?
A: Check that the OpenClaw gateway is running:
```bash
openclaw gateway status
```

### Q: How to disable notifications completely?
A: Run the management script and choose option 1, or delete the cron job directly:
```bash
openclaw cron list  # find the job ID
openclaw cron remove --jobId <ID>
```

### Q: Can I use this on multiple devices?
A: Yes. Run the enable script once on each device.

## Create Notifications Manually

If the script cannot run, create manually:

```bash
openclaw cron add \
  --name "okkigo-update-reminder" \
  --schedule "0 10 * * 1" \
  --payload "clawhub search okki-go --limit 1" \
  --delivery "announce"
```

## Privacy

- Scripts do not collect any personal information
- Will not auto-update the skill — notifications only
- Update decisions are entirely user-controlled
- Checks query only publicly available version information

## Support

For issues, visit:
- Project homepage: https://go.okki.ai
- Documentation: https://docs.openclaw.ai
