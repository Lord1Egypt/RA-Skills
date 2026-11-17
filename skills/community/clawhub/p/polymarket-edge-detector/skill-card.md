## Description:

Polymarket prediction market edge detector that compares binary-option prices against external reference probabilities to surface potential edge in political, sports, and crypto markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

External users, prediction market traders, sports bettors, and DeFi quants use this skill to scan Polymarket-style binary markets for apparent pricing gaps, liquidity, time-to-resolution, and confidence signals. Current outputs should be treated as mock screening data unless the implementation is connected to verified live market and reference sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mock trading signals may be mistaken for real betting or trading advice.

Mitigation: Clearly label outputs as mock/demo data and require verified live market prices plus trusted reference probabilities before using the results for financial decisions.

Risk: Apparent edge scores can be misleading when reference probabilities, liquidity, or resolution timing are stale or unverified.

Mitigation: Review the source data, confidence score, market liquidity, and time-to-resolution before acting on any surfaced opportunity.

## Reference(s):

- [Polymarket CLOB API endpoint](https://clob.polymarket.com)
- [ClawHub skill page](https://clawhub.ai/ssidharhubble/skills/polymarket-edge-detector)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON from the CLI, with concise text or markdown summaries when an agent reports results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes market identifiers, questions, prices, reference probabilities, edge percentages, liquidity, resolution timing, action signals, and confidence scores.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
