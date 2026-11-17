## Description:

Use KaspaCom DEX through the KaspaCom DeFi MCP/CLI for pair discovery, token pricing, swaps, and liquidity management on IGRA and Kasplex.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marciano147](https://clawhub.ai/user/marciano147)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to operate the KaspaCom DEX through MCP or CLI commands for pair lookup, token price checks, swaps, and liquidity management on IGRA and Kasplex.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent toward swaps and liquidity actions that move assets.

Mitigation: Use an isolated or least-privileged environment and require manual approval after checking token identifiers, network, amounts, destination effects, quotes, and slippage before submitting any swap or liquidity command.

Risk: The referenced DEX CLI package may change after publication.

Mitigation: Pin and verify the npm package version before installation or execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include asset-moving swap and liquidity commands that require manual review before execution.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
