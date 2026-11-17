## Description:

Provides Chinese A-share Dragon-Tiger List, broker detail, money-flow, stock-pool, and quote API guidance with a small Python client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fffy520](https://clawhub.ai/user/fffy520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent builders use this skill to query A-share Dragon-Tiger List records, broker seat details, stock-pool data, and money-flow data through documented HTTP endpoints or the included Python client.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included client sends stock codes and dates to a third-party API over unencrypted HTTP, so requests and returned market data could be observed or modified on the network.

Mitigation: Avoid sending API keys or sensitive credentials through the current endpoint, and do not rely on it for high-integrity trading automation unless the provider offers HTTPS or another integrity-protected channel.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fffy520/skills/lhb-api)
- [A-share Market Data API Endpoint](http://fffy520.gicp.net:8003)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with API examples, Python code, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include HTTP request examples and JSON response field descriptions for market data queries.]

## Skill Version(s):

1.0.3 (source: server release metadata, created 2026-05-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
