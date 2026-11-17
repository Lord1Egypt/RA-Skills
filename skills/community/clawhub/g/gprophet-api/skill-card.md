## Description:

AI-powered stock prediction and market analysis for global markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[filwu8](https://clawhub.ai/user/filwu8)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to connect agents to G-Prophet for stock and crypto predictions, market data, technical indicators, sentiment data, balance checks, and asynchronous analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a G-Prophet API key and sends market queries and analysis requests to an external service.

Mitigation: Use environment variables, limited-scope keys with quotas, and rotate or revoke keys if exposed.

Risk: The MCP setup can execute an unpinned gprophet package through uvx.

Mitigation: Pin and review the gprophet package version before installation or deployment.

Risk: Async analysis supports callback_url webhooks that may send results to an external endpoint.

Mitigation: Use callback_url only with HTTPS endpoints you control and expect to receive the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/filwu8/skills/gprophet-api)
- [G-Prophet homepage](https://www.gprophet.com)
- [G-Prophet API keys](https://www.gprophet.com/settings/api-keys)
- [G-Prophet dashboard](https://www.gprophet.com/dashboard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, JSON]

**Output Format:** [Markdown guidance with JSON schemas, curl examples, Python snippets, and MCP configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GPROPHET_API_KEY; API responses are JSON and some analysis workflows are asynchronous.]

## Skill Version(s):

1.0.6 (source: evidence release, artifact/_meta.json, CHANGELOG, released 2026-03-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
