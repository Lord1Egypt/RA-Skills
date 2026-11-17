# Investor Update (Claude Skill)

A Claude skill that drafts a founder's periodic update to investors and LPs, in the founder's voice, for the founder to review and send. It is the drafting engine, it does not connect to any source and it never sends anything.

Built for founders sending monthly or quarterly updates to their investors and LPs.

## What's in here

```
investor-update/
├── SKILL.md    # the skill: role, data input, format selection, output
└── README.md   # this file
```

## How to install

**Claude Code / Agent SDK:** drop the `investor-update/` folder into your skills directory (e.g. `~/.claude/skills/`). It loads automatically and triggers on investor-update requests.

**claude.ai / manual use:** open `SKILL.md`, copy it into a Project's instructions, and start a chat with "draft my investor update."

## How it works

1. It pulls the period's material from whatever is reachable in the session: a Slack MCP on your updates, metrics, and team channels; a Gmail MCP for customer-win, hire, partnership, and fundraise threads; an analytics or billing MCP (Stripe, Amplitude) for numbers. No MCP connected? Paste the material and it drafts from that.
2. It picks the Elad Gil short or long format based on your stage, and lets you override.
3. It infers up to 3 candidate asks and presents them for you to confirm or cut.
4. It builds a month-by-month metrics table from your numbers only, never a number that isn't in the input.
5. It produces a complete email draft (subject and body) for you to review and send.

## A note on what it won't do

It never sends, schedules, or posts anything, and it only reads the channels and threads you point it at. Every draft ends with a "Review before sending" line. You control what goes out.
