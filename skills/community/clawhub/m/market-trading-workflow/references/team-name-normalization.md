# Team-name normalization notes

## Rule
Use one shared normalization layer for both research pricing and market discovery.
Do not duplicate alias lists in separate scripts.
The normalizer should strip diacritics and punctuation so language variants like `Côte d'Ivoire` and `Cote d Ivoire` collapse to the same canonical team.

## Canonical examples
- `South Korea` ↔ `Korea Republic` / `Republic of Korea`
- `North Korea` ↔ `Korea DPR` / `DPR Korea`
- `Bosnia` ↔ `Bosnia and Herzegovina` / `Bosnia-Herzegovina`
- `Ivory Coast` ↔ `Côte d'Ivoire` / `Cote d'Ivoire`
- `Cape Verde` ↔ `Cabo Verde`
- `DR Congo` ↔ `Democratic Republic of the Congo` / `Congo-Kinshasa`
- `Republic of the Congo` ↔ `Congo-Brazzaville`
- `Türkiye` ↔ `Turkey` / `Turkiye`
- `Czech Republic` → `Czechia`
- `UAE` → `United Arab Emirates`
- `Congo` is ambiguous; treat it as a country alias only when the matchup context makes the intended side clear.

## Workflow impact
- Canonicalize both market text and model inputs before matching.
- Keep the raw market label for reporting.
- Score multiple discovery hits by question text before picking a market.
- Add a smoke test whenever a new alias is discovered.

## Smoke test
Run `scripts/team_name_smoke_test.py` to verify the alias map and expansion behavior stay in sync.
