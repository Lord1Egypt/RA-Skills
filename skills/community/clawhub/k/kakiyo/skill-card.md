## Description: <br>
Official Kakiyo skill from Kakiyo.com for managing LinkedIn automation campaigns, prospects, and AI agents via Kakiyo MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CyberBoyAyush](https://clawhub.ai/user/CyberBoyAyush) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to configure Kakiyo MCP access and manage LinkedIn outreach campaigns, prospects, AI agents, analytics, workspaces, webhooks, and do-not-contact lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent operate Kakiyo outreach workflows and account settings broadly. <br>
Mitigation: Install only for trusted Kakiyo usage, use a dedicated revocable API key when possible, and review campaign, prospect, workspace, DNC, and webhook changes before execution. <br>
Risk: Resume, delete, remove, and webhook URL actions can change outreach state or account integrations. <br>
Mitigation: Require explicit user confirmation before these actions and verify target IDs, URLs, and affected workspaces or prospects. <br>


## Reference(s): <br>
- [Kakiyo Website](https://kakiyo.com) <br>
- [Kakiyo Documentation](https://docs.kakiyo.com) <br>
- [Kakiyo Dashboard](https://app.kakiyo.com) <br>
- [Kakiyo MCP Server](https://docs.kakiyo.com/mcp-server) <br>
- [Kakiyo API Reference](https://docs.kakiyo.com/api-reference) <br>
- [ClawHub Skill Page](https://clawhub.ai/CyberBoyAyush/kakiyo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented MCP call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter and a KAKIYO_API_KEY for live Kakiyo MCP calls.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
