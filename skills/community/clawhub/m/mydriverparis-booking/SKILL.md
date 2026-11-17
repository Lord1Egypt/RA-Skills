---
name: mydriverparis-booking
description: Get instant quotes and book private chauffeur rides in Paris and across Europe with MyDriverParis — airport & train station transfers, hourly hire, day trips, VIP airport Meet & Greet. Public MCP server, no API key needed.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🚘"
    homepage: https://www.mydriverparis.com
---

# MyDriverParis — private chauffeur quotes & booking (Paris / France / Europe)

MyDriverParis is a licensed Paris chauffeur company (since 2012, 100% Mercedes-Benz fleet, fixed all-inclusive prices). It exposes a **public MCP server** — no API key, no account:

```
https://mcp-mydriverparis.mydriverparis.workers.dev/mcp
```

## Setup (once)

```bash
openclaw mcp add mydriverparis \
  --url https://mcp-mydriverparis.mydriverparis.workers.dev/mcp \
  --transport streamable-http
```

Verify with `openclaw mcp probe mydriverparis` — you should see 9 tools. (MCP tools are available in the default/embedded runtime with the `coding` and `messaging` tool profiles; if they don't appear, check your runtime and profile.)

## When to use

The user wants a price or a booking for a private driver with pickup **or** drop-off in France: airport/station transfer, city-to-city ride (e.g. Paris → Brussels/London/Nice), hourly chauffeur (3h minimum), private day trip (Versailles, Champagne, D-Day beaches…), or a VIP airport **Meet & Greet** (personal escort through the terminal, incl. EES fast track at CDG).

## Workflow

1. **Fuzzy locations** ("CDG", "our hotel", "Le Bristol") → call `resolve_location` first and use the canonical address.
2. **Airport pickup** → always ask the flight number, then `resolve_flight` (pickup = arrival + 45 min international / + 25 min Schengen). **Station pickup** → ask the train number, then `resolve_train` (digits only, e.g. `9211`; a 6-char code like `JWVLHH` is a PNR, not a train number).
3. `get_quote` (`pickup_date` in **dd/mm/yyyy**, Paris time) → returns per-vehicle prices and a `quote_id` valid **15 minutes**. Present the options; heed any `warning` field.
4. Confirm vehicle + collect passenger name, email, phone (E.164).
5. `book_ride` with `quote_id`, `vehicle_id`, passenger details, `flight_number` if any, and a fresh UUID `idempotency_key`. It returns a **secure Stripe payment link** — hand it to the user on its own line.
6. The booking is confirmed **only after payment**. Never say "confirmed" before.

For Meet & Greet use `book_meetgreet` (fixed prices — do **not** call `get_quote` for the M&G part). For cancellation/modification questions, call `get_cancellation_policy` — never guess.

## Hard rules

- **Never invent a price** — always `get_quote` or the fixed Meet & Greet table.
- Quote expired (`QUOTE_EXPIRED_OR_UNKNOWN`)? Re-run `get_quote`; the price is locked server-side.
- Errors come as `{code, message, retriable, suggested_action}` — follow `suggested_action`.
- Trips must start or end in France; anything else, direct the user to contact@mydriverparis.com.

Docs for agents: https://www.mydriverparis.com/llms-full.txt · Human support: +33 1 88 33 64 43 (24/7).

*This skill is published by MyDriverParis (SARL KAVENTURE), the operator of the service. Booking payments go through Stripe; the skill itself is free and collects nothing.*
