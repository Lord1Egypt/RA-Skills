## Description: <br>
Poly Master is a Polymarket prediction-market skill by Antalpha AI for discovering markets, trading outcomes, copy-trading, tracking portfolio and PnL, enriching wallet and trader analysis, reviewing event money flow, and scanning hedge-strategy signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deanpeng-dotcom](https://clawhub.ai/user/deanpeng-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Poly Master in MCP-compatible agents to discover Polymarket markets, analyze wallet, trader, and event data, place or review signed trades, configure copy-trading and risk limits, track portfolios, and scan hedge signals. It supports real-money prediction-market workflows, so agents should present order details and risks before user signing. <br>

### Deployment Geography for Use: <br>
Global, subject to Polymarket availability and local prediction-market regulations. <br>

## Known Risks and Mitigations: <br>
Risk: Real-money prediction-market trades, copy-trading, and hedge signals can lose funds or be restricted by local rules. <br>
Mitigation: Require users to review order details, jurisdiction, position size, and wallet signing pages before signing; use small limits and configured risk controls. <br>
Risk: Security evidence marks the release suspicious because hedge-trading and copy-trading instructions are inconsistent. <br>
Mitigation: Ask the publisher to clarify whether hedge execution and copy-trading require explicit confirmation for each order before installation or use. <br>
Risk: Credential revocation and wallet/profile data handling are not fully clarified in the evidence. <br>
Mitigation: Ask the publisher how to revoke stored agent credentials and how wallet/profile data is retained or shared. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deanpeng-dotcom/poly-master) <br>
- [Publisher profile](https://clawhub.ai/user/deanpeng-dotcom) <br>
- [Poly Master agent instructions](SKILL.md) <br>
- [Poly Master README](README.md) <br>
- [Quick start guide](docs/quickstart.md) <br>
- [Antalpha AI MCP endpoint](https://mcp-skills.ai.antalpha.com/mcp) <br>
- [Antalpha AI](https://ai.antalpha.com) <br>
- [Polymarket](https://polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance] <br>
**Output Format:** [Markdown responses with structured market, order, portfolio, wallet, trader, and hedge-signal summaries; MCP tool calls provide data and signing URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet signing links and QR-code instructions; financial actions require user wallet review and signature.] <br>

## Skill Version(s): <br>
3.0.2 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
