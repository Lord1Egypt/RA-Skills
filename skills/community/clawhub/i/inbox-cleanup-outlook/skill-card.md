## Description:

Organizes cluttered Outlook inboxes with folders, batch message moves, and server-side inbox rules through Microsoft Graph.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to reduce inbox noise by grouping automated notifications, creating practical folders, moving existing Outlook messages, and setting future inbox rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MailboxSettings.ReadWrite can allow persistent inbox rules that forward or redirect future mail.

Mitigation: Install only with a trusted runtime that blocks forward, redirect, delete, and permanent-delete rule actions; prefer audit-only or folder-only scopes when rule creation is not needed.

Risk: Autonomous invocation with write scopes can create or modify mailbox state without per-call approval.

Mitigation: Avoid autonomous invocation unless runtime-level controls enforce the blocked action list and user approval expectations.

Risk: The skill is instruction-only and cannot enforce its own security model.

Mitigation: Validate the runtime's Microsoft Graph action handlers and revoke OAuth consent if behavior is unexpected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stevenobiajulu/skills/inbox-cleanup-outlook)
- [email-agent-mcp homepage](https://github.com/UseJunior/email-agent-mcp)
- [Reference runtime rule guardrail](https://github.com/UseJunior/email-agent-mcp/blob/main/packages/email-core/src/actions/rules.ts#L39)
- [NemoClaw Email Policy skill](https://clawhub.ai/skill/nemoclaw-email-policy)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with Microsoft Graph examples and MCP command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only guidance; execution depends on a trusted runtime with Microsoft Graph OAuth permissions.]

## Skill Version(s):

0.1.4 (source: server evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
