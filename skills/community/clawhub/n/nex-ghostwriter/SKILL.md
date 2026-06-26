---
name: nex-ghostwriter
description: >-
  Meeting follow-up email drafter. Dump your meeting notes and get a polished follow-up
  email in seconds. Log the meeting (who attended, what was discussed, action items, next
  steps, deadlines), then the tool generates a structured follow-up email ready to send.
  Supports five tone presets: professional, friendly, formal, casual, direct. Regenerate
  the same meeting as a different tone with one command. Tracks which drafts you sent and
  which you skipped. Stores contacts with preferred greetings so emails feel personal, not
  templated. Generates both client-facing follow-up emails and internal team recaps. Handles
  action items with owners and deadlines, next steps, target dates. Full-text search across
  all meetings. Statistics on meetings by type, by client, by month. Export to CSV or JSON.
  Works for agencies (bureaus), consultants, freelancers (freelancers), sales teams
  (verkoopteams), account managers, project managers, founders (oprichters), and anyone who
  has meetings and hates writing follow-up emails. Meeting recap, vergaderingsverslag,
  opvolgmail, follow-up email, meeting summary, notulen, action items, actiepunten,
  vergadering, klantgesprek, sales call, client call, meeting notes, email drafter,
  email generator, meeting tracker, follow-up tracker, recap email.
version: 1.0.0
metadata:
  clawdbot:
    emoji: "✉️"
    requires:
      bins:
        - python3
      env: []
    primaryEnv: ""
    homepage: https://nex-ai.be
    files:
      - "nex-ghostwriter.py"
      - "lib/*"
      - "setup.sh"
---

# Nex Ghostwriter

Dump your meeting notes, get a follow-up email. One command, ready to send.

## When to Use

Use this skill when the user asks about:

- Writing a follow-up email after a meeting
- Drafting a meeting recap or summary email
- Generating a client follow-up from meeting notes
- Creating an internal team recap
- Tracking meeting action items and next steps
- Managing contacts for personalized follow-ups
- Searching past meetings
- Viewing or resending previous follow-up drafts
- Changing the tone of a follow-up email
- Exporting meeting history

Trigger phrases: "follow-up email", "meeting recap", "send a summary", "draft an email", "what did we discuss", "meeting notes", "action items", "follow up with client", "opvolgmail", "vergaderingsverslag", "recap", "meeting follow-up"

## Quick Setup

```bash
bash setup.sh
```

Creates `~/.nex-ghostwriter/` with the SQLite database, exports, and templates directories.

## Available Commands

The CLI tool is `nex-ghostwriter`. All commands output plain text.

### Draft a Follow-up Email

Log a meeting and generate the email in one step:

```bash
# Client meeting
nex-ghostwriter draft "Redesign kickoff with Bakkerij Peeters" \
  --client "Jan Peeters" \
  --email "jan@bakkerijpeeters.be" \
  --notes "Discussed full website redesign. They want modern look, mobile-first. Current site is 5 years old." \
  --actions "Send proposal by Friday, Share 3 design references, Set up staging environment" \
  --next-steps "I send proposal, they review over weekend, follow-up call Monday" \
  --deadline 2026-04-18 \
  --type client \
  --tone professional

# Internal standup
nex-ghostwriter draft "Weekly standup" \
  --type internal \
  --attendees "Kevin, Sarah, Thomas" \
  --notes "Sprint on track. Thomas blocked on API integration. Sarah finishing dashboard." \
  --actions "Kevin: unblock Thomas on API credentials, Sarah: push dashboard to staging by Thursday"

# Quick sales call
nex-ghostwriter draft "Sales call with Lux Interiors" \
  --client "Marie Dubois" \
  --email "marie@luxinteriors.be" \
  --notes "Interested in premium plan. Budget 2K/month. Wants to start in May." \
  --next-steps "Send pricing breakdown and case studies" \
  --tone friendly
```

### Regenerate with Different Tone

Same meeting, different tone:

```bash
nex-ghostwriter redraft 1 --tone formal
nex-ghostwriter redraft 1 --tone casual
```

### Show Meeting Details

```bash
nex-ghostwriter show 1
```

### View a Draft's Full Email

```bash
nex-ghostwriter view 1
```

### List Meetings

```bash
nex-ghostwriter list
nex-ghostwriter list --type client
nex-ghostwriter list --client "Peeters"
```

### List Drafts

```bash
nex-ghostwriter drafts
nex-ghostwriter drafts --status draft
nex-ghostwriter drafts --status sent
```

### Mark Draft as Sent/Skipped

```bash
nex-ghostwriter sent 1
nex-ghostwriter skip 2
```

### Search Meetings

```bash
nex-ghostwriter search "redesign"
nex-ghostwriter search "Peeters"
```

### Edit Meeting

```bash
nex-ghostwriter edit 1 --notes "Updated: they also want e-commerce integration"
nex-ghostwriter edit 1 --deadline 2026-05-01
```

### Manage Contacts

```bash
nex-ghostwriter contact-add "Jan Peeters" --email "jan@bakkerijpeeters.be" --company "Bakkerij Peeters" --greeting "Dag Jan,"
nex-ghostwriter contacts
```

Contacts with a preferred greeting get that greeting in generated emails.

### Statistics

```bash
nex-ghostwriter stats
```

### Export

```bash
nex-ghostwriter export json
nex-ghostwriter export csv
```

## Example Interactions

**User:** "I just had a call with Marie from Lux Interiors. We discussed the premium plan, she's interested, budget is 2K per month, wants to start in May. I need to send her pricing and case studies."
**Agent runs:** `nex-ghostwriter draft "Premium plan discussion with Lux Interiors" --client "Marie Dubois" --email "marie@luxinteriors.be" --notes "Discussed premium plan. Budget 2K/month. Wants to start May." --next-steps "Send pricing breakdown and case studies" --type sales --tone professional`
**Agent:** "Here's your follow-up email for Marie. Subject: Follow-up: Premium plan discussion with Lux Interiors. The email covers what you discussed, confirms the next steps, and asks her to flag anything you missed. Want me to adjust the tone or add anything?"

**User:** "Make it more casual"
**Agent runs:** `nex-ghostwriter redraft 1 --tone casual`
**Agent:** "Redrafted with a casual tone. Opening is now 'Good chatting earlier today' instead of 'Thanks for the meeting'. Closing is 'Cheers,' instead of 'Best regards,'. Want to use this version?"

**User:** "I sent the email to Marie"
**Agent runs:** `nex-ghostwriter sent 1`
**Agent:** "Draft #1 marked as sent."

**User:** "Had a standup with the team. Kevin, Sarah, Thomas. Sprint is on track but Thomas is blocked on API creds."
**Agent runs:** `nex-ghostwriter draft "Weekly standup" --type internal --attendees "Kevin, Sarah, Thomas" --notes "Sprint on track. Thomas blocked on API integration." --actions "Kevin: get API credentials for Thomas, Sarah: push dashboard to staging Thursday"`
**Agent:** "Internal recap generated. Lists the action items with owners. Ready to paste into Slack or email."

**User:** "What meetings did I have with Peeters?"
**Agent runs:** `nex-ghostwriter search "Peeters"`
**Agent:** "Found 2 meetings with Peeters: the redesign kickoff on April 6 and a follow-up review on April 15."

**User:** "Show me the stats"
**Agent runs:** `nex-ghostwriter stats`
**Agent:** "12 meetings this month. 8 client, 4 internal. 10 drafts sent, 2 pending. Top client: Bakkerij Peeters with 3 meetings."

**User:** "Add Jan Peeters to my contacts so emails use his Dutch greeting"
**Agent runs:** `nex-ghostwriter contact-add "Jan Peeters" --email "jan@bakkerijpeeters.be" --company "Bakkerij Peeters" --greeting "Dag Jan,"`
**Agent:** "Contact saved. Future emails to Jan will use 'Dag Jan,' as the greeting."

**User:** "Export all my meetings to CSV"
**Agent runs:** `nex-ghostwriter export csv`
**Agent:** "Exported to ~/.nex-ghostwriter/exports/meetings_export.csv"

## Tone Guide

| Tone | Greeting | Closing | Style |
|------|----------|---------|-------|
| professional | Hi [First], | Best regards, | Balanced and clear |
| friendly | Hi [First], | Talk soon, | Warm, approachable |
| formal | Dear [Full Name], | Kind regards, | Traditional business |
| casual | Hey [First], | Cheers, | Relaxed, short |
| direct | Hi [First], | Best, | Minimal, to the point |

## Output Parsing

- Meeting IDs in brackets: [1], [2]
- Dates in ISO-8601 (YYYY-MM-DD)
- Draft statuses: [DRAFT], [SENT], [SKIP]
- Every command ends with `[Ghostwriter by Nex AI | nex-ai.be]`

Strip the footer when presenting to the user.

## Important Notes

- All data stored locally at `~/.nex-ghostwriter/`. No telemetry.
- The generated email is a starting point. The AI agent should present it and ask if adjustments are needed.
- Contacts with a preferred_greeting override the tone-based greeting.
- Multiple drafts can exist per meeting (different tones, revisions).
- Action items accept comma-separated text or JSON arrays.

## Troubleshooting

- **"No module named lib"**: Run from the skill directory.
- **"Meeting X not found"**: Check `nex-ghostwriter list` for valid IDs.
- **Email looks too generic**: Add the contact with `contact-add` and set a preferred greeting.
- **Wrong tone**: Use `nex-ghostwriter redraft <ID> --tone <tone>` to regenerate.
- **Action items not formatting**: Use commas between items, or pass a JSON array.

## Credits

Built by Nex AI (https://nex-ai.be) - Digital transformation for Belgian SMEs.
Author: Kevin Blancaflor
