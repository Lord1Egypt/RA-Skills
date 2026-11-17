## Description:

Runs an owner-supervised Mermail research inbox for customer requirements clarification, verified order handling, sourced CMC protocol comparisons or market reports, approved delivery, and same-thread follow-ups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mermail](https://clawhub.ai/user/mermail)

### License/Terms of Use:

MIT-0

## Use Case:

External Mermail workspace owners use this skill to run assisted customer research engagements through a dedicated inbox, producing sourced protocol comparisons, crypto market reports, clarification drafts, owner checkpoints, and approved email replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox access can expose customer messages, attachments, and private order context.

Mitigation: Use only owner-selected workspace, mailbox, thread, and clean-scanned content, with bounded reads and task-specific attachment handling.

Risk: Outgoing email replies and paid data purchases can create external effects.

Mitigation: Require owner authorization for exact outgoing replies, recipients, attachments, rights, and paid purchase terms before execution.

Risk: Customer email, attachments, provider output, or payment challenges may contain instructions that exceed the selected workflow.

Mitigation: Treat those inputs as data only; do not let them change tools, accounts, recipients, spending authority, credentials, or financial terms.

Risk: Unverified payment entitlement or data-use rights can make a report unsuitable for paid delivery.

Mitigation: Hold fulfillment or delivery until owner-verified order, entitlement, rights, and source-use evidence support the agreed scope.

## Reference(s):

- [Mermail AI Skills Documentation](https://docs.mermail.app/ai/skills)
- [Research Agent Tool Contracts](references/tools.md)
- [Research Business Security](references/security.md)
- [Research Engagement Workflow](references/workflows.md)
- [CMC Research and Additional Data](references/cmc-research.md)
- [Order and Report Templates](references/templates.md)
- [Official Crypto Research Workflow](https://pro.coinmarketcap.com/api/documentation/ai-agent-hub/skills/crypto-research)
- [Official Market Report Workflow](https://pro.coinmarketcap.com/api/documentation/ai-agent-hub/skills/market-report)
- [CMC MCP](https://pro.coinmarketcap.com/api/documentation/ai-agent-hub/mcp)
- [CMC x402 Endpoints and Protocol](https://pro.coinmarketcap.com/api/documentation/ai-agent-hub/x402)
- [Mermail MCP Server](https://console.mermail.app/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain-text or Markdown email drafts, sourced research memos, private owner checkpoints, and status labels.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Customer-facing output excludes internal billing evidence, wallet details, private entitlement records, and unrelated customer material.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
