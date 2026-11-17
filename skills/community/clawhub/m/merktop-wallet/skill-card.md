## Description:

Pay for any x402-gated API or resource, and get paid, from a non-custodial Merktop wallet on Base under a hard on-chain spend cap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luiso2](https://clawhub.ai/user/luiso2)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill when a task needs an x402-gated API, dataset, service, data feed, hosted paywall, or agent-to-agent resource. The skill guides the agent to pay through Merktop's hosted pay proxy and to report real-money spend from the response headers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The payment credential can be exposed if MERKTOP_BUYER_KEY is placed in URL paths or queryable logs.

Mitigation: Prefer the x-merktop-key header form, rotate any key already used in URL examples, and keep a small spend cap.

Risk: Using the unpinned npx MCP integration can execute an unexpected package version.

Mitigation: Avoid the unpinned npx integration unless a specific trusted version is pinned and verified.

Risk: Paid calls spend real money and repeated loops can consume the user's budget.

Mitigation: Use paid resources only when needed, stop on spend-cap or sanctioned-party errors, and report x-merktop-spent-cents to the user.

## Reference(s):

- [Merktop documentation](https://facilitator.merktop.com/docs)
- [Merktop website](https://merktop.com)
- [ClawHub skill page](https://clawhub.ai/luiso2/skills/merktop-wallet)
- [ClawHub publisher profile](https://clawhub.ai/user/luiso2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and HTTP outcome guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and MERKTOP_BUYER_KEY; successful paid calls return the upstream response body and expose spend in x-merktop-spent-cents.]

## Skill Version(s):

1.0.1 (source: frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
