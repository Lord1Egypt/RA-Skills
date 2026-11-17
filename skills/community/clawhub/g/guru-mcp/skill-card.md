## Description:

Access Guru knowledge base via MCP - ask AI questions, search documents, create drafts, and update cards. Connects to all your Guru sources including Slack, Drive, Confluence, and SharePoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pvoo](https://clawhub.ai/user/pvoo)

### License/Terms of Use:


## Use Case:

Employees and teams with Guru workspaces use this skill to ask knowledge-agent questions, search Guru documents, read cards, and create or update Guru card drafts from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can access Guru content using the permissions of the supplied token.

Mitigation: Use a least-privilege Guru token and install the skill only for workflows where that Guru access is intended.

Risk: Create and update tools can make remote content changes in Guru.

Mitigation: Require explicit user requests and human review before creating drafts or updating cards.

Risk: Guru results may include internal knowledge from connected sources such as Slack, Drive, Confluence, or SharePoint.

Mitigation: Keep outputs within authorized contexts and rely on Guru permissions to limit what the token can retrieve.

## Reference(s):

- [Guru MCP Documentation](https://help.getguru.com/docs/connecting-gurus-mcp-server)
- [Guru API Reference](https://developer.getguru.com)
- [AI Agent Center](https://app.getguru.com/ai-agent-center)
- [Guru Homepage](https://www.getguru.com)
- [ClawHub Skill Page](https://clawhub.ai/pvoo/skills/guru-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Guru MCP tools that return answers, document search results, card HTML, draft metadata, and update results according to the supplied Guru token permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
