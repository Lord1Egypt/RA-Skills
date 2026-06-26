---
name: justfix
description: Use this skill when the user asks for a quote, estimate, price, or "how much" for a UK trades job – electrical, plumbing, locksmith, glazing, carpentry, handyperson, heating, gas, roofing, drains, white goods, or boiler service. Calls the JustFix Estimator MCP server to return a cost breakdown, scope summary, and a tappable booking link that completes the booking in the browser.
metadata:
  source: justfix
  homepage: https://justfix.app
  mcp_endpoint: https://estimator-mcp.justfix.app/mcp
  requires_auth: false
  region: UK
  license: MIT
  repo: https://github.com/Just-Fix/justfix-skill
---

# JustFix Estimator Skill

A drop-in skill that lets your AI agent quote UK trades jobs in real time, and pop the user out to the browser to complete the booking.

JustFix is a UK home-services platform. The skill talks to the public JustFix Estimator MCP server, returns a price breakdown for any of 13 service categories, and produces a tappable booking link the user can complete in their browser.

## When to use this skill

Trigger on any of these intents, in any phrasing:

- "how much for [trades job]"
- "what would [job] cost"
- "estimate for [job]"
- "quote me for [job]"
- "price for a [trade]"
- "book a [trade]"
- "I need a [plumber / electrician / locksmith / etc.]"
- "my [boiler / lock / drain / tap / window] is broken"
- "what services does JustFix do"

If the user is **outside the UK**, mention that JustFix is UK-only and only quote if they confirm they're in the UK or want a UK quote anyway.

## How to use this skill

Three tools are available on the MCP. Use them in this order depending on intent:

### Tool 1: `list_services` (when user asks what's available)

Returns the 13 service categories with their hourly rates. Use when:
- "what services do you offer"
- "what can I book"
- The user mentions a job and you're not sure which service code fits

### Tool 2: `call_out_fee` (when user asks about the booking fee)

Returns the flat call-out fee that applies to every booking. Use when:
- "is there a call-out charge"
- "what's the minimum"
- The user wants to understand the total cost ahead of confirming

### Tool 3: `service-estimate-card` (the main one – generates a quote)

Required arguments:
- `service_code` (string) – one of the codes from the service-code map below
- `booking_description` (string) – a clear one-sentence description of the work

Optional arguments:
- `estimate` (number, default 1) – hours estimated to complete the job
- `work_items` (array of strings) – optional list of specific tasks within the job

Returns the cost breakdown and a unique booking URL the user can tap to complete the booking on https://my.justfix.app.

## Service-code map

Map natural-language descriptions to the right `service_code`:

| User says | service_code | £/hr |
|---|---|---|
| electrician, electrical, sockets, lights, wiring, fuse box, fuse | `electrical` | £90 |
| plumber, plumbing, leak, dripping tap, blocked sink, water pressure | `plumbing` | £90 |
| locksmith, lock, locked out, change locks, key | `locksmith` | £90 |
| glazier, glazing, broken window, broken glass, replace glass | `glazing` | £80 |
| carpenter, carpentry, wooden door, skirting, floorboards, joinery | `carpentry` | £90 |
| handyman, handyperson, odd jobs, mounting, assembly, picture hanging | `handyman` | £80 |
| heating, gas heating, boiler not working, radiator, central heating | `heating_and_gas` | £90 |
| gas appliance, gas hob, gas oven, gas cooker, gas safety | `gas_appliances` | £90 |
| roofer, roofing, roof leak, slipped tiles, gutters | `roofing` | £80 |
| drains, blocked drain, sewer, drainage, blocked toilet | `drains` | £90 |
| white goods, dishwasher, washing machine, tumble dryer, fridge | `white_goods` | £55 |
| boiler service, annual boiler check, gas safety certificate, CP12 | `boiler_service` | £70 |
| anything else / unsure | `something_else` | £80 |

If the user describes a job that could fit two codes (e.g. "my dishwasher is leaking" – could be `plumbing` or `white_goods`), pick the more specific one (`white_goods`) and mention you assumed that.

## Default-hours estimates

If the user doesn't say how long the job is, use these sensible defaults:

| Service | Default hours | Notes |
|---|---|---|
| `boiler_service` | 1 | Fixed-scope annual check, 1 hour is standard |
| `locksmith` | 1 | Lock changes take ~1hr |
| `gas_appliances` | 1-2 | Simple install / safety check |
| `white_goods` | 1 | Most diagnostics + repairs |
| `electrical` | 2 | Variable – ask if scope is bigger |
| `plumbing` | 2 | Variable – ask if scope is bigger |
| `glazing` | 2 | Small window replacement |
| `carpentry` | 2 | Standard repair / install |
| `handyman` | 2 | Catch-all |
| `heating_and_gas` | 2 | Diagnostics + simple fix |
| `drains` | 2 | Clearance + camera survey if needed |
| `roofing` | 3 | Minimum useful site visit |
| `something_else` | 2 | Catch-all default |

**Always tell the user how many hours you've estimated** so they can correct you. The estimate is just a starting point.

## How to render the response

After calling `service-estimate-card`, render the response as a clean, channel-appropriate card. Always include:

1. **Service name and brief scope** (one line)
2. **Cost breakdown** as a table or list
3. **The tappable booking URL** – `[Complete booking →](URL)` if your channel renders markdown, otherwise the raw URL
4. **Honest scope caveat** – the engineer may take more or less time, the final invoice reflects actual time

### Markdown template (works in OpenClaw, Hermes, Claude Code, Cursor, Telegram, Slack)

```markdown
🔧 **[Service Name] Estimate**

**Scope:** [booking_description]
**Estimated duration:** [estimate] hour(s)

| Line | Amount |
|---|---|
| Labour ([hrs] × £[rate]/hr) | £[hrs × rate] |
| Call-out fee | £50.00 |
| **Total estimate** | **£[total]** |

📅 **[Tap to complete booking →]([booking_url])**

_The final invoice will reflect actual time spent on the job._
```

### Plain-text template (for surfaces without markdown)

```
JustFix [Service Name] estimate
Scope: [booking_description]
Estimated duration: [estimate] hour(s)

Labour: £[hrs × rate]
Call-out fee: £50.00
Total estimate: £[total]

Complete booking: [booking_url]

Final invoice reflects actual time spent.
```

### Inline-button hint (channels that support it)

If your channel exposes inline buttons (Telegram `inlinebuttons`, Slack blocks, Discord buttons), render the booking URL as a button labelled "📅 Book this job" pointing at the `booking_url`. The URL is unique per estimate – use exactly what the MCP returns.

## What the skill can and can't do

**CAN:**
- Quote any of the 13 JustFix service categories
- Tell the user the hourly rate, call-out fee, and total estimate
- Generate a unique booking link the user can tap to complete the booking on the JustFix website (a browser pop-out – they finish the booking on `my.justfix.app`)
- Handle scope changes ("actually make it 3 hours") – just call the tool again with the updated `estimate`

**CAN'T:**
- Complete the booking itself (needs customer auth and a real form on `my.justfix.app`)
- Check engineer availability (not exposed via MCP – the booking page handles this)
- Take payment (handled on the booking page after the customer confirms)
- Quote outside the UK (JustFix is UK-only)
- Quote materials or parts (this is a labour-only estimate)

When the user is ready to book, **send them the URL**. The booking page asks for their details, postcode, preferred date, and payment.

## Tracking and attribution

Each `service-estimate-card` call returns a URL with a unique `chatgpt_booking_link_id` UUID query parameter. JustFix uses this to attribute MCP-driven bookings. Don't strip or modify the URL – pass it through to the user exactly as returned.

## Sample conversation

**User:** How much for someone to come and fix my dripping kitchen tap?

**Agent:** _Calls `service-estimate-card` with `service_code=plumbing`, `estimate=1`, `booking_description="Diagnose and repair dripping kitchen tap, replace washers or cartridge if needed."`_

🔧 **Plumbing Estimate**

**Scope:** Diagnose and repair dripping kitchen tap, replace washers or cartridge if needed.
**Estimated duration:** 1 hour

| Line | Amount |
|---|---|
| Labour (1 hr × £90/hr) | £90.00 |
| Call-out fee | £50.00 |
| **Total estimate** | **£140.00** |

📅 **[Tap to complete booking →](https://my.justfix.app/booking/add-detail?service=plumbing&chatgpt_booking_link_id=...)**

_The final invoice will reflect actual time spent on the job. If you'd like a bigger or smaller estimate, just say._

## Installation per harness

See the `install/` folder of the repo for per-harness setup:

- **OpenClaw** – `install/openclaw.md`
- **Hermes** – `install/hermes.md`
- **Claude Code** – `install/claude-code.md`
- **Cursor** – `install/cursor.md`
- **Codex CLI** – `install/codex-cli.md`
- **Gemini CLI** – `install/gemini-cli.md`

All harnesses follow the same pattern: register the MCP endpoint, then put this `SKILL.md` somewhere the agent's skill discovery can find it.

## Support

- Bugs / feature requests: https://github.com/Just-Fix/justfix-skill/issues
- Support policy: https://www.justfix.app/support-policy
- JustFix MCP server bugs (the underlying API): see the support policy above or contact JustFix via https://justfix.app

## License

MIT – see LICENSE in the repo. You can use, modify, distribute, and embed this skill anywhere, commercially or not, with attribution.
