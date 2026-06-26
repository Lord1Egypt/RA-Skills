# OpenClaw Decision-Support API Quick Reference

Base path:

- `/api/v1/agent`

Required user-managed variables:

```bash
OPENCLAW_AGENT_API_BASE_URL=http://your-host:8080/api/v1/agent
OPENCLAW_AGENT_API_KEY=your-own-bearer-token
```

Important:

- these values must be created and managed by the OpenClaw user in their own environment
- this skill only tells the user which variables are required
- this skill does not manage API tokens, provision credentials, or mutate the user's OpenClaw configuration on its own

Usage convention:

- load these variables through the user's OpenClaw configuration layer before calling the API
- send `Authorization: Bearer $OPENCLAW_AGENT_API_KEY`
- treat `OPENCLAW_AGENT_API_BASE_URL` as the canonical base path

Primary PM discovery endpoints:

- `GET /events`
  - use for PM-official event discovery and scope expansion
  - useful query params:
    - `tag_slug`
    - `limit`
    - `offset`
    - `active`
    - `closed`
    - `archived`
    - `order`
    - `ascending`
- `GET /events/{event_id}`
  - use for one event's official metadata and a light market preview
- `GET /events/{event_id}/markets`
  - use for event-internal market enumeration before deeper filtering
  - useful query params:
    - `active_only`

Primary read-only endpoints:

- `GET /markets`
  - use for local tradability discovery
  - useful query params:
    - `sport`
    - `league`
    - `chain`
    - `market_domain`
    - `match_epoch_from`
    - `match_epoch_to`
    - `limit`
    - `status`
    - `include_orderbook`
    - `group_by=market_domain`
- `GET /markets/{market_id}/fair`
  - final fair and edge inputs for one market
- `GET /markets/{market_id}/orderbook`
  - top book and top-3 depth for one market
- `GET /markets/{market_id}/check`
  - final state classification and reasons
- `GET /health`
  - backend freshness and chain counts

Parameter notes:

- `tag_slug`
  - PM official tag slug such as `nba`, `soccer`, `sports`, `politics`
  - use this first when the user needs to expand scope beyond the current local refresh universe
- `order`
  - PM official event ordering field
  - default is `volume24hr`
  - keep this default unless there is a specific reason to sort differently
- `active`, `closed`, `archived`
  - discovery filters on official event lifecycle
  - default scan should be `active=true`, `closed=false`, `archived=false`
- `match_epoch_from`, `match_epoch_to`
  - explicit Unix-second window filters on the local tradable market layer
  - use these instead of vague text windows whenever possible
- `group_by=market_domain`
  - use only when the user wants a grouped overview by category such as `nba`, `ncaab`, `soccer5`

External behavior assumptions:

- `status` / `data_status` is agent-facing:
  - `tradable`
  - `watch`
  - `unpriced`
- `fair` is final fair only
- internal pricing source is intentionally hidden

Best practice:

1. Use `/events` first when PM-official discovery or scope expansion is needed.
2. Use `/events/{event_id}/markets` to enumerate markets within one event.
3. Use `/markets` when only locally-evaluable, tradability-aware candidates are needed.
4. Use `match_epoch_from` and `match_epoch_to` for explicit time-window scans.
5. Use `/fair` + `/check` on the shortlisted set.
6. Use `/orderbook` only when deeper inspection than top-of-book summary is needed.

Important distinction:

- `/events*` is the PM-official discovery layer
- `/markets*` is the local trading-evaluation layer
- do not treat `/events` results as final conclusions without checking `/markets/{market_id}/check`

Current local sports coverage note:

- NBA is exposed through the local `/markets` layer
- Basic soccer is also exposed through the local `/markets` layer as `market_domain=soccer5`
- For soccer opportunity discovery, prefer:
  - `GET /markets?market_domain=soccer5`
  - optionally with `match_epoch_from`, `match_epoch_to`, and `status=tradable`
- Do not assume every soccer-derived market family is available just because PM official discovery can see the event
