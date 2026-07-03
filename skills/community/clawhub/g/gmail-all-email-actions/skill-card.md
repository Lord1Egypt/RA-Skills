## Description: <br>
Gmail All Email Actions helps agents send, read, search, reply to, forward, label, draft, trash, and restore Gmail messages through AgentPMT-hosted tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to automate Gmail workflows such as inbox triage, customer follow-up, message search, draft review, forwarding, labeling, and sending messages with attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad Gmail mailbox and outbound email authority, including reading, sending, forwarding, labeling, trashing, deleting drafts, and attachment handling. <br>
Mitigation: Use it only in workflows that require explicit review of recipients, message bodies, forwarded content, attachments, labels, and trash or delete actions before execution. <br>
Risk: The security summary reports weak scoping and no clear confirmation rules for sensitive Gmail actions. <br>
Mitigation: Restrict enabled workflows to the minimum needed Gmail actions and require confirmation before sending, forwarding, or destructive mailbox changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/gmail-all-email-actions) <br>
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/gmail-all-email-actions) <br>
- [Gmail All Email Actions Schema](artifact/schema.md) <br>
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, JSON] <br>
**Output Format:** [Markdown instructions with JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes action names, required and optional parameters, response handling guidance, and schema lookup routes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
