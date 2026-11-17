## Description:

Query Pinax API datasets, including Token API for EVM/SVM/TVM token data, prediction markets, and perp exchange data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pinax](https://clawhub.ai/user/pinax)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to choose Pinax API endpoints, build authenticated API requests, handle pagination, and discover supported blockchain, prediction-market, and perp-exchange datasets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet and per-user trading endpoints can expose privacy-sensitive activity if queried or correlated unnecessarily.

Mitigation: Use these endpoints only for legitimate user-requested purposes, minimize retention, and avoid unnecessary correlation of wallet or trading data.

Risk: Bearer tokens and API keys can authorize Pinax, The Graph Market, or paid API access.

Mitigation: Protect credentials with secret storage, avoid logging tokens, and send credentials only to the intended Pinax API service.

## Reference(s):

- [Pinax API base URL](https://api.pinax.network)
- [Pinax API docs](https://app.pinax.network/docs)
- [Pinax API FAQ](https://app.pinax.network/help)
- [The Graph Market](https://thegraph.market)
- [ClawHub skill page](https://clawhub.ai/pinax/skills/pinax-api)
- [Pinax publisher profile](https://clawhub.ai/user/pinax)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with endpoint tables, JSON examples, and request snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance focuses on API endpoint selection, authentication headers, pagination, filters, and request construction.]

## Skill Version(s):

3.21.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
