## Description:

Query BTC/ETH perpetual contract market data, discover newly listed tokens, and retrieve structured listing research reports from Hotcoin Exchange.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xss4755](https://clawhub.ai/user/xss4755)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to access public Hotcoin BTC/ETH futures data, discover newly listed tokens, and summarize listing research for recently listed tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Hotcoin public API and Learn pages for market and research data.

Mitigation: Install only when outbound access to the listed Hotcoin domains is acceptable.

Risk: Exchange-provided token research can be mistaken for independent financial advice.

Mitigation: Treat research summaries as informational and verify important claims with independent sources before making investment decisions.

Risk: Hotcoin public endpoints may rate limit repeated requests.

Mitigation: Retry rate-limited requests slowly and avoid high-frequency polling through the agent.

## Reference(s):

- [Hotcoin homepage](https://www.hotcoin.com)
- [Hotcoin Learn](https://www.hotcoin.com/zh_CN/learn/index/)
- [ClawHub skill listing](https://clawhub.ai/xss4755/skills/hotcoin-ai-skill)
- [Hotcoin public spot API endpoint](https://api.hotcoinfin.com)
- [Hotcoin perpetual contract API endpoint](https://api-ct.hotcoin.fit)

## Skill Output:

**Output Type(s):** [Text, JSON, API calls, Guidance]

**Output Format:** [Markdown text with structured JSON data when listing reports are requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public market and research data; no credentials or trading permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
