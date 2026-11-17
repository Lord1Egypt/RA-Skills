## Description:

Create, inspect, update, and delete Mermail task triagers and review recent triager runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mermail](https://clawhub.ai/user/mermail)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, inspect, troubleshoot, update, or delete Mermail mailbox task triagers while keeping inbound automation scoped, reviewable, and least-privilege.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inbound mailbox content can contain untrusted instructions or sensitive material.

Mitigation: Require clean scan status, bounded sanitized content, strict sender and volume scope, and metadata-only handling for unapproved attachments before interpretation.

Risk: A triager configuration could enable unintended sends, deletes, credential use, account changes, or other external effects.

Mitigation: Keep automation disabled during review, show exact configuration diffs, use a minimum allowlist, and require fresh human confirmation for risky effects.

Risk: Deleting a triager is destructive and an uncertain retry could remove the wrong target.

Mitigation: Bind explicit approval to the exact mailbox, triager, tool name, and arguments, use the single-use destructive-action token once, and verify final state with a read.

## Reference(s):

- [Mermail AI skills documentation](https://docs.mermail.app/ai/skills)
- [Mermail MCP server](https://console.mermail.app/mcp)
- [Triager security boundary](references/security.md)
- [Triage tool map](references/tools.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with structured configuration proposals, debugging reports, and final-state summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include mailbox and triager IDs, current-to-intended configuration diffs, approval prompts, status labels, and linked workflow handoffs.]

## Skill Version(s):

1.2.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
