# JustFix Skill 🛠️

Quote UK trades jobs from any AI agent. Get a price breakdown and a tappable booking link in a single turn.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skill format: AgentSkills](https://img.shields.io/badge/Skill-AgentSkills-blueviolet)](https://docs.openclaw.ai)
[![MCP](https://img.shields.io/badge/MCP-justfix-teal)](https://estimator-mcp.justfix.app/mcp)

---

## See it in action

### On OpenClaw + Telegram

Ask any OpenClaw (or other harness) agent for a quote in plain English. The skill maps the request to the right JustFix service code, calls the MCP, and replies with a clean quote card and a tappable booking URL.

![JustFix quote in OpenClaw Telegram](assets/screenshots/openclaw-telegram-quote.jpg)

### In ChatGPT (via the JustFix app)

The same underlying MCP server powers JustFix's official ChatGPT app. The skill in this repo gives you the equivalent experience in any other agent, with a tappable booking link instead of the ChatGPT rich card.

<table>
  <tr>
    <td><img src="assets/screenshots/chatgpt-app-1.jpg" alt="ChatGPT JustFix step 1" /></td>
    <td><img src="assets/screenshots/chatgpt-app-2.jpg" alt="ChatGPT JustFix step 2" /></td>
  </tr>
  <tr>
    <td><img src="assets/screenshots/chatgpt-app-3.jpg" alt="ChatGPT JustFix step 3" /></td>
    <td><img src="assets/screenshots/chatgpt-app-4.jpg" alt="ChatGPT JustFix step 4" /></td>
  </tr>
</table>

### In Claude Code, Cursor, Codex CLI or Gemini CLI

_install guide in [install/](install/) covers all four._
<table><tr><td><img src="assets/screenshots/claude_cli.jpg" alt="Claude CLI" /></td></tr></table>

---

## What is this?

A portable AI skill that plugs into [JustFix's public MCP server](https://estimator-mcp.justfix.app/mcp) and lets your AI agent quote real trades jobs in real time. Built for OpenClaw, Hermes, Claude Code, Cursor, Codex CLI, Gemini CLI, and any other harness that supports AgentSkills or the Model Context Protocol.

**One conversation, one quote, one tap to book.**

```
You: How much would it cost to get someone to fix a broken kitchen tap?

Agent: 🔧 Plumbing Estimate
       Scope: Diagnose and repair dripping kitchen tap.
       Estimated duration: 1 hour

       Labour (1 hr × £90/hr): £90.00
       Call-out fee:           £50.00
       Total estimate:        £140.00

       📅 Tap to book this job → my.justfix.app/booking/...
```

## What it does

The skill exposes three MCP tools from JustFix's estimator server to your AI agent:

| Tool | What it does |
|---|---|
| `list_services` | Lists JustFix's 13 service categories with hourly rates |
| `call_out_fee` | Returns the flat booking call-out fee |
| `service-estimate-card` | Generates a full cost estimate plus a unique booking URL |

When the user is ready to confirm, the URL pops them to `my.justfix.app` where they finish the booking (date, postcode, payment).

## Supported services

Electrical · Plumbing · Locksmith · Glazing · Carpentry · Handyperson · Heating + Gas · Gas Appliances · Roofing · Drains · White Goods · Boiler Service · Something Else (catch-all)

UK only. Hourly rates from £55 (white goods) to £90 (most trades). £50 flat call-out fee per booking.

## Installation (pick your harness)

| Harness | Install guide |
|---|---|
| OpenClaw | [install/openclaw.md](install/openclaw.md) |
| Hermes | [install/hermes.md](install/hermes.md) |
| Claude Code | [install/claude-code.md](install/claude-code.md) |
| Cursor | [install/cursor.md](install/cursor.md) |
| Codex CLI | [install/codex-cli.md](install/codex-cli.md) |
| Gemini CLI | [install/gemini-cli.md](install/gemini-cli.md) |

If your harness isn't listed but supports MCP, the pattern is:

1. Register `https://estimator-mcp.justfix.app/mcp` as a streamable-HTTP MCP server.
2. Put `SKILL.md` somewhere the harness's skill discovery picks up (or paste its contents into your agent instructions).
3. Done. No auth, no config, no API keys.

## Sample conversations

Worked examples for common queries:

- [Quote a boiler service](examples/quote-boiler-service.md)
- [Multi-hour electrical job](examples/quote-multi-hour-electrical.md)
- [What services does JustFix offer?](examples/what-services.md)

## How it works

```
┌─────────────┐         ┌──────────────────────┐         ┌────────────────────┐
│  AI agent   │ ──MCP──▶│ JustFix MCP server   │ ──API──▶│ justfix.app        │
│ + SKILL.md  │         │ estimator-mcp        │         │ pricing engine     │
└─────────────┘         └──────────────────────┘         └────────────────────┘
       │                                                          │
       │                                                          │
       │  ◀── booking URL with unique tracking ID ────────────────┘
       │
       ▼
┌─────────────┐
│   User      │ ──── taps URL ────▶ my.justfix.app booking form
└─────────────┘
```

The MCP server is hosted on Vercel by JustFix and is open – no API key required. Each estimate is tagged with a unique `chatgpt_booking_link_id` for attribution.

## What this skill CAN'T do

Honest about the boundaries:

- ❌ Complete the booking itself (the user finishes on the JustFix website)
- ❌ Check live engineer availability (handled at booking time)
- ❌ Take payment (handled on the booking page)
- ❌ Quote outside the UK
- ❌ Quote materials or parts (labour-only estimate)

These are functions of the underlying JustFix product, not the skill. As JustFix expands the MCP, the skill will too.

## Branding and attribution

This is an official integration with JustFix's public MCP server, but the skill repo itself is community-maintained. JustFix takes no responsibility for the skill's behaviour – only for the underlying MCP server.

If you fork, modify, or embed this skill, you must:

- Keep the MIT license intact
- Not misrepresent the JustFix brand
- Pass through the booking URL unchanged (for attribution tracking)

## Roadmap

When JustFix expands the MCP server, the skill will follow:

- Engineer availability lookup
- Quote-to-booking-confirmation in one turn
- Multi-job bundle pricing
- Recurring service plans (e.g. annual boiler service auto-rebook)
- Photo upload for diagnostic estimates

Track progress in [GitHub Issues](https://github.com/Just-Fix/justfix-skill/issues).

## Contributing

Pull requests welcome. Please:

1. Read SKILL.md and understand the format
2. Run the install/* guides in your own harness to test changes
3. Open an issue first for anything bigger than a typo fix

## License

[MIT](LICENSE) – use, modify, distribute, embed in commercial products. No warranty.

## About JustFix

JustFix is redefining Home Repair through the combination of AI + Human Service. Its UK based home-services platform enables rapid booking of vetted tradespeople for common jobs around the home. Examples include: boiler repairs and service, electrical, plumbing, locksmith, glazing, handyman and more. Same-day availability in most UK cities.

🌐 [justfix.app](https://justfix.app)
