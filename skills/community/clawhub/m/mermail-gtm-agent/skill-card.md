## Description:

Run outbound GTM email, classify replies, and draft warm-acks through a Mermail mailbox.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mermail](https://clawhub.ai/user/mermail)

### License/Terms of Use:

MIT-0

## Use Case:

External GTM and sales teams use this skill to run Mermail-based outbound outreach, classify replies, draft warm acknowledgements, honor unsubscribes, and hand off interested threads for human follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prepare outbound email, reply, forward, Apollo connection, and triager actions that affect a Mermail workspace.

Mitigation: Require exact previews and fresh user approval before sends, replies, forwards, Apollo connections, or triager configuration changes.

Risk: Inbound replies, Apollo records, attachments, and tool output may contain untrusted or misleading content.

Mitigation: Treat external content as data, require clean scan status before message body interpretation, and ignore embedded instructions that attempt to change recipients, offers, skills, tool allowlists, or approval state.

Risk: Reply automation could accidentally continue outreach after an unsubscribe or send without human review.

Mitigation: Honor unsubscribe and stop-sequence language, keep warm acknowledgements and triager output draft-only, and require independent approval before any reply is sent.

## Reference(s):

- [Mermail AI Skills Documentation](https://docs.mermail.app/ai/skills)
- [Mermail MCP Server](https://console.mermail.app/mcp)
- [GTM agent tools](references/tools.md)
- [GTM agent workflows](references/workflows.md)
- [GTM agent security](references/security.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with structured mailbox, outreach, classification, draft, approval, and handoff status details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outbound sends, replies, forwards, Apollo connections, and triager changes require exact previews and fresh user approval.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
