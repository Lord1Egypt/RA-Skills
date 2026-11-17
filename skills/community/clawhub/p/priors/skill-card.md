## Description:

Check an AI agent's repayment record before you pay or trust it, pay x402 APIs in USDG on Robinhood Chain within caps, borrow the shortfall from a Priors credit line, and repay before the due date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[priors-agents](https://clawhub.ai/user/priors-agents)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators of AI agents use this skill to check an agent's recorded repayment history and to configure bounded USDG payments, borrowing, and repayment through Priors. It provides instructions for interpreting records and for obtaining user approval before actions that sign transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner identifies an unpinned `npx agent001` command as a potential supply-chain risk, and the available scan was partial.

Mitigation: Do not run `npx agent001`; verify the package source and version before installing. The skill documents a pinned `@priors/mcp@0.19.1` install for the MCP server.

Risk: Payment, borrowing, repayment, and related signing tools can move real funds on Robinhood Chain mainnet.

Mitigation: State the amount and obtain user approval before each signing action; use a dedicated wallet and the documented per-call, total-spend, and borrowing caps.

## Reference(s):

- [Priors](https://priors.trade)
- [Priors ClawHub skill page](https://clawhub.ai/priors-agents/skills/priors)
- [Priors Check API documentation](https://github.com/priors-agents/priors/blob/main/docs/CHECK-API.md)
- [Priors security findings and fixes](https://github.com/priors-agents/priors/blob/main/docs/SECURITY-v2.md)
- [agent001 repository](https://github.com/priors-agents/agent001)
- [Priors invitation page](https://priors.trade/invite)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks and JSON/API response interpretation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes repayment-record interpretation, spending limits, and transaction-approval guidance.]

## Skill Version(s):

0.2.18 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
