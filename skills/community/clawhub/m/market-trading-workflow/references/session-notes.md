# Session notes: market trading workflow

This skill now bundles the World Cup research model alongside the execution script.

## Bundled pieces
- `scripts/football_worldcup_model.py` computes win/draw/loss probabilities from competitive international results.
- `scripts/clawhub_trader.py` is the conservative execution layer that discovers the market, validates the fixture, and passes when context is fragile.

## Compatibility lesson
The deployed `simmer-sdk` available in this environment exposed `SimmerClient.get_markets()` with a narrower signature than newer docs examples. The skill should therefore:
- prefer runtime discovery
- avoid assuming `tags`, `sort`, or `venue` are available on every install
- fall back safely to the supported kwargs rather than crashing

## Name-matching lesson
Markets and model inputs often use different canonical team names. The skill now shares one normalization module across research and execution, so both sides stay aligned:
- `South Korea` ↔ `Korea Republic` / `Republic of Korea`
- `Bosnia` ↔ `Bosnia and Herzegovina` / `Bosnia-Herzegovina`
- keep the raw market label for user-facing reporting, but use the shared canonical form for pricing and lookup
- when discovery returns multiple candidates, score the event/question text and choose the best match rather than blindly taking the first hit
- paper trading on the sim venue should submit by default, while `--live` remains required for real-money execution
- moderate underdogs can size down, but extreme longshots should not be force-bet just because they are the opposite side
- the reporting contract should expose `model_yes/model_no` and `market_yes/market_no` instead of only a single fair probability

## Publishing lesson
Publishing worked only after:
- switching to an eligible ClawHub account
- logging in with device flow
- republishing the skill slug `market-trading-workflow` with the display name `World Cup Head to Head Fixture Trader`

## Operational note
The skill is intentionally conservative and should keep failing closed when the market context is unclear, stale, or mismatched to the intended fixture.
