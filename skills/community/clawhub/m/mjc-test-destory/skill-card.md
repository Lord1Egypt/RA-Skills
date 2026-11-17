## Description:

ValueScan Skill Beta helps agents query ValueScan cryptocurrency market APIs for major fund-flow analysis, whale and wallet monitoring, sector rotation, opportunity and risk token signals, large-holder cost analysis, and support or resistance data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[majincheng](https://clawhub.ai/user/majincheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to answer cryptocurrency market-analysis questions by retrieving ValueScan API data about token flows, whale activity, K-line history, on-chain wallet behavior, social sentiment, and AI-curated opportunity or risk signals. Outputs should be treated as informational market analysis rather than financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The SDK can forward signed ValueScan API credentials to an arbitrary URL if a caller supplies an unsafe path or URL.

Mitigation: Only call trusted ValueScan API paths, validate that the final request origin is ValueScan before sending signed headers, and avoid passing user-controlled URLs to the SDK.

Risk: The skill sends token, wallet-address, and market-analysis queries to the ValueScan service.

Mitigation: Use the skill only when the user trusts ValueScan with those queries and store API credentials securely outside prompts or shared logs.

Risk: Cryptocurrency opportunity, risk, flow, sentiment, and support or resistance signals may be mistaken for financial advice.

Mitigation: Present outputs as informational market analysis, disclose uncertainty, and encourage independent verification before trading or investment decisions.

## Reference(s):

- [ValueScan Homepage](https://beta.valuescan.io)
- [ValueScan Developer Portal](https://beta.valuescan.io/dev-portal/home/)
- [ValueScan API Documentation](https://beta-claw.valuescan.io/zh-CN/)
- [ClawHub Skill Page](https://clawhub.ai/majincheng/skills/mjc-test-destory)
- [SDK README](artifact/script/sdk/README.md)
- [API Reference Definitions](artifact/references/)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown responses with summarized JSON API data, configuration snippets, and JavaScript usage examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ValueScan API credentials and HMAC-SHA256 request signing; some API numeric fields may be returned as strings.]

## Skill Version(s):

1.0.7 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
