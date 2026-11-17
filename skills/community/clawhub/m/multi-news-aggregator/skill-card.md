## Description:

Agent skill for x402-paid global news aggregation and source/time-filtered search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parsonssss](https://clawhub.ai/user/parsonssss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to search global news through a paid x402 API, including source-domain and publication-time filters. It supports workflows that need recent news results with source and timestamp context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to use an EVM private key to authorize paid x402 requests, which can create unintended spending or key-exposure risk.

Mitigation: Use a dedicated low-balance wallet, store the key only in local secret storage, set strict spending limits, and require confirmation or local validation of payment terms before signing.

Risk: News queries are sent to the x402 API, so sensitive query text may leave the user's environment.

Mitigation: Avoid sensitive or regulated search terms unless the API use is approved, and pin requests to the documented API origin.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/parsonssss/skills/multi-news-aggregator)
- [x402 API base](https://www.x402api.app/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples and TypeScript code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent instructions for calling a paid news-search API and handling x402 payment-required responses.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
