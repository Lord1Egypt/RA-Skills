## Description: <br>
Post On Discord Channel sends messages to Discord channels through AgentPMT-hosted remote tool calls using webhooks, markdown, embeds, file attachments, and mention controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external automation teams use this skill to let an agent post Discord notifications, formatted reports, support updates, event notices, and files to channels via webhook URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Discord webhook URLs are sensitive credentials that can allow posting to a channel if exposed. <br>
Mitigation: Keep webhook URLs out of prompts and logs, and rotate the webhook if it is exposed. <br>
Risk: Messages, embeds, and attached files are sent to external Discord channels and can expose private or unintended content. <br>
Mitigation: Review each destination webhook and keep tool inputs scoped to the minimum content needed before sending. <br>
Risk: Mention controls can notify broad audiences such as everyone, roles, or individual users. <br>
Mitigation: Restrict allowed_mentions unless broad pings are intentional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/post-on-discord-channel) <br>
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/post-on-discord-channel) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, JSON, API calls] <br>
**Output Format:** [Markdown instructions with JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defines one send action with webhook_url plus optional content, embeds, files, username, avatar_url, tts, and allowed_mentions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
