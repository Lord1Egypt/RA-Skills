## Description:

API marketplace for AI agents. Browse, buy, sell APIs, and call them - via CLI, MCP, or raw HTTP. USDC on Solana.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sosa782](https://clawhub.ai/user/sosa782)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to discover, subscribe to, call, publish, and manage APIs through the Onchor marketplace using CLI, MCP, or raw HTTP workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use an Onchor account token to spend funds, manage marketplace listings, update payout details, and withdraw USDC.

Mitigation: Use a proper secret store for the `oat_` token and require explicit owner approval before purchases, paid calls, listing deletion, payout changes, or withdrawals.

Risk: Installing or running the Onchor CLI or MCP package can introduce package supply-chain risk.

Mitigation: Pin and verify the CLI or MCP package before running it in an agent environment.

## Reference(s):

- [Onchor homepage](https://onchor.xyz)
- [Onchor API base URL](https://api.onchor.xyz)
- [ClawHub skill page](https://clawhub.ai/sosa782/skills/onchor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON, and HTTP examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce authenticated marketplace actions and payment-related API calls when the operator supplies valid Onchor credentials.]

## Skill Version(s):

2.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
