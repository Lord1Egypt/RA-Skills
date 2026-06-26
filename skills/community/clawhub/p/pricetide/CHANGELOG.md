# Changelog

## 1.0.0

Release theme: turn shopping advice into a timing decision instead of a location comparison.

What ships:
- add the new `PriceTide` skill
- position it as a dedicated buy-timing layer for mainland China shopping scenarios
- default the output to four verdicts: `现在买`, `等等看`, `先关注，等活动`, and `不值得追这个价`
- teach the skill to weigh current payable price, recent price clues, promotion rhythm, urgency, and the downside of waiting
- add launch README, release notes, package metadata, and ClawHub publishing materials
- add `scripts/publish.sh` so the skill can be published directly from the skill directory

Suggested one-line changelog:
- Launch PriceTide, a buy-timing decision skill that judges whether the current price is a buy-now window, a wait candidate, an event-watch case, or not worth chasing.
