## Description:

Locus payment tools for AI agents. Use when asked to send payments, check wallet balances, list tokens, approve token spending, or process payment-related actions from emails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cdermott7](https://clawhub.ai/user/cdermott7)

### License/Terms of Use:


## Use Case:

External users and developers use Locus to connect an agent to wallet-backed payment tools for balance checks, token listing, token approvals, and sending payments after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet-linked API keys and authorization headers may be exposed during setup through terminal logs, screenshots, command history, or process telemetry.

Mitigation: Use narrowly scoped Locus API keys with low limits and recipient controls, avoid recorded or shared terminals during setup, and rotate the key if exposure is possible.

Risk: Payment and token approval tools can transfer assets or grant spending authority if invoked with incorrect recipients, amounts, tokens, or allowances.

Mitigation: Review every payment or token approval manually, confirm recipient, token, amount, and memo before execution, and apply extra review to large payments.

Risk: Setup may install an unpinned global mcporter package before configuring the Locus MCP connection.

Mitigation: Install a reviewed and pinned mcporter version separately when package provenance or reproducibility is required.

## Reference(s):

- [ClawHub Locus skill page](https://clawhub.ai/cdermott7/skills/locus)
- [Locus website](https://paywithlocus.com)
- [Locus API key portal](https://app.paywithlocus.com)
- [Locus MCP endpoint](https://mcp.paywithlocus.com/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool availability is dynamic and depends on the user's Locus permission group.]

## Skill Version(s):

1.3.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
