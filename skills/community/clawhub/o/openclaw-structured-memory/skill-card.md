## Description: <br>
Qordinate gives an OpenClaw agent durable structured memory for documents, contacts, tasks, reminders, web search, and connected apps through an MCP connection authenticated with an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SinghCoder](https://clawhub.ai/user/SinghCoder) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to connect an agent to Qordinate over MCP so it can store, retrieve, and update durable user context such as documents, contacts, tasks, reminders, forms, automations, web-search results, and connected-app data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad ongoing access to private documents, contacts, tasks, reminders, connected apps, and stored Qordinate data. <br>
Mitigation: Use a dedicated or expiring QORDINATE_API_KEY, connect only necessary apps, and periodically review stored data and active automations. <br>
Risk: The agent may make persistent changes such as deletes, sharing actions, reminders, automations, or connected-app actions. <br>
Mitigation: Require explicit user confirmation before any destructive, sharing, reminder, automation, or connected-app action. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/SinghCoder/openclaw-structured-memory) <br>
- [Qordinate MCP Server](https://api.qordinate.ai/mcp) <br>
- [Qordinate App](https://app.qordinate.ai) <br>
- [Qordinate WhatsApp Channel](https://qordinate.ai/whatsapp) <br>
- [Qordinate Telegram Channel](https://qordinate.ai/telegram) <br>
- [Qordinate Slack Channel](https://qordinate.ai/slack) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown with setup instructions, connection details, and natural-language MCP query examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MCP client support, curl, and QORDINATE_API_KEY.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata; artifact frontmatter reports 0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
