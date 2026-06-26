# Nex Decision Journal

**Log decisions, track reasoning, review outcomes. See where your judgment is sharp and where it needs work.**

Built by **Nex AI** - Digital transformation for Belgian SMEs.

## What It Does

- Log important decisions with full context: options considered, reasoning, predictions, confidence level
- Set follow-up dates to review outcomes (1 week to 1 year)
- Record what actually happened and whether your prediction was correct, partially correct, or wrong
- Capture lessons learned from every reviewed decision
- Stats that surface overconfidence (high confidence + wrong) and underconfidence (low confidence + correct)
- Full-text search across your entire decision history
- Timeline view, tag management, and CSV/JSON export
- Local SQLite storage. No telemetry. Your data stays on your machine.

## Quick Install

```bash
# Via ClawHub
clawhub install nex-decision-journal

# Or manual
git clone https://github.com/Nex-AI-Guy/nex-decision-journal.git
cd nex-decision-journal
bash setup.sh
```

## Example Usage

**Logging a decision:**

```
User: I'm deciding whether to hire a freelancer or a full-time developer.

Agent: I'll log that decision for you.

> nex-decision-journal log "Hire freelancer vs full-time developer" \
    --options "Freelancer at 45/hour, Full-time at 3K/month, Wait 3 months" \
    --chosen "Freelancer at 45/hour" \
    --reasoning "Less risk with current runway" \
    --prediction "Backlog cleared in 2 months" \
    --confidence 7 --category hiring --follow-up 3m

Decision logged (ID: 1). I'll remind you to review the outcome in 3 months.
```

**Reviewing the outcome:**

```
User: The freelancer worked out. Backlog done in 6 weeks.

Agent: Great, I'll record that.

> nex-decision-journal review 1 \
    --outcome "Backlog cleared in 6 weeks, quality was solid" \
    --accuracy correct \
    --lesson "Freelancers work well for defined backlogs"

Outcome recorded. Your prediction was correct.
```

**Checking your patterns:**

```
User: How accurate are my decisions?

> nex-decision-journal stats

Total: 15 decisions | Reviewed: 10 | Correct: 6 | Partial: 3 | Wrong: 1
Average confidence: 6.8/10
Overconfidence alert: 1 time you were 8+/10 confident but wrong
```

## Configuration

Data is stored at `~/.nex-decision-journal/`. Override with the `NEX_DECISION_JOURNAL_DIR` environment variable.

## Privacy

- All data stored locally at `~/.nex-decision-journal/`
- No external API calls
- No telemetry, no analytics, no tracking
- You own your data

## How It Works

1. You log a decision with context, options, reasoning, and a prediction
2. You set a confidence level (1-10) and a follow-up date
3. When the follow-up date arrives, you record what actually happened
4. You mark whether your prediction was correct, partially correct, or wrong
5. Stats and reflect commands surface patterns in your judgment over time

## CLI Reference

```
nex-decision-journal log        Log a new decision
nex-decision-journal show       Show decision details
nex-decision-journal list       List decisions (with filters)
nex-decision-journal review     Record outcome of a decision
nex-decision-journal pending    Show decisions due for review
nex-decision-journal search     Full-text search
nex-decision-journal stats      Show statistics and patterns
nex-decision-journal reflect    Bias detection and lessons
nex-decision-journal edit       Edit a decision
nex-decision-journal abandon    Mark as abandoned
nex-decision-journal tags       List all tags
nex-decision-journal export     Export to JSON or CSV
nex-decision-journal timeline   Timeline view
```

See SKILL.md for full command documentation.

## License

This project uses a dual license model:

**ClawHub (MIT-0):** Copies installed through ClawHub are licensed under MIT-0 as required by the platform. Free for any use.

**GitHub (AGPL-3.0):** Copies obtained from this GitHub repository are licensed under the GNU Affero General Public License v3.0. You may use, modify, and distribute freely, but if you offer a modified version as a service, you must open-source your changes.

**Commercial License:** Want to use this in a proprietary product or hosted service without AGPL obligations? Commercial licenses are available from Nex AI.

Contact: info@nex-ai.be | Website: [nex-ai.be](https://nex-ai.be)

---

Built by [Nex AI](https://nex-ai.be) -- Digital transformation for Belgian SMEs.

## Credits

- **Author**: Kevin Blancaflor
