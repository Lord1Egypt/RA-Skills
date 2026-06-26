## Description: <br>
Organize a cluttered Outlook inbox with folders, batch moves, and server-side inbox rules via the Microsoft Graph API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Microsoft 365 and Outlook users use this skill to reduce inbox noise by grouping recurring notifications, moving existing messages, and setting up server-side rules for future cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MailboxSettings.ReadWrite can create persistent inbox rules, including forwarding or redirect rules if the runtime does not block them. <br>
Mitigation: Install only with a trusted Microsoft Graph runtime that blocks forwardTo, forwardAsAttachmentTo, redirectTo, delete, and permanentDelete actions. <br>
Risk: Autonomous invocation with mailbox write permissions can increase the impact of unexpected rule creation. <br>
Mitigation: Prefer folder cleanup or audit-only mode when rule creation is not needed, avoid autonomous invocation, and revoke Microsoft OAuth consent if unexpected rules appear. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/stevenobiajulu/inbox-cleanup-outlook) <br>
- [Email Agent MCP Reference Runtime](https://github.com/UseJunior/email-agent-mcp) <br>
- [Reference Runtime Rule Guardrails](https://github.com/UseJunior/email-agent-mcp/blob/main/packages/email-core/src/actions/rules.ts#L39) <br>
- [NemoClaw Email Policy](https://clawhub.ai/skill/nemoclaw-email-policy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with REST API and MCP command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Microsoft Graph delegated OAuth scopes for mailbox changes; inbox rule safety depends on runtime guardrails.] <br>

## Skill Version(s): <br>
0.1.4 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
