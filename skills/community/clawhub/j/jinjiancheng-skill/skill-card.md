## Description: <br>
Use when evaluating US stock strategies, ETF positioning, buy/sell points, staged entries, profit-taking, or portfolio rotation through a risk-first, trend-aware lens inspired by Jinjiancheng. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ting2tao](https://clawhub.ai/user/ting2tao) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent operators use this skill to frame US stock, ETF, crypto, portfolio-rotation, and position-sizing questions with a risk-first investment-analysis method. It helps an agent provide conditional market-analysis guidance, not licensed financial advice or trade execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can influence financial decisions about stocks, ETFs, crypto, and portfolio allocation. <br>
Mitigation: Treat outputs as market-analysis framing rather than licensed financial advice; independently verify prices, news, suitability, taxes, and risk before acting. <br>
Risk: Market-sensitive answers may be wrong or stale if real-time data is unavailable or not checked. <br>
Mitigation: Verify current market data and macro news before relying on any buy, sell, hold, or sizing recommendation. <br>
Risk: Portfolio details can expose sensitive personal financial information. <br>
Mitigation: Share only the minimum portfolio context needed for analysis and avoid putting unnecessary private details into search queries. <br>
Risk: The optional Longbridge connection may expose the agent to third-party tool permissions. <br>
Mitigation: Enable Longbridge only after reviewing and accepting that provider's permissions and trust model. <br>


## Reference(s): <br>
- [Jinjiancheng Skill on ClawHub](https://clawhub.ai/ting2tao/jinjiancheng-skill) <br>
- [Longbridge MCP](https://openapi.longbridge.com/mcp) <br>
- [01 Investment Framework](references/research/01-investment-framework.md) <br>
- [02 Buy Sell Signals](references/research/02-buy-sell-signals.md) <br>
- [03 Expression DNA](references/research/03-expression-dna.md) <br>
- [04 Asset Allocation](references/research/04-asset-allocation.md) <br>
- [05 Boundaries And Failure Modes](references/research/05-boundaries-and-failure-modes.md) <br>
- [Local Corpus Notes](references/sources/local-corpus-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown or plain text with optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Typically concise Chinese-language investment-analysis responses with conclusions, rationale, conditions, and invalidation criteria.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
