## Description:

Provides Chinese-language stock position management and risk-control guidance focused on trailing stops, scaled take-profit plans, core-satellite allocation, portfolio rebalancing, and trading psychology for users who already hold positions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georgetao730](https://clawhub.ai/user/georgetao730)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to assess an existing stock position, calculate profit/loss and position concentration, and produce a concise risk-management plan with stop-loss, take-profit, rebalancing, and psychology guidance. It is not a stock-picking skill and should not be treated as personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce concrete trading percentages and price levels that users may mistake for personalized investment advice.

Mitigation: Treat outputs as educational position-risk guidance, independently verify assumptions and market data, and make final trading decisions outside the skill.

Risk: Optional market-price lookup may be unavailable, stale, or incorrect, and depends on optional Python packages.

Mitigation: Verify market data independently, provide a manual current price when appropriate, and install optional dependencies in a reviewed virtual environment with pinned versions.

Risk: Position-management rules may not fit every user's risk tolerance, jurisdiction, tax situation, or portfolio constraints.

Mitigation: Review generated plans against the user's full portfolio, financial constraints, and applicable professional or regulatory requirements before acting.

## Reference(s):

- [Risk Management Rules](references/risk-rules.md)
- [Trading Psychology](references/trading-psychology.md)
- [Trailing Stop Guide](references/trailing-stop-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include concrete buy/sell percentages, price levels, stop-loss levels, risk labels, and position-management suggestions.]

## Skill Version(s):

1.3.0 (source: server release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
