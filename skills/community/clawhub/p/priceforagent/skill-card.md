## Description:

Get real-time prices for crypto, stocks, and commodities through natural-language queries, direct lookups, and batch requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edibez](https://clawhub.ai/user/edibez)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to retrieve current crypto, stock, and commodity prices through natural-language queries, direct lookups, or batch asset requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Asset queries and the registration agent_id are sent to p4ai.bitharga.com, and the service returns an API key and tracks usage.

Mitigation: Avoid sending personal, confidential, or trading-strategy details in price queries unless the provider is trusted.

Risk: The skill depends on an external price API for market lookup responses.

Mitigation: Review the returned price data before acting on it and use appropriate independent checks for financial decisions.

## Reference(s):

- [Price for Agent on ClawHub](https://clawhub.ai/edibez/skills/priceforagent)
- [Price for Agent API](https://p4ai.bitharga.com)
- [Price for Agent Function Schema](https://p4ai.bitharga.com/v1/function-schema)
- [Price for Agent OpenAPI Spec](https://p4ai.bitharga.com/v1/openapi.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include API registration guidance, price-query commands, and response-shape examples.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
