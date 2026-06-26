## Description: <br>
Manage Outlook and Microsoft 365 email with AI agents: triage inboxes by sender trust, draft replies with tone matching, organize folders, create inbox rules, and monitor for priority messages through Microsoft Graph-compatible clients. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and developers use this skill to help agents summarize, triage, draft, organize, and monitor Microsoft 365 email while preserving a draft-first review posture for write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Microsoft Graph write and send scopes can allow outbound mail or mailbox changes if granted to an untrusted runtime. <br>
Mitigation: Start with Mail.Read and offline_access when possible, grant Mail.Send or MailboxSettings.ReadWrite only for workflows that need them, and require draft review before sending. <br>
Risk: Inbox rule write access can create forwarding or redirect rules that persist after the agent session. <br>
Mitigation: Use a runtime that blocks dangerous inbox rule actions, or avoid granting MailboxSettings.ReadWrite unless rule creation is required. <br>
Risk: Autonomous write actions increase impact when combined with Mail.Send or MailboxSettings.ReadWrite. <br>
Mitigation: Avoid autonomous write actions unless the runtime enforces recipient allowlists, draft-first review, and rule-action blocks. <br>
Risk: Calendar references in the artifact could be mistaken for calendar automation permission. <br>
Mitigation: Do not create calendar events without separate calendar consent and timezone confirmation. <br>


## Reference(s): <br>
- [Outlook Graph Patterns](references/outlook-graph-patterns.md) <br>
- [email-agent-mcp reference runtime](https://github.com/UseJunior/email-agent-mcp) <br>
- [Reference runtime inbox rule guardrails](https://github.com/UseJunior/email-agent-mcp/blob/main/packages/email-core/src/actions/rules.ts#L39) <br>
- [Reference runtime deletion guardrail](https://github.com/UseJunior/email-agent-mcp/blob/main/packages/email-core/src/actions/label.ts) <br>
- [Reference runtime Microsoft Graph scopes](https://github.com/UseJunior/email-agent-mcp/blob/main/packages/provider-microsoft/src/auth.ts#L14) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with Microsoft Graph workflow patterns, OAuth scope notes, and draft or summary content for the user to review.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to create email drafts, move messages, organize folders, configure inbox rules, or summarize mailbox state through a trusted runtime.] <br>

## Skill Version(s): <br>
0.1.7 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
