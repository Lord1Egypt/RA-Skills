## Description: <br>
Access Guru knowledge base via MCP - ask AI questions, search documents, create drafts, and update cards. Connects to all your Guru sources including Slack, Drive, Confluence, and SharePoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pvoo](https://clawhub.ai/user/pvoo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Teams that use Guru can let an agent answer workplace knowledge questions, search Guru content, read cards, create drafts, and update existing cards through the Guru MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent access to broad workplace knowledge through a Guru API token. <br>
Mitigation: Install only for Guru workspaces and data approved for agent access, and use the least-privileged token available. <br>
Risk: The skill can create drafts and update Guru cards. <br>
Mitigation: Manually review any draft creation or card update before allowing it to run. <br>
Risk: Questions and retrieved content may include sensitive business information. <br>
Mitigation: Avoid secrets or regulated personal data in questions and follow the organization's data handling policy. <br>


## Reference(s): <br>
- [Guru MCP Documentation](https://help.getguru.com/docs/connecting-gurus-mcp-server) <br>
- [Guru API Reference](https://developer.getguru.com) <br>
- [AI Agent Center](https://app.getguru.com/ai-agent-center) <br>
- [Guru Homepage](https://www.getguru.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, and MCP tool call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter and a GURU_API_TOKEN environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
