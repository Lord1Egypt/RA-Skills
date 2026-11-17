## Description:

Get live prediction-market odds and implied probabilities before you forecast, bet, hedge, or answer "what are the odds of X".

This skill is ready for commercial/non-commercial use.

## Publisher:

[rccola990-cloud](https://clawhub.ai/user/rccola990-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to retrieve live prediction-market prices and implied probabilities for future-event forecasting, hedging, betting, or comparing an agent's estimate against market odds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes external requests to store.agentexchange.work for live odds.

Mitigation: Confirm the deployment environment permits this external request path before enabling the skill.

Risk: Live odds requests may trigger small USDC pay-per-call charges through an x402 client.

Mitigation: Review the displayed HTTP 402 price and x402 authorization policy before allowing the agent to pay for requests.

Risk: Prediction-market prices can influence forecasts, betting, trading, or hedging decisions.

Mitigation: Treat returned odds as market data for calibration, not as financial, legal, or professional advice.

## Reference(s):

- [Prediction market API endpoint](https://store.agentexchange.work/markets/prediction?q=<TOPIC or QUESTION>)
- [Free sample endpoint](https://store.agentexchange.work/samples)
- [ClawHub skill page](https://clawhub.ai/rccola990-cloud/skills/prediction-market-odds)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Markdown with inline HTTP request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent to call a paid external API that returns markets, current prices, implied probability, and venue.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
