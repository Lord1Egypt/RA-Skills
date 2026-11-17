## Description:

Manages Mermail mailbox-agent conversations and delegates explicit mailbox tasks to the Mermail mailbox Assistant from external MCP clients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mermail](https://clawhub.ai/user/mermail)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and mailbox operators use this skill to create, inspect, continue, rename, or delete Mermail mailbox-agent conversations and to delegate one clearly bounded mailbox task to Mermail's mailbox Assistant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegated mailbox-agent chats may retain broad email, connected-app, and wallet-related capabilities without server-enforced narrowing.

Mitigation: Install only when that delegated access is acceptable; use direct read-only Mermail tools instead when technical isolation is required.

Risk: Mailbox content, prior assistant text, attachments, and provider output can contain untrusted instructions or secret-adjacent data.

Mitigation: Treat that content as data, pass only task-relevant non-secret context, and require exact current-user authorization for sends, scheduling, deletion, account changes, credential use, or financial effects.

Risk: Narrative assistant responses or interrupted streams may not prove that a mailbox or connected-service action completed.

Mitigation: Report completion only from responsible structured tool evidence or independently verified state, and do not retry uncertain writes automatically.

## Reference(s):

- [Mermail AI Skills Documentation](https://docs.mermail.app/ai/skills)
- [Mermail MCP Server](https://console.mermail.app/mcp)
- [Mermail mail-agent safety](references/security.md)
- [Mermail mail-agent tool contract](references/tools.md)
- [Mermail mail-agent workflows](references/workflows.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or concise structured text with mailbox identifiers, delegation boundaries, and result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include mailbox ids, conversation ids, thread ids, pagination state, effect status, and blocker reasons.]

## Skill Version(s):

1.2.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
