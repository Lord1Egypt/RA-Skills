## Description:

Retrieve dated market research through Mass REST or MCP integrations with explicit x402 payment controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcii](https://clawhub.ai/user/0xcii)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use an authorized Mass integration to review dated market signals, macro context, capital activity, narrative shifts, and observed airdrop research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid research requests may incur unapproved charges.

Mitigation: Approve a clear maximum spend and verify the exact payment details before any paid retry.

Risk: Payment or authentication details may expose sensitive information.

Mitigation: Keep wallet signing local and do not share keys, recovery phrases, API keys, payment proofs, or private report URLs in chat or tool arguments.

Risk: Dated research may be mistaken for guaranteed or executable investment advice.

Mitigation: State the observation time, research caveats, and uncertainty; do not present results as execution instructions or guarantees.

## Reference(s):

- [Skill source (server-resolved GitHub import)](https://github.com/0xcii/mass-mcp/tree/main/skills/mass-intelligence)
- [ClawHub release](https://clawhub.ai/0xcii/skills/mass-alpha-feed)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown research summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dated findings with evidence, counter-evidence, and uncertainty; paid requests require an approved spending cap.]

## Skill Version(s):

0.1.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
