## Description:

Poly Master helps agents discover and analyze Polymarket prediction markets, prepare wallet-signed trades, evaluate copy-trading candidates, track portfolios, and review hedge-strategy signals using the Antalpha AI MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deanpeng-dotcom](https://clawhub.ai/user/deanpeng-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect Polymarket markets, review wallet and trader performance signals, generate user-signed order flows, monitor positions and PnL, and assess hedge opportunities before deciding whether to trade.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can support real-money Polymarket trading and copy-trading workflows.

Mitigation: Treat all trading, copy-trading, and hedge outputs as decision support only, set conservative limits, and require the user to verify every order before wallet signing.

Risk: Credential persistence for agent registration is described but secure API-key storage is not fully specified.

Mitigation: Store agent credentials only in an approved secret store and avoid exposing keys in prompts, logs, screenshots, or shared configuration.

Risk: Hedge execution guidance is inconsistent because security evidence notes unsupported hedge-execution instructions.

Mitigation: Use hedge tools for scanning and analysis unless execution support is explicitly verified, and do not promise automatic two-leg hedge execution.

Risk: Prediction-market availability and trading rules can vary by jurisdiction.

Mitigation: Require users to confirm local compliance and Polymarket account eligibility before using trading or copy-trading features.

Risk: Wallet, trader, and enrichment data may be incomplete or unavailable.

Mitigation: Explain missing enrichment as incomplete information, not as reduced risk, and avoid recommending trades based solely on absent data.

## Reference(s):

- [Poly Master on ClawHub](https://clawhub.ai/deanpeng-dotcom/skills/poly-master)
- [Publisher profile](https://clawhub.ai/user/deanpeng-dotcom)
- [Antalpha AI MCP endpoint](https://mcp-skills.ai.antalpha.com/mcp)
- [Antalpha AI](https://ai.antalpha.com)
- [Polymarket](https://polymarket.com)
- [Quick Start Guide](docs/quickstart.md)
- [Skill Instructions](SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown responses with market summaries, order previews, signing links, wallet and trader analysis, portfolio reports, and hedge-signal explanations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet-signing URLs, QR-code instructions, risk-limit settings, and MCP tool-call guidance; users must verify order details before signing.]

## Skill Version(s):

3.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
