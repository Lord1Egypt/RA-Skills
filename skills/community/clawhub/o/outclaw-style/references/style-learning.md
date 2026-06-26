# Style Learning Reference

Full specification for the Prompt Learning Protocol as applied to outreach style learning.

## Overview

Learn how the user writes outreach messages on each connected channel, producing per-channel style prompts that draft messages indistinguishable from the user's own voice.

## Ground Truth Collection

### Collection Strategy Per Channel

| Channel | Data Source | API Method | Volume Target |
|---------|-----------|------------|---------------|
| Email | Sent folder | `gog gmail messages search "from:me" -j --include-body --max 50` + filters | 30-50 messages |
| Slack | DMs + channels | `slack_search_public_and_private` for user's messages | 20-30 messages |
| WhatsApp | Chat history | WhatsApp MCP message retrieval | 15-25 messages |
| LinkedIn | Sent InMails | Browser automation scrape of sent messages | 10-20 messages |

Gmail retrieval uses the `gog` CLI (see Setup Wizard for prerequisites). When multiple accounts are authorized, pass `-a <email>` to target one; otherwise omit. Parse JSON from stdout: `messages[*].body` is the decoded plain-text body, `messages[*].id`, `threadId`, `date`, `from`, `subject`, `labels` are sibling fields.

### Two-Stage Classification Pipeline

**Stage 1 — Heuristic Pre-filter (fast, free):**

INCLUDE signals:
- Contains company names, titles, or role references
- Mentions meetings, demos, calls, partnerships
- First message in a thread to a non-contact
- Contains value propositions or asks
- Sent to addresses outside user's org domain

EXCLUDE signals:
- Internal team threads (same domain, ongoing)
- Automated notifications, receipts, confirmations
- Personal messages (family, friends — detected by contact frequency)
- Support tickets, bug reports
- Newsletter replies, list-serv posts
- Messages under 20 words (reactions, acknowledgments)

**Stage 2 — LLM Classification (precise):**

Classification prompt:
```
You are classifying sales/business outreach messages.
A message is OUTREACH if the sender is:
  (a) introducing themselves or their company to a prospect,
  (b) following up on a previous outreach attempt,
  (c) proposing a meeting, demo, or partnership, or
  (d) reconnecting with a dormant business contact.

A message is NOT outreach if it is:
  - Internal communication with colleagues
  - Customer support or account management
  - Casual/personal conversation
  - Administrative (scheduling logistics with existing contacts)

Classify as: OUTREACH_COLD | OUTREACH_FOLLOWUP | OUTREACH_WARM | NOT_OUTREACH
```

**Stage 3 — User Confirmation:**

Present summary of classified dataset:
```
I found {n} outreach messages across your channels:

  Email:     {n} messages  ({cold} cold, {followup} follow-up, {warm} warm)
  Slack:     {n} messages  (...)
  WhatsApp:  {n} messages  (...)
  LinkedIn:  {n} messages  (...)

Here are a few examples for you to verify I'm on the right track:
  [3-5 sample messages with classification labels]

Does this look right? Should I include/exclude anything?
```

User approves or adjusts before proceeding.

## Prompt Learning Protocol

Run independently for each channel with sufficient samples (minimum 5, ideally 10+).

### Step 1 — Analyze (thinking model)

Feed all outreach messages for the channel to a reasoning model. Discover:

- **Quality dimensions** specific to the user's style: sentence length, formality level, humor, personalization depth, CTA directness, emoji usage, greeting patterns, sign-off conventions, question density, name-drop frequency
- **Patterns** — recurring structural and stylistic choices (e.g., always opens with a compliment, uses bullet points in follow-ups)
- **Anti-patterns** — what the user consistently avoids (e.g., never uses "I hope this finds you well")

### Step 2 — Generate Candidate Prompt

Produce a style prompt as direct instructions:

```markdown
# {Channel} Outreach Style — {User Name}

Write {type} outreach {messages/emails} following these rules:

STRUCTURE:
- [specific structural rules discovered]

VOICE:
- [voice characteristics]

AVOID:
- [anti-patterns]
```

### Step 3 — Iteration Loop (5 cycles)

For each iteration:

1. **Generate** — Use current style prompt to draft a test message (temperature 0.6-0.8, neutral topic)
2. **Evaluate** — Score test output against reference messages on each dimension (0-100). Compute overall conformity score.
3. **Track best** — If overall score exceeds previous best, save this prompt version
4. **Refine** — Feed scores + weaknesses back. Improve prompt targeting lowest-scoring dimensions (temperature 0.2-0.4)

### Evaluation Dimensions (per channel)

Use `scripts/style_evaluator.py` to score each dimension. The evaluator compares:
- Structural similarity (sentence count, paragraph structure, length)
- Lexical similarity (vocabulary level, formality markers)
- Stylistic markers (greetings, sign-offs, CTA patterns)
- Tone alignment (confidence level, warmth, urgency)

## Output

### Style Learning Report

Present after all channels are processed:

```
╔══════════════════════════════════════════════════╗
║           STYLE LEARNING REPORT                  ║
╠══════════════════════════════════════════════════╣
║  CHANNEL: {channel}                              ║
║  Training samples: {n} messages                  ║
║  Dimensions discovered: {n}                      ║
║                                                  ║
║  Iteration Log:                                  ║
║  ┌────┬───────┬──────┬──────┬──────┬──────┐     ║
║  │ #  │Overall│Tone  │Struct│Person│CTA   │     ║
║  ├────┼───────┼──────┼──────┼──────┼──────┤     ║
║  │ 1  │  ...  │ ...  │ ...  │ ...  │ ...  │     ║
║  │ ...│       │      │      │      │      │     ║
║  │ 5  │  ...  │ ...  │ ...  │ ...  │ ...  │     ║
║  └────┴───────┴──────┴──────┴──────┴──────┘     ║
║  ★ Best: Iteration {n} (score: {score})          ║
║                                                  ║
╚══════════════════════════════════════════════════╝
```

### Storage

Style prompts saved to `~/.openclaw/outclaw/styles/{channel}_style.md` with metadata:
- Training date
- Sample count
- Best score
- Discovered dimensions
