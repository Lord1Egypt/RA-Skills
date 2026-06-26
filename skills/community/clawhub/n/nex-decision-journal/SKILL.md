---
name: nex-decision-journal
description: >-
  Personal decision journal and reasoning tracker that helps you become a better decision maker
  over time. Log important decisions before you make them, capture your reasoning, options
  considered, confidence level, and predictions. Set follow-up dates to review outcomes later.
  Record what actually happened, whether your prediction was correct, partially correct, or
  wrong, and capture lessons learned. Over time, build a searchable archive of your decision
  history with statistics that reveal patterns in your judgment: where you're overconfident,
  where you're underconfident, which categories you decide well in, and which ones need work.
  Perfect for founders (oprichters), CEOs, managers (managers), freelancers (freelancers),
  entrepreneurs (ondernemers), team leads, investors, agency owners, consultants, and anyone
  making high-stakes business or personal decisions. Track hiring decisions (aanwervingen),
  product strategy (productstrategie), pricing changes (prijswijzigingen), partnership deals,
  investment choices (investeringskeuzes), technical architecture decisions, marketing
  experiments, sales strategies, career moves (carrierestappen), and personal life decisions.
  Includes reflection tools that surface overconfidence bias, underconfidence patterns, accuracy
  breakdowns by category, and a complete lessons-learned knowledge base built from your own
  experience. Supports decision categories, tags, stakes levels, reversibility flags, confidence
  scoring on a 1-10 scale, flexible follow-up scheduling (1 week to 1 year), full-text search,
  timeline view, and CSV/JSON export. All data stored locally in SQLite. No external APIs, no
  telemetry, no tracking. Your decisions are yours. Works in English and Dutch. Decision log,
  beslissingenlogboek, besluitvorming, beslissingsarchief, decision tracker, judgment tracker,
  outcome tracker, prediction journal, reflection tool, thinking tool, metacognition.
version: 1.0.0
metadata:
  clawdbot:
    emoji: "🎯"
    requires:
      bins:
        - python3
      env: []
    primaryEnv: ""
    homepage: https://nex-ai.be
    files:
      - "nex-decision-journal.py"
      - "lib/*"
      - "setup.sh"
---

# Nex Decision Journal

Log decisions, track reasoning, review outcomes. See where your judgment is sharp and where it needs work.

## When to Use

Use this skill when the user asks about:

- Logging, recording, or tracking a decision they're about to make
- Deciding between multiple options and wanting to document their reasoning
- Predicting outcomes and wanting to check their accuracy later
- Reviewing past decisions and their outcomes
- Checking what decisions are due for follow-up review
- Searching through their decision history
- Understanding their decision-making patterns (overconfidence, underconfidence)
- Getting statistics on their prediction accuracy
- Reflecting on lessons learned from past decisions
- Exporting their decision journal for analysis
- Viewing a timeline of decisions
- Tracking business decisions: hiring, pricing, product, partnership, investment
- Tracking personal decisions: career moves, health, finances
- Wanting accountability for important choices
- Building a decision-making knowledge base from their own experience
- Asking about their judgment patterns or cognitive biases

Trigger phrases: "decision", "deciding", "should I", "log this decision", "track my decision", "what did I decide", "review my decisions", "decision journal", "prediction", "outcome", "how accurate am I", "overconfident", "lessons learned", "follow up on decision", "beslissing", "besluit", "keuze maken"

## Quick Setup

If the database does not exist yet, run the setup script:

```bash
bash setup.sh
```

This creates `~/.nex-decision-journal/` with the SQLite database and export directory.

## Available Commands

The CLI tool is `nex-decision-journal`. All commands output plain text.

### Log a Decision

Log a new decision with full context:

```bash
# Minimal: just a title
nex-decision-journal log "Hire a junior developer"

# Full context
nex-decision-journal log "Hire a junior developer" \
  --context "Team is overwhelmed. Current sprint velocity dropped 30%. Need more hands." \
  --options "Hire full-time at 3K/month, Hire freelancer at 45/hour, Wait 3 months and reassess" \
  --chosen "Hire freelancer at 45/hour" \
  --reasoning "Full-time is too risky with current runway. Freelancer gives flexibility to scale down if revenue dips." \
  --prediction "Freelancer will handle the backlog within 2 months and we'll convert to full-time by Q4" \
  --confidence 7 \
  --category hiring \
  --stakes high \
  --tags "team,capacity,budget" \
  --follow-up 3m

# Quick log with just the essentials
nex-decision-journal log "Switch from Firebase to Supabase" \
  --reasoning "Firebase costs are scaling badly" \
  --prediction "Migration takes 3 weeks, saves 40% on hosting by month 2" \
  --confidence 6 \
  --category technical \
  --follow-up 2m
```

Follow-up accepts: `1w`, `2w`, `1m`, `2m`, `3m`, `6m`, `1y`, a number of days (e.g., `45`), or an ISO date (e.g., `2026-09-01`). Default: 90 days.

### Show a Decision

Show full details of a logged decision:

```bash
nex-decision-journal show 1
```

### List Decisions

List all decisions with optional filters:

```bash
# All decisions
nex-decision-journal list

# Filter by status
nex-decision-journal list --status pending
nex-decision-journal list --status reviewed

# Filter by category
nex-decision-journal list --category hiring

# Filter by tag
nex-decision-journal list --tags budget
```

### Review a Decision (Record Outcome)

When the follow-up date arrives, record what actually happened:

```bash
nex-decision-journal review 1 \
  --outcome "Freelancer delivered 80% of backlog in 6 weeks. Quality was good." \
  --accuracy correct \
  --notes "Slightly ahead of schedule" \
  --lesson "Freelancers work well for defined backlogs. Less good for open-ended feature work."
```

Accuracy options: `correct`, `partially_correct`, `wrong`.

### Check Pending Reviews

See which decisions are overdue for review:

```bash
nex-decision-journal pending
```

### Search Decisions

Full-text search across all decision fields:

```bash
nex-decision-journal search "freelancer"
nex-decision-journal search "pricing"
nex-decision-journal search "Firebase"
```

### View Statistics

See your decision-making patterns:

```bash
nex-decision-journal stats
```

Shows: total decisions, prediction accuracy breakdown, average confidence, confidence by accuracy, overconfidence/underconfidence alerts, decisions by category and stakes, monthly volume.

### Reflect on Patterns

Bias detection, accuracy by category, lessons learned:

```bash
nex-decision-journal reflect
```

Shows: accuracy by category, overconfident decisions (high confidence but wrong), underconfident decisions (low confidence but correct), and all lessons learned.

### Edit a Decision

Update fields on an existing decision:

```bash
nex-decision-journal edit 1 --prediction "New prediction after more info" --confidence 8
nex-decision-journal edit 1 --tags "team,capacity,budget,q2"
nex-decision-journal edit 1 --follow-up 6m
```

### Abandon a Decision

Mark a decision as abandoned (never acted on):

```bash
nex-decision-journal abandon 3 --reason "Client cancelled the project"
```

### List Tags

See all tags used across decisions:

```bash
nex-decision-journal tags
```

### Export Decisions

Export to JSON or CSV for external analysis:

```bash
nex-decision-journal export json
nex-decision-journal export csv --status reviewed --output "reviewed_decisions.csv"
```

### Timeline View

See decisions on a timeline:

```bash
nex-decision-journal timeline
nex-decision-journal timeline --start 2026-01-01 --end 2026-06-30
```

## Example Interactions

**User:** "I need to decide whether to raise my agency prices from 299 to 399 per month. Help me log this."
**Agent runs:** `nex-decision-journal log "Raise retainer pricing from 299 to 399/month" --context "Current margins are thin at 299. Competitors charge 350-500. 3 clients out of 12 have mentioned they'd pay more for faster turnaround." --options "Raise to 399 for new clients only, Raise to 399 for everyone, Raise to 349 as compromise, Keep at 299" --chosen "Raise to 399 for new clients only" --reasoning "Grandfather existing clients to avoid churn. Test new price point on incoming leads." --prediction "New clients will still convert at 60%+ close rate. No existing client churn." --confidence 7 --category pricing --stakes high --tags "pricing,revenue,agency" --follow-up 3m`
**Agent:** "Logged your pricing decision (ID: 5). You chose to raise to 399 for new clients only, with 7/10 confidence that conversion stays above 60%. I'll remind you to review the outcome in 3 months."

**User:** "How did my decisions turn out this quarter?"
**Agent runs:** `nex-decision-journal stats`
**Agent:** "Here's your Q1 summary. You logged 8 decisions. Of the 5 you've reviewed, you were correct on 3, partially correct on 1, and wrong on 1. Your average confidence was 6.4/10. You tend to be slightly overconfident on hiring decisions (2 were wrong despite 7+/10 confidence)."

**User:** "Show me decisions where I was overconfident"
**Agent runs:** `nex-decision-journal reflect`
**Agent:** "You have 2 overconfident decisions where you rated 7+/10 confidence but the prediction was wrong. Both were in the hiring category. The lesson from decision #3 was: 'Cultural fit matters more than technical skills for long-term hires.'"

**User:** "What decisions are due for review?"
**Agent runs:** `nex-decision-journal pending`
**Agent:** "3 decisions are overdue for review: pricing change (12 days overdue), new marketing channel (5 days overdue), and office lease renewal (2 days overdue). Want to review any of them now?"

**User:** "The pricing change worked out great. Close rate stayed at 65%."
**Agent runs:** `nex-decision-journal review 5 --outcome "Close rate stayed at 65% with new 399 pricing. Revenue per new client up 33%." --accuracy correct --lesson "Grandfather existing, test new price on leads. Works every time."`
**Agent:** "Outcome recorded for your pricing decision. Prediction was correct. Your overall accuracy is now 67% across reviewed decisions."

**User:** "I decided not to go through with the partnership deal after all"
**Agent runs:** `nex-decision-journal abandon 7 --reason "Due diligence revealed financial red flags"`
**Agent:** "Decision #7 marked as abandoned. Reason: due diligence revealed financial red flags."

**User:** "Search my decisions for anything about Firebase"
**Agent runs:** `nex-decision-journal search "Firebase"`
**Agent:** "Found 2 decisions mentioning Firebase: #4 (Switch from Firebase to Supabase, pending review) and #9 (Add Firebase Analytics to client dashboards, reviewed, prediction was partially correct)."

**User:** "Export all my reviewed decisions to CSV"
**Agent runs:** `nex-decision-journal export csv --status reviewed`
**Agent:** "Exported 12 reviewed decisions to ~/.nex-decision-journal/exports/decisions_export.csv."

**User:** "Show me a timeline of everything I decided this year"
**Agent runs:** `nex-decision-journal timeline --start 2026-01-01`
**Agent:** "Here's your decision timeline for 2026. January: 3 decisions (2 reviewed, 1 pending). February: 5 decisions (3 reviewed, 1 wrong, 1 pending). March: 4 decisions (all pending)."

## Output Parsing

All CLI output is plain text, structured for easy parsing:
- Decision IDs are always shown in brackets: [1], [2], etc.
- Dates are in ISO-8601 format (YYYY-MM-DD)
- Confidence is shown as X/10
- Accuracy symbols: [OK] = correct, [~~] = partially correct, [XX] = wrong
- Every command output ends with `[Decision Journal by Nex AI | nex-ai.be]`

When presenting output to the user, strip the footer line and present the information naturally.

## Important Notes

- All data is stored locally at `~/.nex-decision-journal/`. No telemetry, no analytics.
- Decisions are never auto-deleted. Use `abandon` to mark unused decisions.
- Follow-up dates are suggestions, not hard deadlines. The `pending` command shows overdue reviews.
- Confidence scoring is subjective but patterns emerge after 10+ reviewed decisions.
- Export to CSV for spreadsheets, or JSON for programmatic analysis.

## Troubleshooting

- **"No module named lib"**: Run from the skill directory, or ensure `lib/` is in the same folder as `nex-decision-journal.py`.
- **"Database is locked"**: Another process may be using the database. Wait and retry.
- **"No decisions found"**: Run `nex-decision-journal list` to verify decisions exist. Use `nex-decision-journal log` to add one.
- **FTS search returns no results for valid terms**: Try a simpler query. FTS5 uses prefix matching. Single short words work best.
- **"Confidence must be between 1 and 10"**: The confidence flag only accepts integers from 1 to 10.
- **Follow-up not triggering**: The `pending` command checks if follow_up_date <= today. Run it regularly or integrate with a cron/scheduled task.
- **Export directory not found**: Run `bash setup.sh` to recreate the directory structure.

## Credits

Built by Nex AI (https://nex-ai.be) - Digital transformation for Belgian SMEs.
Author: Kevin Blancaflor
