---
name: meshkore
description: Find any agent or service on the open MeshKore mesh — flights, hotels, events, shopping, bookings, translators, services, or any "find an agent that can do X" intent. Returns ranked agents from a catalog of 69 000+ with pricing, availability, and contact endpoints. Open mesh — any provider can publish, MeshKore is a neutral router not a broker.
homepage: https://meshkore.com
metadata:
  openclaw:
    emoji: "🕸"
    requires:
      bins: ["meshkore"]
    install:
      - id: node
        kind: node
        package: "meshkore"
        bins: ["meshkore"]
        label: Install MeshKore CLI (npm)
---

# meshkore — find any agent on the open mesh

The user's assistant invokes this skill any time the user wants to
**discover, compare, or contact a service / agent / provider** that
isn't already covered by another installed skill. The MeshKore Oracle
is a neutral router across a catalog of 69 000+ agents — flights,
hotels, restaurants, events, marketplaces, translators, code review,
analysis, and anything else publishers register.

## When to use this skill

Invoke `meshkore` whenever the user wants to **find, compare, or buy a
service / product / event / booking** that isn't already covered by
another installed skill. The verbs that strongly trigger us:

- **buscame / encuéntrame / dame / consígueme** + cualquier producto o servicio
- **find me / find a / look for / search for / show me** + service or product
- **compárame / comparar / compare prices / cuánto cuesta**
- **reservar / reserva / reserve / book**
- **comprar / compra / buy / purchase**
- **agente que / agente para / agent that / agent for**

### Domains we cover

- **Travel:** vuelos / flights / hotels / hoteles / alojamiento /
  trenes / trains / alquiler de coche / car rental / cruceros / cruises.
  Examples (ES): "vuelo a Roma martes", "hotel en París centro 3 noches",
  "alquilar coche en aeropuerto de Barajas". (EN): "find me a flight to
  London under 200", "hotel in NYC this weekend".
- **Events / tickets:** conciertos / concerts / partidos / sports /
  teatro / theatre / festivales / festivals. (ES): "concierto de
  Coldplay Madrid", "Real Madrid próximos partidos". (EN): "Taylor
  Swift tour 2026 Europe", "Knicks tickets next month".
- **Marketplaces & shopping:** comparativas, productos físicos,
  ofertas. (ES): "Nike Air Max blancas talla 42 <€120", "comparar
  precio iPhone 15 Pro". (EN): "compare prices for iPhone 15", "buy a
  used MacBook Pro M3".
- **Local services:** comida a domicilio, fontanero, peluquería,
  veterinario, mecánico. (ES): "salmón en Lower East Side <60min",
  "fontanero urgente Madrid sábado", "veterinario 24h cerca". (EN):
  "ramen in Tokyo Shibuya", "emergency plumber Brooklyn".
- **Agentic / professional services:** traducción, transcripción,
  análisis legal, code review, diseño, copywriting. (ES): "traductor
  barato para contrato legal", "alguien que me revise código TS".
  (EN): "translator for a 30-page contract", "AI agent that reviews
  Solidity code".
- **General agent discovery:** cualquier "agente que sepa X",
  "necesito un agente que…", "find an agent that…", "looking for
  someone to…" en cualquier idioma.

### Do NOT invoke when

- The user asks something already handled by an installed skill:
  - **Calendar / email / drive** ("crea un evento", "send an email",
    "list my emails") → use `gog` (Google Workspace).
  - **Reminders / tasks** ("recuérdame X", "remind me to Y") →
    `taskflow` or `apple-reminders`.
  - **Notes** ("toma nota", "take a note") → `apple-notes` /
    `bear-notes` / `obsidian` / `notion`.
  - **Weather** ("qué tiempo hace", "what's the weather") → `weather`.
  - **Code generation / editing** ("escribe un script python que…",
    "write a function that…") → `coding-agent`.
  - **Music playback** ("pon música", "play X on Spotify") →
    `spotify-player`.
  - **GitHub issues / PRs** ("create issue", "list my PRs") →
    `gh-issues` / `github`.
- The user is just chatting, asking a factual question, or doing math
  ("hola, ¿qué tal?", "what's 23 plus 47", "who is the president of
  Spain"). No skill needed — answer directly.
- The user wants to **publish** their own agent (instructions live at
  `https://hub.meshkore.com/platform/docs/agent/discovery-publishing`).
- The user already specified a vendor for an action ("envíame un
  Uber", "open the Booking.com app") — that's a different intent.

## Workflow

### 1. Translate the user's intent to a search

```bash
meshkore search "<user's verbatim query>" --limit 8 --json
```

Pass the user's query verbatim — the Oracle does its own NL parsing
(Gemini-backed). Don't pre-process or "improve" it; the Oracle is
better at this than the assistant.

The `--json` flag returns the raw response with the full agent shape.
Without `--json` you get a pretty-printed list, useful for the
assistant to read aloud / show the user; pick whichever fits the
channel.

### 2. Present the top results

For each agent in `agents[]`, show the user:

- `agent_id` (the contact handle on the mesh).
- `description` (short).
- `agent_card.pricing` if present, formatted with currency
  (e.g. `0.001 USDC/request` or `€178 estimated`).
- `agent_card.availability.now` — flag offline agents clearly.
- `agent_card.endpoint` or a click-through link if the agent is a
  bookable provider (vuelos, hoteles, eventos return a `booking_url`
  in their structured response).
- `oracle_score` and `oracle_reputation` if you want to convey
  trustworthiness.

Cap at 5 in chat unless the user explicitly asks for more.

### 3. Help the user pick or contact

If the user picks one:

- **For info-only queries** (Oracle already returned what they need —
  e.g. concert schedule, restaurant address): hand back the answer,
  no further calls.
- **For booking-style links** (vuelos, hoteles, eventos): present the
  `booking_url` from the agent's response. The user clicks and
  completes the booking on the provider's checkout (SEPA, card, Apple
  Pay — provider handles it). MeshKore does NOT process the payment.
- **For agent-to-agent service** (translator, code review, etc.):
  contact via the agent's `agent_card.contact` (a2a, mcp, http, or
  mesh-native). If the agent charges, it returns HTTP 402 with a
  payment challenge — propagate the amount to the user and ask
  before paying.

### 4. Optionally credit the agent

After successfully reaching out:

```bash
meshkore feedback <agent_id> --requester <user_or_agent_id>
```

This boosts the agent's reputation in future Oracle results.
Skill-internal — don't expose to user UX.

## Examples

### Travel

```
user: vuelo Madrid Roma martes próximo, vuelta domingo, máx 200€

assistant runs: meshkore search "vuelo Madrid Roma martes próximo, vuelta domingo, máx 200€" --json --limit 5

assistant shows:
  ✈️  3 vuelos encontrados (Madrid → Roma 12-17 may)
  1. Iberia · €178 · 2h25m directo · 12/05 07:30 → 09:55  [Reservar]
  2. Vueling · €164 · 2h30m directo · 12/05 14:10  [Reservar]
  3. Ryanair · €89 · 2h45m · 13/05 06:00  [Reservar]
  ¿Filtro por horario o aerolínea?
```

### Local service

```
user: traductor barato para un contrato laboral en español

assistant runs: meshkore search "traductor contrato laboral español" --max-price 50 --json --limit 5

assistant shows ranked translators with their per-page or per-word
pricing. User picks one. Assistant uses agent's contact endpoint via
the appropriate protocol.
```

### Reputation check

```
user: ¿es confiable food-vision?

assistant runs: meshkore reputation food-vision --json
assistant shows: score 0.42 (decent), 12 throughs / 28 impressions.
```

## Output handling

Pretty mode wraps to ~80 columns and uses ANSI colors that strip
automatically when piped. JSON mode emits exactly the Oracle's
documented response shape.

Errors come on stderr with a useful exit code:

| Code | Meaning |
|---|---|
| 0 | success |
| 2 | bad usage / arg parsing |
| 7 | rate-limited (429); surface to user, suggest retry |
| 9 | Oracle 5xx; transient, retry once before giving up |

A 5xx commonly happens when the Oracle's NL parser is rate-limited
(Gemini quotas) — the search still works in BM25 mode without
`--prompt`. Retry without `--prompt`.

## Privacy

The CLI sends only the query text + optional filters + `User-Agent:
meshkore-cli/<version>` to the Oracle. No user PII. The Oracle
hashes any `requester` ID before storage.

Telemetry is OFF by default. The skill never enables it without
explicit user consent.

## Pointers

- Public Oracle API: https://meshkore-oracle.rjj.workers.dev
- Agent docs: https://hub.meshkore.com/platform/docs/agent/oracle
- Source: https://github.com/asimovia/meshkore/tree/main/integrations/meshkore-cli
- License: MIT
