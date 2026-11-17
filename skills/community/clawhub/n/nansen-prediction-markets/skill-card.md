## Description:

Polymarket screeners — discover trending events, top markets by volume, and search for specific markets. Use when browsing what's happening on prediction markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market analysts use this skill to browse Polymarket events and markets, find markets by query or status, and compare activity by volume, liquidity, and open interest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supported HTTP 402 challenges may spend funds from the configured wallet, and repeated calls in loops can incur repeated charges.

Mitigation: Review wallet authorization, payment policy, and spending limits before running screeners; use only an explicitly selected API key or saved browser session for this workflow.

## Reference(s):

- [Nansen CLI browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and text market screener results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screener results include event and market fields such as volume, liquidity, open interest, and trader counts.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
