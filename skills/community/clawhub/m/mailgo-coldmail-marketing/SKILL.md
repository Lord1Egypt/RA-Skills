---
name: mailgo-campaign-suite
description: Complete cold email campaign suite for Mailgo — verify recipients, claim free mailbox, generate & optimize content, create campaigns, manage lifecycle, and view reports. All-in-one skill that handles the full outreach pipeline end-to-end. Use when a user wants to send cold emails, launch outreach campaigns, or manage existing campaigns.
env:
  MAILGO_API_KEY:
    required: true
    description: >
      Mailgo OpenAPI Key. Obtain from https://app.mailgo.ai → Click avatar
      in bottom-left corner → Personal Tokens → Create Token. Used as
      X-API-Key header for all Mailgo API calls (api.leadsnavi.com).
      Never paste into chat — set as local env var only.
dependencies:
  python: ">=3.7"
  optional:
    - openpyxl  # for .xlsx file support
---

# Mailgo Campaign Suite

One skill, complete cold email pipeline. From recipient verification to campaign reporting — everything runs through bundled scripts with zero third-party dependencies.

---

## Step 0 — Authentication Setup

**Required:** `MAILGO_API_KEY` environment variable must be set before any other step.

### Quick check

```bash
# Confirm the variable is set (shows first 5 characters only)
echo "${MAILGO_API_KEY:0:5}"
```

If output is non-empty → proceed to Step 1. If empty → follow the setup flow below.

### Setup Flow

**Sub-step 0.1 — Register or Log In**

New users:
1. Go to [https://app.mailgo.ai](https://app.mailgo.ai)
2. Click "Sign Up" and complete registration

Existing users:
1. Go to [https://app.mailgo.ai](https://app.mailgo.ai)
2. Log in with your credentials

**Sub-step 0.2 — Create Personal Token**

Once logged in:
1. Click your **avatar** in the bottom-left corner
2. Select **Personal Tokens** from the menu
3. Click **Create Token**
4. Give your token a descriptive name (e.g., "Claude Code")
5. Copy the generated token

> **SECURITY:** Never paste the token into chat. It must only be set as a local environment variable.

**Sub-step 0.3 — Set Environment Variable**

```bash
# macOS / Linux (permanent)
echo 'export MAILGO_API_KEY="YOUR_TOKEN"' >> ~/.zshrc && source ~/.zshrc

# Windows PowerShell (permanent)
[System.Environment]::SetEnvironmentVariable('MAILGO_API_KEY', 'YOUR_TOKEN', 'User')
```

Replace `YOUR_TOKEN` with the copied value.

**Sub-step 0.4 — Verify**

```bash
# macOS / Linux — shows first 5 characters to confirm without exposing the token
echo "${MAILGO_API_KEY:0:5}"

# Windows PowerShell
$k = $env:MAILGO_API_KEY; if ($k) { $k.Substring(0, [Math]::Min(5, $k.Length)) } else { "" }
```

If output is non-empty, you're ready. If empty, run `source ~/.zshrc` or open a new terminal.

### Key Facts

| Item | Value |
|------|-------|
| Token source | app.mailgo.ai → Avatar → Personal Tokens |
| Env variable name | `MAILGO_API_KEY` |
| API header | `X-API-Key: {MAILGO_API_KEY}` |
| Token scope | Your Mailgo account (mailboxes, campaigns, reports) |
| Revoke token | app.mailgo.ai → Avatar → Personal Tokens → Delete |

### Auth Error Handling

| Issue | Fix |
|-------|-----|
| Empty after `source ~/.zshrc` | Open a new terminal window |
| 401 Unauthorized | Token may be invalid or deleted — create a new one in Personal Tokens |
| 403 Forbidden | Ensure `User-Agent` header is set (scripts handle this automatically) |

---

## Step 0.5 — Upfront Information Gathering

**Collect all required information in a single interaction before starting the pipeline.**

Ask all questions at once. Do not ask in separate rounds. The user fills in what they know; mark anything skipped as "not provided".

> **When to run:** Only when the user intends to create a new campaign. Skip for report/manage/replies tasks.

---

### Group A — Your Information (for email signature & credibility)

Ask all of these together in one message:

| # | Question | Field | Required? |
|---|----------|-------|-----------|
| 1 | What is your **company name**? | `sender_company` | Yes |
| 2 | What is **your name** (for the signature)? | `sender_name` | Yes |
| 3 | What does your company **offer** (products / services)? | `sender_offerings` | Yes |
| 4 | What is your **job title**? | `sender_title` | Recommended |
| 5 | What is your company **website**? | `sender_website` | Recommended |
| 6 | Any notable **clients, certifications, or metrics** to mention? | `sender_proof` | Optional |

---

### Group B — Your Recipients

Ask all of these together in the same message as Group A:

| # | Question | Field |
|---|----------|-------|
| 7 | Who are you sending to? Paste emails, or provide a file path (CSV / XLSX / TXT). | `recipients` |
| 8 | What is the **goal** of this campaign? (one sentence) | `campaign_purpose` |
| 9 | Do your recipients have **names** available? (column name or yes/no) | `has_name` |
| 10 | Do you have recipients' **company names**? (column name or yes/no) | `has_company` |
| 11 | Do you have recipients' **job titles**? (column name or yes/no) | `has_title` |
| 12 | Do you have recipients' **company websites / domains**? (column name or yes/no) | `has_domain` |

> If the user provides a file, auto-detect columns after reading the file headers — then mark fields 9–12 automatically without asking again.
>
> **⚠ Header Warning:** Column detection relies entirely on header names. Files without headers (e.g. a bare two-column XLSX with email + company but no row of column names) will only have `col_0`, `col_1`, … as synthetic headers — none of which match any known field name. As a result, **only the email column can be identified by content scanning; all other columns (company, name, title, domain) will be silently discarded.**
> Whenever a user provides a headerless file and you can see that extra columns exist (e.g. "two-column spreadsheet"), **proactively warn them**:
> _"Your file appears to have no header row. Only email addresses were imported — company names and other fields were not recognized. Add a header row (e.g. `email`, `company`, `name`) and re-upload to include that data."_

---

### Auto-Derive Name from Email Prefix (CRITICAL)

**Immediately after receiving the recipient list**, check whether name data is available.
If `has_name` is false (no name column detected, no names provided inline):

1. Extract name from each email's local-part (the portion before `@`):
   - Split on `.`, `-`, `_` → capitalize each segment → join with space
   - Examples: `alice.smith@co.com` → `"Alice Smith"`, `john_doe@co.com` → `"John Doe"`, `jdoe@co.com` → `"Jdoe"`
2. Store the derived name into each recipient entry in `session_context.recipients`
3. Set `recipient_fields.name = true` with source noted as `"auto-derived from email prefix"`
4. **Do this silently** — do not ask the user, do not announce it; just note it in the Step 3 change summary

This ensures `#{Name}` is **always available** as long as there are valid email addresses.

---

### Handling Partial Answers

| Situation | Action |
|-----------|--------|
| User skips a **required** field (1, 2, 3, 7, 8) | Ask once more specifically for that field only |
| User skips a **recommended** field (4, 5) | Mark as not provided, do not ask again |
| User skips an **optional** field (6) | Mark as not provided, move on |
| User says "I'll send to a file I haven't uploaded yet" | Ask for file path, then detect columns |
| User provides inline recipients with no extra data | Auto-derive names from email prefixes (see above); mark fields 10–12 as not provided |
| User provides a file **without a header row** and extra columns are present | Warn: only emails were imported; other columns were discarded. Ask user to add a header row (`email`, `company`, `name`, etc.) and re-upload |

---

### Carry Forward

Store all answers as session context. **Every subsequent step uses this context directly — never ask for the same information again.**

```
session_context = {
  sender_company:   "...",   # or null
  sender_name:      "...",   # or null
  sender_title:     "...",   # or null
  sender_website:   "...",   # or null
  sender_offerings: "...",   # or null
  sender_proof:     "...",   # or null
  recipients: [              # each entry always has a name (user-provided or auto-derived)
    { email: "...", name: "...", company: "...", title: "...", domain: "..." },
    ...
  ],
  campaign_purpose: "...",
  recipient_fields: {
    name:    true,           # ALWAYS true — either user-provided or auto-derived from email prefix
    company: true/false,
    title:   true/false,
    domain:  true/false,
  }
}
```

---

## Step 1 — Verify Recipient Emails

**Always verify before sending to >10 recipients.**

### Use the bundled script (MANDATORY)

```bash
source ~/.zshrc

# Option A: inline emails
python3 scripts/verify_emails.py alice@example.com bob@gmail.com

# Option B: from file (TXT/CSV/JSON)
python3 scripts/verify_emails.py --file leads.csv

# Option C: override column detection
python3 scripts/verify_emails.py --file leads.csv --email-column "Email Address"
```

**Script flags:**

| Flag | Default | Description |
|------|---------|-------------|
| `emails` | — | Space-separated email addresses |
| `--file` | — | Read from TXT/CSV/JSON file |
| `--email-column` | auto-detect | Override email column name |
| `--timeout` | 180 | Poll timeout in seconds |
| `--interval` | 5 | Poll interval in seconds |

**Output:** JSON on stdout with categorized results:
```json
{
  "total": 5,
  "valid": [{"email": "...", "status": "VALID"}],
  "invalid": [...],
  "domain_error": [...],
  "unknown": [...],
  "unchecked": [...]
}
```

### Email Status Values

| Status | Meaning | Recommendation |
|--------|---------|----------------|
| `VALID` | Confirmed deliverable | Send |
| `UNKNOWN` | Catch-all or greylisting | Send with caution |
| `DOMAIN_ERROR` | No MX records | Do not send |
| `INVALID` | Malformed or SMTP-rejected | Do not send |
| `UNCHECKED` | Still processing | Wait or re-poll |

**Filtering guidance:** Conservative = `VALID` only. Aggressive = `VALID` + `UNKNOWN`.

### Behavior Rules
- Never report results while `UNCHECKED` entries remain (unless timeout)
- Show progress during polls: "Verifying... X/total processed"
- Ask before filtering: "Found N undeliverable addresses. Remove them?"
- Credit error = stop immediately
- UNKNOWN is not a hard block — explain the tradeoff

### API Details (edge cases only)
- **Submit:** `POST /sirius/api/biz/email/verification` — body: `{"emails": [...]}`
- **Poll:** `GET /sirius/api/biz/email/verification/task/{taskId}`
- Max 10,000 emails per task; script auto-batches larger lists
- 120 req/min rate limit; on 429 wait 60s

---

## Step 2 — Claim Free Pre-Warmed Mailbox

**Run before creating any campaign.** Each user gets one free mailbox (60 days, 90+ sender score).

### Use the bundled script (MANDATORY)

```bash
source ~/.zshrc

# Claim (idempotent — safe to run multiple times)
python3 scripts/claim_free_mailbox.py

# JSON output for scripting
python3 scripts/claim_free_mailbox.py --json
```

**What you get:**
- Pre-warmed mailbox with 90+ sender score
- 60-day validity, no credit card required
- Idempotent: re-running returns the same mailbox
- stdout outputs just the email address (for piping)

> **Note:** The free mailbox uses a **randomly assigned domain** (e.g. `you@randomdomain.io`) which may not match your company domain. If brand consistency matters, consider purchasing a dedicated domain at https://app.mailgo.ai.

### Auto-integration
After claiming, use the returned email as `--sender` in Step 4:
```bash
SENDER=$(python3 scripts/claim_free_mailbox.py)
python3 scripts/run_campaign.py --sender "$SENDER" ...
```

### API Details (edge cases only)
- **Endpoint:** `POST /api/biz/benefits/assign-prewarm`
- **Auth:** `X-API-Key: {key}`
- **Response:** `{"code": 0, "data": "email@domain.com"}`
- `data: null` = pool empty, contact support

---

## Step 3 — Generate & Optimize Email Content

**This is a knowledge-and-rewrite step. No API calls. No scripts.**

Apply the 6-step optimization pipeline to user content, or generate from scratch.

### Prerequisites for Generation — Use Session Context (CRITICAL)

All sender and recipient information was collected in **Step 0.5**. Do NOT ask again.

Read directly from `session_context`:

| Context field | Use in email |
|---------------|--------------|
| `sender_name` | Signature name |
| `sender_title` | Signature title (omit if null) |
| `sender_company` | Signature company + body references |
| `sender_website` | Signature website (omit if null) |
| `sender_offerings` | Value bridge paragraph |
| `sender_proof` | Proof point sentence (omit if null) |
| `recipient_fields.name` | **Always `true`** — use `#{Name}` unconditionally (user-provided or auto-derived from email prefix in Step 0.5) |
| `recipient_fields.company` | Use `#{Company Name}` only if `true` |
| `recipient_fields.title` | Use `#{Title}` only if `true` |
| `recipient_fields.domain` | Use `#{Domain}` only if `true` |

> If `session_context` is missing (e.g. user jumped directly to Step 3), collect the missing fields inline — but only the ones not yet known.

### Template Variables and Placeholder Rules (CRITICAL)

Mailgo uses `#{...}` placeholders that are resolved server-side at send time:

| Placeholder | Description | Resolved from |
|-------------|-------------|---------------|
| `#{Name}` | Recipient's name | `contactName` in leads data |
| `#{Company Name}` | Company name | `companyName` in leads data |
| `#{Domain}` | Company website | `domain` in leads data |
| `#{Title}` | Job title | `title` in leads data |
| `#{Email}` | Email address | `contactEmail` in leads data |

**CRITICAL — Conditional Placeholder Rule:**
- **ONLY use a `#{...}` placeholder if the corresponding data is confirmed available** (either from the file columns or user-provided inline data).
- **If a field has NO data, NEVER use its `#{...}` placeholder.** The placeholder will resolve to empty string at send time, creating ugly output like `，您好` or `关于  的合作`.
- **Exception: `#{Name}` is ALWAYS available.** Every recipient has a name — either provided by the user or auto-derived from the email prefix in Step 0.5. Never fall back to `"您好"` when you have email addresses.
- For other fields, use a generic alternative:

| Placeholder | If data available | If data NOT available |
|-------------|-------------------|----------------------|
| `#{Name}` | `#{Name}，您好` | _(never happens — always use `#{Name}`)_ |
| `#{Company Name}` | `关于 #{Company Name} 的合作` | `关于贵公司的合作` / `About a potential partnership` |
| `#{Domain}` | `我浏览了 #{Domain}` | Omit this sentence entirely |
| `#{Title}` | `作为 #{Title}` | Omit or use generic phrasing |

**Log placeholder decisions** in the change summary:
```
Placeholders used: #{Name} (data available), #{Email} (always available)
Placeholders skipped: #{Company Name} (no data), #{Title} (no data), #{Domain} (no data)
```

### Optimization Pipeline (execute ALL 6 steps, in order)

**Step 3.1 — Normalize**
- Plain text input → wrap in HTML skeleton (see below)
- HTML input → preserve structure

**Step 3.2 — Spam Trigger Scan**
- Scan subject + body against `resources/spam-triggers.md`
- Replace each trigger with neutral alternative
- Log every replacement

Key replacements (most common):

| Trigger | Replacement |
|---------|-------------|
| `free` / `free trial` | `included` / `trial period` |
| `Click here` | `Learn more` / `See details` |
| `Act now` | `When you're ready` |
| `Limited time` | `While available` |
| `Guaranteed` | `Proven` |
| `Dear friend` | `Hi #{Name}` |
| ALL CAPS words | Sentence case |
| `!!!` / `???` | Single punctuation |

Full replacement table: `resources/spam-triggers.md`

**Step 3.3 — HTML Cleanup**
- Remove: `<script>`, `<style>`, `<meta>`, `<link>`, `<iframe>`, `<embed>`, `<object>`
- Remove: event handlers (`onclick`, `onload`, etc.)
- Convert `<style>` blocks → inline styles, then remove block
- Remove: HTML comments, CSS `!important`, base64 images
- Ensure: all `<img>` have `alt` attributes

**Step 3.4 — Structure Check**
- Text-to-image ratio > 60% text (warn if image-heavy)
- Cold email target: < 150 words (flag if > 200)
- One CTA only (suggest consolidation if multiple)
- **Placeholder Data Validation** — scan all `#{...}` in the content against `session_context.recipient_fields`:
  - `#{Name}` and `#{Email}` → always safe, never touch
  - `#{Company Name}` → if `recipient_fields.company == false`: replace with generic text (e.g. `贵公司` / `your company`); log the replacement
  - `#{Domain}` → if `recipient_fields.domain == false`: remove the sentence containing it entirely; log the removal
  - `#{Title}` → if `recipient_fields.title == false`: replace with generic phrasing or omit; log the replacement
  - If data IS available for a placeholder: preserve it unchanged

**Step 3.5 — Link Audit**
- Replace URL shorteners (bit.ly, t.co, tinyurl, goo.gl, ow.ly) with full URLs
- Warn if > 3 links in cold email
- Remove `javascript:` and `data:` URLs

**Step 3.6 — Final Polish**
- Add soft opt-out line if missing (see below)
- Verify HTML is well-formed
- Write to `/tmp/email_optimized_<timestamp>.html`

### Content Generation (from scratch)

Generate **4 subject line variants** for A/B testing. Adapt based on available data:

**If `#{Company Name}` data IS available:**

| # | Strategy | Example |
|---|----------|---------|
| 1 | Value proposition | `How #{Company Name} can cut onboarding time by 60%` |
| 2 | Industry insight | `A shift I'm seeing in #{Company Name}'s space` |
| 3 | Case study / metrics | `How [similar company] grew pipeline 3x in 90 days` |
| 4 | Curiosity / question | `Quick question about #{Company Name}'s [process]` |

**If `#{Company Name}` data is NOT available:**

| # | Strategy | Example |
|---|----------|---------|
| 1 | Value proposition | `Cutting onboarding time by 60% — here's how` |
| 2 | Industry insight | `A shift I'm seeing in the [industry] space` |
| 3 | Case study / metrics | `How [similar company] grew pipeline 3x in 90 days` |
| 4 | Curiosity / question | `A quick question about your [process]` |

**Subject rules:** 40-50 chars, always personalize with `#{Name}` (always available); use `#{Company Name}` only if data available. No ALL CAPS, no spam triggers, no fake Re:/Fwd:.

**Body structure (adapt based on available fields):**
```
1. Personal opener (1 sentence)
   - ALWAYS use "#{Name}，您好：" — #{Name} is always available (user-provided or auto-derived)
   - WITH #{Company Name}: reference it in opener
   - WITHOUT #{Company Name}: use generic "贵公司" / "your company" or omit

2. Value bridge (1-2 sentences) — connect their situation to your offering
3. Proof point (1 sentence) — specific metric or case study (use sender_proof if available)
4. Soft CTA (1 sentence) — question, not demand
5. Signature — use actual sender_name + sender_title + sender_company (NEVER use placeholders like [Name])
6. Soft opt-out
```

**Body rules:** under 150 words, conversational tone, one CTA. All sender info in signature must be real data, not placeholders.

**Select industry template** from `resources/industry-templates.md` based on user's offerings.

### HTML Skeleton

Use for plain-text wrapping or building from scratch:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0; padding:20px; font-family:Arial, sans-serif; font-size:14px; line-height:1.6; color:#333333;">
  <div style="max-width:600px; margin:0 auto;">

    <!-- EMAIL CONTENT HERE -->

  </div>
</body>
</html>
```

### Soft Opt-Out Line

Always add after signature if missing:
```
P.S. If this isn't relevant, just reply and let me know — I won't reach out again.
```

### Change Summary Format

```
Email Optimization Complete
---
Industry template: SaaS / Software (matched from "AI deployment platform")
Sender info: Zhang Wei, Sales Director, TirePro Technologies (www.tirepro.com)
Recipient data available: name (auto-derived from email prefix), company (no), title (no), domain (no)
Placeholders used: #{Name} (auto-derived from email prefix — e.g. alice.smith@co.com → "Alice Smith")
Placeholders skipped: #{Company Name}, #{Title}, #{Domain} (no data — generic wording used)
Spam triggers replaced: 3
  - "free trial" → "trial period"
  - "Click here" → "Learn more"
  - "Act now" → "When you're ready"
HTML issues fixed: 1
  - Removed <script> tag
Structure: 118 words (OK)
Links: 2 (OK)
Opt-out: Added
Subjects generated: 4 variants

Output: /tmp/email_optimized_1711468800.html
→ Use with: --body-file /tmp/email_optimized_1711468800.html
```

### Severity Levels

| Level | Issues |
|-------|--------|
| **Critical** (must fix) | `<script>` tags, shortener URLs, base64 images, `javascript:` URLs, "This is not spam", `#{Company Name}`/`#{Domain}`/`#{Title}` placeholders with no corresponding recipient data |
| **Warning** (recommend) | Spam trigger words, image-heavy, >3 links, missing opt-out |
| **Info** | Word count >150, multi-punctuation, subject line suggestions |

### Behavior Rules
- Run automatically before every campaign send, even if not asked. Report "0 issues found" if clean.
- If user says "don't change my content": scan and **report** only, do not modify.
- Never change meaning. Replace words, don't rewrite paragraphs.
- **Placeholder rule differs by scenario:**
  - **Generating content from scratch:** NEVER write a `#{...}` placeholder unless the corresponding `recipient_fields` value is `true`. Use the generic alternatives from the Placeholder Rules table instead.
  - **Optimizing existing content:** if the content already contains a `#{...}` placeholder with NO data available, MUST replace it with the generic alternative (Step 3.4 Placeholder Data Validation). Do not silently preserve it — an unresolved placeholder will appear as a blank gap to the recipient.
  - **Exception: `#{Name}` and `#{Email}` are always safe** — never remove or replace them.
- **NEVER use `[bracketed placeholders]` like `[Name]`, `[Company]`, `[Title]` in final email output.** These must be replaced with actual sender data or omitted. They are template authoring aids, not send-time variables.
- Always use actual sender info (name, title, company, website) in the email signature — collected from the user in the Prerequisites step.
- Write HTML to `/tmp/email_optimized_<timestamp>.html` and use via `--body-file`.

---

## Step 4 — Create & Send Campaign

### Use the bundled script (MANDATORY)

```bash
source ~/.zshrc

# Option A: inline recipients
python3 scripts/run_campaign.py \
    --sender "claimed@mailbox.com" \
    --subject "Quick question about #{Company Name}" \
    --body-file /tmp/email_optimized_1711468800.html \
    --recipients "alice@example.com,bob@test.com" \
    --campaign-name "SaaS Outreach Mar 2026" \
    --daily-limit 50

# Option B: recipients from file (CSV/XLSX/TXT/JSON)
python3 scripts/run_campaign.py \
    --sender "claimed@mailbox.com" \
    --subject "Quick question about #{Company Name}" \
    --body-file /tmp/email_optimized_1711468800.html \
    --recipients-file leads.xlsx \
    --campaign-name "SaaS Outreach Mar 2026"
```

**Script flags:**

| Flag | Default | Description |
|------|---------|-------------|
| `--sender` | required | Sender email (from Step 2) |
| `--subject` | required | Subject line |
| `--body` | — | HTML body (or use `--body-file`) |
| `--body-file` | — | Read body from file (from Step 3) |
| `--recipients` | — | Comma-separated emails |
| `--recipients-file` | — | CSV/XLSX/TXT/JSON file |
| `--email-column` | auto | Override email column name |
| `--name-column` | auto | Override name column name |
| `--company-column` | auto | Override company column name |
| `--title-column` | auto | Override title/job column name |
| `--domain-column` | auto | Override domain/website column name |
| `--recipient-names` | auto from email | Comma-separated display names |
| `--recipient-companies` | — | Comma-separated company names |
| `--recipient-titles` | — | Comma-separated job titles |
| `--recipient-domains` | — | Comma-separated company websites |
| `--campaign-name` | "Campaign" | Display name |
| `--timezone-id` | Asia/Singapore | Timezone |
| `--timezone-offset` | +08:00 | UTC offset |
| `--send-days` | 1,2,3,4,5 | Days (1=Mon...7=Sun) |
| `--send-hours` | 9,18 | Start,end hour |
| `--daily-limit` | 50 | Daily send limit |
| `--no-tracking` | off | Disable open/click tracking |
| `--dry-run` | off | Create but do not activate |

**Output:** JSON summary with `campaignId`, `emailContentId`, lead counts, activation status.

### Agent Decision Framework

All campaign inputs were collected in **Step 0.5**. Use `session_context` directly.

**From session_context (never ask again):**
- Recipients — `session_context.recipients`
- Purpose/goal — `session_context.campaign_purpose`
- Sender info — `sender_company`, `sender_name`, `sender_title`, `sender_website`, `sender_offerings`, `sender_proof`
- Recipient field availability — `recipient_fields.{name, company, title, domain}`

**Auto-inferred (never ask):**
- Sender email — auto-assigned from Step 2 (free mailbox)
- Subject — generate from `campaign_purpose` (Step 3), using only placeholders with confirmed `recipient_fields`
- Body — generate personalized HTML (Step 3), respecting `recipient_fields` availability
- Campaign name — derived from `campaign_purpose` + current month (e.g. "Tire Outreach Mar 2026")
- Schedule — Mon-Fri 9am-6pm, Asia/Singapore timezone
- Daily limit — 50 for new accounts
- Tracking — open + click ON

### Decision Flow
```
0.5. [Already done] All info collected upfront — use session_context throughout
1.   Verify recipients (Step 1) if > 10 emails
2.   Claim mailbox (Step 2) if no sender specified
3.   Generate & optimize content (Step 3) — use ONLY placeholders with confirmed recipient_fields
4.   Run scripts/run_campaign.py (Step 4) — pass all available recipient fields
5.   Report: campaignId, name, lead count, activation status
```

### API Reference (edge cases only)

Campaign creation is a **4-step sequential flow** handled by the script:
```
Step 4a — Upload content:  POST /campaign/api/biz/mailgo/email/content/upload
Step 4b — Create campaign: POST /campaign/api/biz/mailgo/campaign/save
Step 4c — Add leads:       POST /campaign/api/biz/mailgo/leads/add
Step 4d — Activate:        POST /campaign/api/biz/mailgo/campaign/operate
```

Fall back to raw API only for: updating existing campaigns or adding leads from contact groups.

---

## Step 5 — Manage Campaign Lifecycle

### Use the bundled script (MANDATORY)

```bash
source ~/.zshrc

# Activate / Pause / Delete
python3 scripts/campaign_control.py activate <campaignId>
python3 scripts/campaign_control.py pause    <campaignId>
python3 scripts/campaign_control.py delete   <campaignId>   # confirm with user first!

# List campaigns
python3 scripts/campaign_control.py list                    # all
python3 scripts/campaign_control.py list --status 1         # active
python3 scripts/campaign_control.py list --status 0         # paused
python3 scripts/campaign_control.py list --name "outreach"  # fuzzy search

# Get campaign detail
python3 scripts/campaign_control.py info <campaignId>
```

### Decision Flow
```
User says "stop/pause/resume/delete <campaign>"

1. Know campaign ID?
   YES → run script directly
   NO  → run: scripts/campaign_control.py list --status 1,0
         show results, ask user to pick one

2. If delete → confirm: "Delete campaign '{name}'? This cannot be undone."

3. Run script, report: "Campaign '{name}' (ID: {id}) is now {STATUS}."
```

### Campaign Status Reference

| Code | Name | Description |
|------|------|-------------|
| `-1` | DRAFT | Not activated |
| `0` | PAUSE | Paused |
| `1` | ACTIVE | Sending |
| `2` | COMPLETE | All leads processed |
| `3` | ERROR | Error state |

State transitions: DRAFT->ACTIVE, ACTIVE<->PAUSE, any->deleted

### Abnormal States (`abnormalType`)

| Code | Meaning | Action |
|------|---------|--------|
| `1` | Monthly quota exhausted | Upgrade plan |
| `2` | Some sender accounts have issues | Check account settings |
| `4` | All sender accounts have issues | Fix sender accounts first |
| `9` | Daily sending limit reached | Wait for next day |
| `11` | Email quota exhausted | Upgrade plan |

---

## Step 6 — View Campaign Reports

### Use the bundled script (MANDATORY)

```bash
source ~/.zshrc

# Overview stats
python3 scripts/campaign_report.py overview <campaignId>

# Per-round breakdown
python3 scripts/campaign_report.py rounds <campaignId>

# Daily progress (requires date range)
python3 scripts/campaign_report.py daily <campaignId> --start 2026-03-25 --end 2026-03-31

# List replies (metadata only)
python3 scripts/campaign_report.py replies <campaignId>

# List replies + read plain-text body of each reply
python3 scripts/campaign_report.py replies <campaignId> \
    --sender "sender@mailbox.com" \
    --read-content

# Raw JSON output
python3 scripts/campaign_report.py --json overview <campaignId>
```

### Output Format

Always show rates, not raw numbers alone:
```
Campaign: "Q1 Outreach" (ID: 123456)  Status: ACTIVE
Leads: 500 total | 250 completed | 30 in progress | 200 not yet | 20 failed

  Sent:       450
  Delivered:  420  (93.3%)
  Opened:     180  (42.9%)
  Replied:     35  ( 8.3%)
  Clicked:     65  (15.5%)
  Bounced:     30  ( 6.7%)
```

### Deliverability Health Metrics

| Metric | Healthy | Critical |
|--------|---------|----------|
| Open rate | >20% | <10% |
| Bounce rate | <2% | >5% |
| Spam complaints | <0.1% | >0.3% |

### API Reference (for advanced queries)

| Report | Endpoint |
|--------|----------|
| Overview | `POST /campaign/api/biz/mailgo/stat/overview` |
| Per-round | `POST /campaign/api/biz/mailgo/stat/sequence-info` |
| Send records | `POST /campaign/api/biz/mailgo/stat/sequence-detail` |
| Reply list | `POST /campaign/api/biz/mailgo/stat/sequence-detail-reply` |
| Reply content | `POST /tp/api/hmail/proxy` — `func: mbox:readMessage`, `mid: <messageId>` |
| Reply detail | `POST /campaign/api/biz/mailgo/stat/sequence-detail-reply` |
| Click detail | `POST /campaign/api/biz/mailgo/stat/sequence-detail-click` |
| Contact history | `POST /campaign/api/biz/mailgo/stat/leads-send` |
| Daily progress | `POST /campaign/api/biz/mailgo/stat/daily-step` |

### Behavior Rules
- Default to overview. Drill into details only on explicit request.
- Always show rates alongside raw counts.
- If `sent == 0`: say "No emails sent yet" — do not divide by zero.
- If no campaign ID: list campaigns first, offer to drill into one.
- If `openClick == 0`: tracking was disabled — say so.
- **If `replied > 0` in overview:** proactively suggest reading replies:
  ```
  💬 X reply(ies) detected. Run the following to read them:
  python3 scripts/campaign_report.py replies <campaignId> \
      --sender <senderEmail> --read-content
  ```

---

## Global Error Handling

| HTTP | Action |
|------|--------|
| `401` | Re-run Step 0 (token expired or invalid) |
| `403` | Ensure `User-Agent` header is set |
| `429` | Wait 60s, retry |
| `500` | Retry after 10s |
| `502/503` | Retry after 30-60s |

---

## Global Behavior Rules

1. **Script-first:** Always use bundled scripts. Never reimplement API calls inline.
2. **Verify before send:** Always run Step 1 for campaigns with >10 recipients.
3. **Optimize before send:** Always run Step 3 before sending, even if not explicitly asked. Report "0 issues" if clean.
4. **Confirm destructive actions:** Always confirm before delete. Campaign deletion is irreversible via API.
5. **Security:** Never handle API keys in chat. User must create token in Personal Tokens and set as environment variable.
6. **Zero dependencies:** All scripts use Python stdlib only (`urllib`, `json`, `csv`, `ssl`). No `pip install` required (except optional `openpyxl` for .xlsx files).
