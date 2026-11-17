## Description:

Use when evaluating US stock strategies, ETF positioning, buy/sell points, staged entries, profit-taking, or portfolio rotation through a risk-first, trend-aware lens inspired by Jinjiancheng.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ting2tao](https://clawhub.ai/user/ting2tao)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to frame US stock and ETF allocation questions, staged entries, profit-taking, and portfolio rotation with a risk-first, trend-aware investment lens. It is best suited for conditional market-analysis guidance that checks current data before giving buy, sell, hold, or allocation suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce actionable trading or allocation guidance that readers may mistake for individualized financial advice.

Mitigation: Treat outputs as educational analysis, require user-specific suitability context, and seek independent financial advice before acting.

Risk: Market recommendations can become stale or misleading without current price, macroeconomic, and issuer-specific data.

Mitigation: Verify current market data before giving advice and express recommendations as conditional scenarios with clear failure conditions.

Risk: The README installation command is unpinned, so later package changes could differ from the reviewed release.

Mitigation: Install from an immutable reviewed commit or pinned release whenever possible.

## Reference(s):

- [Investment Framework](references/research/01-investment-framework.md)
- [Buy Sell Signals](references/research/02-buy-sell-signals.md)
- [Expression DNA](references/research/03-expression-dna.md)
- [Asset Allocation](references/research/04-asset-allocation.md)
- [Boundaries And Failure Modes](references/research/05-boundaries-and-failure-modes.md)
- [Local Corpus Notes](references/sources/local-corpus-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown prose with concise conclusions, supporting rationale, conditions, and risk caveats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Usually 200-400 Chinese characters for ordinary strategy questions; longer only for multi-asset comparisons.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
