# Automated slate scan notes

## Purpose
Use this when the user wants "today's games", "tomorrow's games", or "all tradable games" without naming a single fixture.

## Pattern
- Query the active market list at runtime; do not rely on one hardcoded search string.
- Prefer a World Cup scoped search first, then fall back to the full active list if the scoped search is sparse.
- Filter by `resolves_at` in UTC, then keep only questions that actually contain a fixture pair.
- Canonicalize both teams through `scripts/team_names.py` before comparing model and market labels.
- Report the raw market question plus canonical team names so multilingual aliases are visible to the user.

## Pitfalls
- Alias-heavy fixtures can hide under a different spelling (`Ivory Coast` vs `Côte d'Ivoire`, `Curacao` vs `Curaçao`, `South Korea` vs `Korea Republic`).
- A date-only slice may miss a fixture if the user is asking about a broader slate.
- Props and futures can share the same team names but are not the same class as a 3-way fixture market.

## Verification
When the scan is working, it should surface a list of candidate fixtures automatically without the user needing to suggest the country names first.
