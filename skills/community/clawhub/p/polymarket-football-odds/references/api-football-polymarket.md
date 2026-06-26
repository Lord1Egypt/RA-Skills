# API Reference

Official sources to re-check before changing endpoint behavior:

- API-Football v3 documentation: `https://www.api-football.com/documentation-v3`
- Polymarket market data docs: `https://docs.polymarket.com/market-data/fetching-markets`
- Polymarket Gamma API base observed in official docs and live API responses: `https://gamma-api.polymarket.com`

## Polymarket

- Base URL: `https://gamma-api.polymarket.com`
- Fetch an event by URL slug: `GET /events/slug/{slug}`
- Fallback event query: `GET /events?slug={slug}`
- Fetch a market by URL slug: `GET /markets/slug/{slug}`
- Fallback market query: `GET /markets?slug={slug}`
- Gamma event and market discovery endpoints are public. Do not use trading/order endpoints for this skill.

Polymarket URLs normally expose the event slug as the path segment after `/event/`.

## API-Football / API-SPORTS

- Base URL: `https://v3.football.api-sports.io`
- Auth header: `x-apisports-key: <API_FOOTBALL_KEY>`
- API responses use a wrapper with `errors`, `results`, `paging`, and `response`.
- Useful endpoints:
  - `GET /teams?search={name}`: find API-Football team IDs.
  - `GET /fixtures?date=YYYY-MM-DD`: list fixtures for a date.
  - `GET /fixtures?team={id}&next=20`: fallback when no date is available.
  - `GET /fixtures?id={id}`: fetch a specific fixture.
  - `GET /predictions?fixture={id}`: get API-Football prediction output for one fixture.

The predictions response contains a `predictions.percent` object with `home`, `draw`, and `away` probabilities. Map those to the fixture's home and away teams, not necessarily to the order teams appeared in the Polymarket title.

## Practical Rules

- Prefer fixture date matching first because team-name search alone can confuse clubs with similar names, women/youth teams, or national teams.
- Search plus/minus one day by default because Polymarket and API-Football may expose kickoff dates in different time zones.
- Treat "Draw" as a match outcome, not a team.
- Keep confidence low if only one team name matches or if the best fixture score is close to the runner-up.
- Respect API-Football quota. Avoid repeated broad `/fixtures?date=` calls when a `--fixture-id` is known.
