# ClawHub listing draft – JustFix Skill

This is the listing copy for [clawhub.ai](https://clawhub.ai). Submit at https://clawhub.ai/submit (or via PR to the ClawHub catalogue repo when listing is opened up).

---

## Title

JustFix – Quote UK trades jobs from any AI agent

## One-line description (max 80 chars)

Quote a plumber, electrician, locksmith or 10 other trades. Tap-to-book.

## Tags

`mcp` `home-services` `uk` `quotes` `booking` `commercial-mcp` `b2c`

## Author

Squid – maintained on behalf of JustFix

## License

MIT

## Source

https://github.com/Just-Fix/justfix-skill

## Long description

JustFix is a UK home-services platform. This skill plugs into their public MCP server (`estimator-mcp.justfix.app`) and lets any AI agent quote real trades jobs in seconds, with a unique booking URL the user can tap to confirm.

**Supported services:**
Electrical · Plumbing · Locksmith · Glazing · Carpentry · Handyperson · Heating + Gas · Gas Appliances · Roofing · Drains · White Goods · Boiler Service · Catch-all

**What it does:**
- Lists JustFix's 13 service categories with hourly rates
- Returns the flat call-out fee
- Generates a full cost estimate (labour + call-out) with a unique tappable booking link
- Maps natural-language descriptions to the right service code automatically
- Picks sensible default durations and explains the estimate to the user

**What it doesn't:**
- Complete the booking itself – the URL takes the user to `my.justfix.app` to confirm date, postcode, payment
- Check live engineer availability (the booking page handles this)
- Quote outside the UK
- Quote parts or materials (labour-only)

**Who it's for:**
- Anyone in the UK who wants to quote a trades job in their AI agent without leaving the conversation
- Developers building B2C products that include home-services pricing
- Founders/operators of property businesses (lettings agents, facilities managers) who want their AI to surface JustFix quotes for their tenants/staff

**Why it's safe:**
- No auth required (public MCP)
- Read-only – the skill cannot take payment, change accounts, or commit to bookings
- MIT licensed, open source
- Booking URL is the only action surface – user always confirms before any money changes hands

**Installs on:**
OpenClaw · Hermes · Claude Code · Cursor · Codex CLI · Gemini CLI (and any harness that supports MCP)

## Featured screenshots

**MUST CAPTURE BEFORE PUBLISHING:**
- [ ] Boiler service quote in OpenClaw / Telegram (clean card view)
- [ ] Electrical multi-hour quote in Claude Code (terminal view)
- [ ] Service list query in ChatGPT (rich card from the underlying MCP)

Save to `assets/screenshots/` in the repo.

## Category

Home services / Commercial integrations / UK

## Suggested ClawHub categorisation

- **Primary:** Commercial integrations
- **Secondary:** UK-specific
- **Tertiary:** Examples & templates (this skill is also a reference for how to wrap a commercial MCP into a portable skill)
