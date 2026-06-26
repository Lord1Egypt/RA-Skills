# OPC Invoice Manager — Claude Code Skill

An Accounts Receivable light system for solo entrepreneurs and one-person company CEOs.

This skill manages the **full billing lifecycle** — from creating invoices to collecting payment — all from Claude Code. It's not just an invoice generator; it's the system that tells you when to invoice, how to follow up, and where your money is.

> **Important:** This is an invoicing tool, not tax advice. Always consult a qualified accountant for tax compliance decisions.

## What It Does

### Invoice Generation
- **Professional invoices** in markdown and HTML (print/PDF-ready)
- **Auto-infer from contracts** — pulls client, terms, currency, milestones from your contract archive
- **Auto-infer from client profiles** — remembers billing addresses, AP contacts, PO requirements
- **Arithmetic validation** — line items + tax - discount = total, verified every time
- **Flexible numbering** — configurable format, yearly/monthly reset, void number reservation

### Collections Workflow
- **6-stage cadence engine** — pre-due reminder through final notice
- **Ready-to-send email drafts** — tone-matched to stage and client preference
- **Dispute handling** — acknowledgment templates, cadence pausing, resolution paths
- **Automatic overdue detection** — alerts when you open the skill

### Payment Reconciliation
- **Full, partial, and batch payments** — mark paid with one command
- **Payment matching** — "Got $15,000 from Acme" → suggests which invoices it covers
- **Overpayment/underpayment** detection with suggested next actions

### Cash Flow Visibility
- **Action-oriented dashboard** — what to send, follow up, and escalate today
- **Aging report** — overdue buckets (1-30, 31-60, 60+ days)
- **Revenue analytics** — invoiced vs collected, client distribution, recurring vs one-off mix
- **AR health metrics** — DSO, collection rate, dispute rate, client payment behavior

### Contract Integration
- Reads from `opc-contract-manager` archive when available
- Pulls billing model, milestones, PO requirements, late fee clauses
- No hard dependency — works standalone or integrated

## Installation

### Option 1: Clone to skills directory

```bash
git clone https://github.com/LeonFJR/opc-skills.git ~/.claude/skills/opc-skills
```

### Option 2: Copy just this skill

```bash
cp -r opc-invoice-manager ~/.claude/skills/opc-invoice-manager
```

### Option 3: Project-level skill

Add to your project's `.claude/settings.json`:

```json
{
  "skills": ["path/to/opc-invoice-manager"]
}
```

## Usage

### Create an invoice

```
/opc-invoice-manager

Invoice Acme Corp $5,000 for March consulting
```

The skill auto-detects the client, pulls terms from contracts/profiles, and generates a complete invoice. No questionnaire.

### Quick invoice

```
/opc-invoice-manager

Quick invoice for Acme Corp $12,000 milestone 2 delivery
```

### Follow up on unpaid invoices

```
/opc-invoice-manager

Follow up on overdue invoices
```

Generates stage-appropriate email drafts based on how long each invoice has been outstanding.

### Record a payment

```
/opc-invoice-manager

Acme paid INV-2026-003
```

Or partial: "Received $5,000 of $12,000 on INV-2026-003"

### Check your dashboard

```
/opc-invoice-manager

What's outstanding?
```

Shows action items, aging buckets, and overdue alerts.

### Revenue insights

```
/opc-invoice-manager

Show me revenue trends
```

### Void and reissue

```
/opc-invoice-manager

Void INV-2026-003 — wrong amount. Reissue with corrected line items.
```

### Manage clients

```
/opc-invoice-manager

Add client: Beta Inc, AP contact: ap@beta.com, Net 45, PO required
```

## Archive Structure

```
invoices/
├── INDEX.json                                    # Master index (auto-generated)
├── INSIGHTS.json                                 # Revenue + AR insights
├── INSIGHTS.md                                   # Human-readable insights
├── clients/
│   ├── acme-corp.json                            # Client AR profile
│   └── beta-inc.json
├── recurring/
│   └── acme-monthly-retainer.json                # Recurring template
├── 2026-03/
│   ├── INV-2026-001_acme-corp/
│   │   ├── invoice.md                            # Rendered invoice
│   │   ├── invoice.html                          # HTML version
│   │   └── metadata.json                         # Full metadata
│   └── INV-2026-002_beta-inc/
│       ├── invoice.md
│       └── metadata.json
└── .numbering-config.json                        # Numbering policy
```

## Skill Architecture

```
opc-invoice-manager/
├── SKILL.md                                      # Core workflow (~280 lines)
├── README.md                                     # This file
├── LICENSE                                       # MIT
├── references/
│   ├── invoice-best-practices.md                 # Content, formatting, numbering, timing
│   ├── tax-and-compliance.md                     # Tax awareness + escalation triggers
│   ├── payment-terms-guide.md                    # Net terms, discounts, milestones, retainers
│   └── collections-playbook.md                   # 6-stage cadence engine with email templates
├── templates/
│   ├── invoice.md                                # Markdown invoice template
│   ├── invoice.html                              # HTML invoice (print/PDF-ready, inline CSS)
│   ├── invoice-metadata-schema.json              # Full metadata schema
│   ├── client-profile-schema.json                # AR-oriented client profiles
│   ├── aging-report.md                           # Action-oriented aging report
│   └── revenue-summary.md                        # AR + Revenue dual-view analytics
└── scripts/
    ├── invoice_tracker.py                        # Index, aging, reconciliation, insights
    └── invoice_numbering.py                      # Configurable numbering with format tokens
```

**Progressive disclosure**: Only `SKILL.md` is loaded initially. Reference files and templates are loaded on-demand during the specific mode that needs them.

## Requirements

- Claude Code CLI
- Python 3.8+ (for scripts — stdlib only, no pip install needed)

## What This Skill Is NOT

This skill is designed for practical billing management. It is **not** a substitute for accounting software or professional advice. It will flag and recommend an accountant for:

- Cross-border tax complexity (VAT, withholding, transfer pricing)
- Tax registration threshold questions
- Revenue thresholds affecting tax status
- Year-end tax reporting or filing
- Credit notes with tax implications
- Bad debt write-off decisions
- Multi-entity billing

## License

MIT
