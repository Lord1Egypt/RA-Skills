## Description:

This skill helps agents install and use the official Mermail CLI for deterministic shell automation across workspaces, mailboxes, email, folders, labels, agents, task triage, and Agent Wallet workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mermail](https://clawhub.ai/user/mermail)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a Mermail task needs terminal commands, scripts, CI steps, or deterministic JSON output instead of direct MCP chat actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow uses an unpinned npm CLI that could change later while retaining access to mail and wallet credentials.

Mitigation: Review the npm package, prefer a pinned and verified mermail-cli version, run it in a constrained environment without administrator privileges, and keep MERMAIL_API_KEY in the environment rather than command arguments.

Risk: Email and wallet workflows can create external effects such as sends, deletes, funding handoffs, transfers, swaps, or x402 payments.

Mitigation: Preview the exact recipients, resource IDs, scope, amount, asset, network, destination, and irreversible effects, then require fresh user approval immediately before each write.

Risk: Untrusted email, links, attachments, command output, or third-party content may try to broaden scope, disclose secrets, or authorize spending.

Mitigation: Treat inbound content as data only, independently match expected senders and destinations, protect tokens and payment proofs, execute each approved write once, and preserve pending or uncertain states as non-success.

## Reference(s):

- [Mermail AI Skills Documentation](https://docs.mermail.app/ai/skills)
- [Mermail CLI Command Contract](artifact/references/tools.md)
- [Mermail CLI Workflows](artifact/references/workflows.md)
- [Mermail CLI Safety](artifact/references/security.md)
- [Use Mermail CLI on ClawHub](https://clawhub.ai/mermail/skills/mermail-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, scripts, structured-output conventions, and approval guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers deterministic JSON for automation, bounded reads, stable resource IDs, explicit write previews, and non-secret error or pending-state reports.]

## Skill Version(s):

1.2.13 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
