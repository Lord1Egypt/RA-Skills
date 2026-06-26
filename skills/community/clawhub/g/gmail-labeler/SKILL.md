---
name: gmail-labeler
description: Gmail inbox triage, labeling, and safe archiving with gog plus a configurable lightweight LLM review layer. Use when building or running Gmail automation that separates actionable vs non-actionable mail, applies Gmail labels, archives low-value messages, keeps important human replies in Inbox, routes urgent items for notification, supports multilingual inboxes (English, Portuguese, Spanish), and needs a clean publishable skill with private local overlays kept outside the skill folder.
metadata:
  {
    "openclaw": {
      "emoji": "📬",
      "requires": { "bins": ["gog", "python3"] },
      "install": [
        {
          "id": "node",
          "kind": "node",
          "package": "@felipematos/ain-cli",
          "bins": ["ain"],
          "label": "Install AIN CLI for lightweight structured review"
        }
      ]
    }
  }
---

# Gmail Labeler

A production-oriented Gmail labeling workflow built around:
- `gog` for Gmail access
- a local overlay for private rules/accounts/routes
- a hybrid review flow: heuristics first, lightweight LLM review for ambiguity-band messages
- a 15-minute cron-friendly runner

## What it does

- Classifies inbox items into **non-actionable** vs **actionable** buckets
- Applies Gmail labels and archives non-actionable mail
- Keeps replies, opportunities, urgent billing items, and other actionable mail in Inbox
- Supports **English, Portuguese, and Spanish** keyword coverage out of the box
- Logs every decision to JSONL for auditability and tuning
- Purges logs older than 30 days
- Supports a daily self-improvement review loop based on prior decisions and user corrections

## Default categories

### Non-actionable
- Newsletters
- Promotions
- Notifications
- Ordinary receipts

### Actionable
- Billing issues
- Replies
- Opportunities
- Action Required

## What stays local/private
Keep user-specific editorial, business, or inbox-policy rules in the local overlay, not in the shared skill defaults.
Examples of local-only rules:
- PR / press release handling
- press trip or media invitation routing
- VIP sender policies
- business-specific labels
- custom notification routes

## Operating model

### 1. Sender-type-first routing
Classify sender as:
- `person`
- `company`
- `person_or_unknown`

This keeps bulk automated mail cheap to classify and reserves deeper review for ambiguous or human-origin messages.

### 2. Inbox-by-exception policy
Treat Inbox as an **action queue**, not a reading queue.
Recommended default:
- processed mail always gets `Auto/Triaged`
- mail stays in Inbox only when it is clearly actionable / important
- everything else should leave Inbox, even when the category is still somewhat generic

Practical effect:
- **important/actionable** mail → keep in Inbox and add category labels when possible
- **non-important** mail → remove `INBOX`, keep `Auto/Triaged`, then add a best-fit category label (`Notification`, `Newsletter`, `Receipt`, `Press Releases`, etc.)

### 3. Confidence-band review
Use heuristics first.
Then send only ambiguity-band messages to a lightweight LLM review.

Recommended pattern:
- high confidence → trust heuristics
- medium confidence → LLM review
- low confidence → conservative fallback

### 4. Conservative-but-useful fallback
If a message is clearly automated/company-origin but no specific filter matches, prefer a generic non-actionable classification (for example `Notification`) over leaving it untouched in Inbox.

### 5. Label normalization
Use a small canonical label set and avoid near-duplicates caused by translation, singular/plural, or typos.
Example normalization targets:
- `Press Release` → `Press Releases`
- finance label variants → one canonical finance label
- keep `Auto/Triaged` as the universal processed marker

## Gmail-native labels to prefer
Use Gmail system labels when possible:
- `CATEGORY_PROMOTIONS`
- `CATEGORY_UPDATES`
- `IMPORTANT`
- `STARRED`
- `INBOX`

Create custom labels only when needed, for example:
- `Newsletter`
- `Notification`
- `Receipt`
- `Opportunity`
- `Action Required`
- `Auto/Triaged`

## Local overlay design
Keep the skill publishable by storing private configuration outside the skill directory.

Recommended local overlay path:
```text
~/.openclaw/local/gmail-labeler.config.json
```

Store private values only in the local overlay:
- email accounts
- VIP senders/domains
- notification targets
- business-specific opportunity rules
- personal/custom labels

## Logging and review
Decision logs should live outside the skill source tree, for example:
```text
/home/ubuntu/.openclaw/gmail-labeler-logs/
```

Recommended format:
- one JSONL file per day
- one row per decision
- separate error rows

Suggested daily review inputs:
- yesterday's decision log
- false positives / false negatives
- over-aggressive archiving
- missed billing urgency
- missed opportunities
- user-requested corrections

## Files to read
- `references/default-config.json`
- `references/config-guide.md`
- `references/filter-catalog.md`
- `references/implementation-notes.md`
- `references/logging-and-review.md`
- `references/llm-review.md`
- `references/cron-example.md`
- `references/ain-email-review.schema.json`

## Runners
- Main runner: `scripts/gmail_labeler_runner.py`
- Launcher example: `scripts/gmail_labeler_run.sh`

## Publishing guidance
Before publishing:
- keep only generic defaults in the skill
- remove personal accounts, chat ids, private domains, and custom user rules
- keep examples generic
- document clearly that private configuration belongs in the local overlay
- keep PR / press-release handling user-specific when it reflects private editorial policy; do not publish those local heuristics by default
- validate cron/non-interactive execution via the launcher, not only via direct Python invocation
