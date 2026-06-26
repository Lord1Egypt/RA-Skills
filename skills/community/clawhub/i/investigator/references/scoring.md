# Scoring

Use scoring as a confidence aid, not proof.

## Suggested signals
- exact username match: +20
- close username variant: +10
- matching display name: +10
- bio overlap: +15
- linked website overlap: +20
- obvious avatar similarity from public pages: +15
- explicit cross-link between accounts: +25
- public email-derived clue such as matching Gravatar/profile identity: +10

## Penalties
- conflicting display name or branding: -10
- clearly different geography / language / identity cues: -10
- empty or nearly empty profile: -5
- platform result too weak to verify: -5

## Confidence bands
- 0-24: weak
- 25-49: possible
- 50-74: likely
- 75+: strong

## Rule
Never present the numeric score as certainty. Present it as confidence based on public evidence.
