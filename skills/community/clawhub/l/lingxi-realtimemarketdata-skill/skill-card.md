## Description:

GuoTai HaiTong Lingxi Real-Time Market Data helps agents retrieve real-time market quotes for A-shares, Hong Kong stocks, U.S. stocks, ETFs, and indexes, including price, change, volume, turnover, net inflow, turnover rate, and volume ratio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gtht-tech](https://clawhub.ai/user/gtht-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and financial-data agents use this skill to answer requests for current securities quotes, stock-code lookup, single-symbol行情, and multi-symbol comparisons. The skill is intended to return objective market data and route users to the Lingxi app when neither this skill nor its documented fallback can provide data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a GuoTai HaiTong API key locally in gtht-entry.json.

Mitigation: Treat the API key like a password, avoid pasting it into chat when possible, review where the file is stored, and restrict local file permissions.

Risk: Credential-bearing market-data requests can be routed through configurable gateways.

Mitigation: Use only trusted gateway-config.json or GTHT_GATEWAY_CONFIG values and review gateway destinations before running the skill.

Risk: Market-data responses could be mistaken for investment advice.

Mitigation: Present the output as objective data only and preserve the skill's disclaimer that generated content is not investment advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gtht-tech/skills/lingxi-realtimemarketdata-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/gtht-tech)
- [GuoTai HaiTong market data gateway](https://zx.app.gtja.com:8443/mcp/marketdata)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with inline Node.js command examples and market-data values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should present returned market-data fields without fabricating securities codes or investment advice.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
