## Description:

Manage Outlook and Microsoft 365 email with AI agents for inbox triage, tone-matched draft replies, folder organization, inbox rules, and priority-message monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams with Microsoft 365 accounts use this skill to triage inboxes, draft reviewed replies, organize folders and rules, and monitor priority messages through a Graph-capable agent or runtime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill involves high-impact Microsoft Graph permissions, including Mail.Send and MailboxSettings.ReadWrite, which can enable outbound email or persistent mailbox changes if misused.

Mitigation: Install with least-privilege consent: start with Mail.Read, avoid Mail.Send and MailboxSettings.ReadWrite unless the runtime enforces draft-first sending, recipient allowlists, and safe rule actions.

Risk: Inbox rules can continue acting after an agent session and can silently forward, redirect, or delete mail if unsafe actions are allowed.

Mitigation: Use a runtime that blocks forward, redirect, delete, and permanent-delete rule actions; prefer safe move, copy, mark-read, and stop-processing rules.

Risk: Calendar scheduling is described as out of scope for the skill's core email scope set.

Mitigation: Use a separate calendar tool only when deliberately enabled, and confirm timezone and event details before creating calendar events.

Risk: The skill is instruction-only and cannot enforce its own safety model by itself.

Mitigation: Deploy it with a trusted Graph runtime or policy layer that enforces draft review, explicit send approval, secure token storage, and dangerous-action blocking.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/stevenobiajulu/skills/outlook-email-management)
- [email-agent-mcp homepage](https://github.com/UseJunior/email-agent-mcp)
- [Outlook Graph API Patterns](references/outlook-graph-patterns.md)
- [email-agent-mcp rule action guards](https://github.com/UseJunior/email-agent-mcp/blob/main/packages/email-core/src/actions/rules.ts#L39)
- [email-agent-mcp delete guard](https://github.com/UseJunior/email-agent-mcp/blob/main/packages/email-core/src/actions/label.ts)
- [email-agent-mcp Microsoft auth scopes](https://github.com/UseJunior/email-agent-mcp/blob/main/packages/provider-microsoft/src/auth.ts#L14)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with Microsoft Graph API examples and OAuth scope configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-first email workflow; read and write actions depend on Microsoft Graph OAuth scopes and runtime guardrails.]

## Skill Version(s):

0.1.7 (source: server release evidence and artifact frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
