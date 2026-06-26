# mailgo-campaign-suite

Complete cold email campaign skill for Mailgo. One skill handles the entire outreach pipeline:

1. **Verify** recipient emails (async submit + poll)
2. **Claim** a free pre-warmed mailbox (90+ sender score, 60 days)
3. **Optimize** email content (spam triggers, HTML cleanup, deliverability)
4. **Send** campaigns (content upload, lead import, activation)
5. **Manage** campaign lifecycle (activate, pause, delete, list)
6. **Report** campaign statistics (overview, per-round, daily progress)

## Publisher

This skill is published by **LeadsNavi**, the company behind the Mailgo cold email platform.

- Product: [https://app.mailgo.ai](https://app.mailgo.ai)
- Publisher website: [https://www.leadsnavi.com](https://www.leadsnavi.com)

## Requirements

- Python 3.7+
- `MAILGO_API_KEY` environment variable (OpenAPI Key from Mailgo)
- No third-party dependencies (stdlib only: `urllib`, `json`, `csv`, `ssl`)
- Optional: `openpyxl` for .xlsx file support (`pip install openpyxl`)

## Security & Credentials

This skill requires a **Mailgo OpenAPI Key** (`MAILGO_API_KEY`) to operate. Please read before using:

| Concern | Detail |
|---------|--------|
| **What the token can do** | Claim mailboxes, create/activate/pause/delete campaigns, verify emails, read campaign reports — all actions on your Mailgo account. |
| **How to obtain it** | Log in to [https://app.mailgo.ai](https://app.mailgo.ai) → Click your avatar in the bottom-left corner → Personal Tokens → Create Token → Copy the token. See SKILL.md Step 0 for step-by-step instructions. |
| **How it is used** | Sent as `X-API-Key: {token}` header to `api.leadsnavi.com` — the official Mailgo backend (LeadsNavi is the parent brand behind Mailgo; see [app.mailgo.ai](https://app.mailgo.ai) and the Mailgo website for details). |
| **How to stay safe** | Set as a local environment variable only — **never paste into chat**. |
| **How to revoke** | Go to [https://app.mailgo.ai](https://app.mailgo.ai) → Personal Tokens → Delete the token. |
| **API endpoints called** | All calls go to `https://api.leadsnavi.com` (Mailgo's official API) — email verification, mailbox claiming, campaign CRUD, and reporting. Review the bundled Python scripts for exact endpoints. |

> `MAILGO_API_KEY` is your Mailgo account credential. Keep it secure and never share it publicly.

## Compliance

This skill sends emails to recipient lists you provide. You are responsible for ensuring your campaigns comply with applicable laws and platform terms, including:

- **CAN-SPAM Act** (US) — include a physical address and honor opt-out requests
- **GDPR** (EU) — ensure you have a lawful basis for contacting recipients
- **Mailgo Terms of Service** — [https://app.mailgo.ai](https://app.mailgo.ai)

The skill's built-in email optimizer adds a soft opt-out line to every email by default.

## Directory Structure

```
mailgo-campaign-suite/
├── SKILL.md                        # Main skill instructions
├── README.md                       # This file
├── scripts/
│   ├── verify_emails.py            # Step 1: Email verification (submit + poll)
│   ├── claim_free_mailbox.py       # Step 2: Free mailbox claiming
│   ├── run_campaign.py             # Step 4: Campaign creation & activation
│   ├── campaign_control.py         # Step 5: Lifecycle management
│   └── campaign_report.py          # Step 6: Statistics & reporting
└── resources/
    ├── spam-triggers.md            # Step 3: Spam trigger replacement table
    └── industry-templates.md       # Step 3: Industry-specific email templates
```

## Quick Start

```bash
# 1. Set up authentication
export MAILGO_API_KEY="your-api-key"

# 2. Verify emails
python3 scripts/verify_emails.py alice@example.com bob@gmail.com

# 3. Claim free mailbox
python3 scripts/claim_free_mailbox.py

# 4. Create and send campaign
python3 scripts/run_campaign.py \
    --sender "claimed@mailbox.com" \
    --subject "Quick question" \
    --body "<html><body><p>Hi</p></body></html>" \
    --recipients "alice@example.com" \
    --campaign-name "My Campaign"

# 5. Check status
python3 scripts/campaign_control.py list
python3 scripts/campaign_report.py overview <campaignId>
```

## Scripts Reference

| Script | Purpose | Key Args |
|--------|---------|----------|
| `verify_emails.py` | Submit + poll email verification | `emails...`, `--file`, `--email-column` |
| `claim_free_mailbox.py` | Claim pre-warmed mailbox | `--json`, `--api-key` |
| `run_campaign.py` | Full campaign creation flow | `--sender`, `--subject`, `--body/--body-file`, `--recipients/--recipients-file` |
| `campaign_control.py` | Activate/pause/delete/list | `activate/pause/delete/list/info` |
| `campaign_report.py` | View campaign statistics | `overview/rounds/daily`, `--json` |

## Relationship to Other Mailgo Skills

This suite consolidates functionality from:
- `mailgo-auth-setup` — authentication guidance (Step 0)
- `mailgo-email-verifier` — email verification (Step 1)
- `mailgo-email-optimizer` — content optimization rules (Step 3)
- `mailgo-campaign` — campaign creation (Step 4)
- `mailgo-campaign-control` — lifecycle management (Step 5)
- `mailgo-campaign-report` — statistics (Step 6)

Those individual skills remain available for standalone use. This suite provides the same capabilities in a single, self-contained package.
