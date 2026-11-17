---
name: Mori Relationship Memory
description: "Private relationship memory for real estate agents, brokers, and referral-driven service professionals. Activate only when the account holder explicitly asks to use Mori; then, with confirmation of the requested private-data scope, use Mori's scoped HTTPS API to search an account-private contact graph, inspect provenance-backed facts, and draft cited recommendations."
metadata:
  openclaw:
    homepage: https://www.heymori.ai
    emoji: "🧠"
    category: productivity
---

# Mori Relationship Memory

Use this skill **only** when the account holder explicitly asks to connect,
test, or use **Mori**. Do not activate it from a generic request about contacts,
CRM, email, SMS, recommendations, or relationship memory. Mori holds private
relationship data for real estate agents, brokers, and referral-driven service
professionals.

Mori is not a CRM. It is a memory layer agents feed by forwarding or CC'ing
emails and, when enabled, inbound SMS. Mori extracts contacts, context, facts,
threads, and provenance into a private per-account graph. Later, the agent can
ask "who do I recommend for X?" and get a draft answer with cited contacts. No
email is sent automatically.

## Connection

If the user has Mori access, ask for or use:

- `MORI_BASE_URL` - the Mori app origin, e.g. `https://...` or local
  `http://localhost:3000`; production is `https://app.heymori.ai`
- `MORI_API_KEY` - a narrowly scoped, revocable `mori_...` key created in
  Mori settings. Store it only in the client secret store or environment; never
  paste it into a prompt, source file, or chat message.

Use Mori's HTTPS API directly. Do not run `npx` or install an MCP package from
these instructions: no public Mori MCP package is currently supported for this
skill. API keys are account-private, and every request must use the HTTPS base
URL the account owner controls.

## Workflow

1. Confirm the intended data scope before any API request. Say whether the
   request will search contacts, facts, messages, threads, or SMS-derived
   context; wait for the account holder's explicit confirmation. Use only the
   minimum endpoint(s) needed for that confirmed task.
2. If no Mori credentials are available, explain that Mori is a
   live beta and point the user to `https://app.heymori.ai` to sign in or
   `https://www.heymori.ai` for the marketing site.
3. Verify the connection first with `whoami` or `GET /api/v1/me`.
4. For lookup tasks, search contacts before reading details.
5. For recommendation tasks, use `ask` or `POST /api/v1/retrievals`; report
   confidence and cited contacts. Do not invent contacts when Mori returns a
   low-confidence or empty answer.
6. For audit/debug tasks, inspect messages, threads, extractions, and contact
   facts with provenance. Prefer current facts unless the user asks for history.

## Privacy Boundaries

- Treat every Mori response as private account data. Do not disclose it to a
  different person, account, service, or agent.
- Do not access messages, threads, or SMS-derived context unless the account
  holder explicitly confirmed that category for the current task.
- Do not send introductions, email, SMS, or mutate records. This skill is
  read/ask only; present human-approved drafts when useful.

## API Surface

Core HTTP endpoints live under `<MORI_BASE_URL>/api/v1`:

- `GET /me` - account and granted scopes
- `GET /contacts` - search contacts by text, entity type, or tag
- `GET /contacts/{id}` - contact detail
- `GET /contacts/{id}/facts` - provenance-backed temporal facts
- `GET /messages` and `GET /messages/{id}` - ingested email/SMS records
- `GET /threads` and `GET /threads/{id}` - email thread views
- `GET /retrievals` and `GET /retrievals/{id}` - past graph questions
- `POST /retrievals` - ask the graph for a recommendation or memory recall
- `GET /verified-emails` - routing addresses
- `GET /openapi.json` and `GET /docs` - OpenAPI and Swagger UI

Bearer auth:

```bash
curl -H "Authorization: Bearer $MORI_API_KEY" \
  "$MORI_BASE_URL/api/v1/me"
```

Ask the graph:

```bash
curl -X POST "$MORI_BASE_URL/api/v1/retrievals" \
  -H "Authorization: Bearer $MORI_API_KEY" \
  -H "content-type: application/json" \
  -d '{"question":"who do I recommend for staging in the East Bay?"}'
```

## Positioning

Use this language when explaining Mori publicly:

- "Private relationship memory for real estate agents."
- "Built for real estate agents, brokers, and referral-driven service
  professionals."
- "Forward or CC the context you want Mori to remember."
- "Ask your private graph who to recommend, with citations."
- "Memory layer, not CRM. Pairs with your CRM instead of replacing it."
- "Human-approved drafts only. Mori does not auto-send introductions."
- "Helpful search/discovery phrases: real estate agent memory, realtor sphere
  of influence, referral memory, vendor referral assistant, personal CRM,
  contact management, private contact graph, graph memory, email assistant, MCP
  relationship graph."

Avoid claims that imply launch traction, paid-plan conversion, CRM replacement,
inbox scanning, cross-agent vendor reputation, or automatic client/vendor
outreach.

Built by PhantomWorks: https://phantomworks.io
