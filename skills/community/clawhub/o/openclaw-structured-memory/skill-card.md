## Description:

Qordinate gives OpenClaw agents durable structured memory for documents, contacts, tasks, reminders, web search, and connected apps through an MCP server authenticated with a Qordinate API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[singhcoder](https://clawhub.ai/user/singhcoder)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw agent users use this skill to connect an agent to Qordinate via MCP so it can preserve and retrieve structured memory, manage tasks and reminders, interact with documents and contacts, and use connected productivity services over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Qordinate API key can allow broad and lasting access to memory, documents, contacts, tasks, reminders, and connected apps.

Mitigation: Use the narrowest available API key scope, set an expiry when possible, store the key securely, and revoke it when the integration is no longer needed.

Risk: The agent can store information permanently or change, delete, share, and automate user data through Qordinate.

Mitigation: Require explicit user confirmation before permanent storage, deletion, sharing, connected-app actions, or automation creation.

Risk: Sensitive personal data or secrets could be sent to the remote Qordinate service.

Mitigation: Avoid sending secrets or sensitive personal data unless the user has approved the disclosure and the data is necessary for the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/singhcoder/skills/openclaw-structured-memory)
- [Qordinate MCP server endpoint](https://api.qordinate.ai/mcp)
- [Qordinate application](https://app.qordinate.ai)
- [Qordinate WhatsApp channel](https://qordinate.ai/whatsapp)
- [Qordinate Telegram channel](https://qordinate.ai/telegram)
- [Qordinate Slack channel](https://qordinate.ai/slack)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, API Calls, Text]

**Output Format:** [Markdown instructions with MCP connection details and natural-language query examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QORDINATE_API_KEY and curl; uses Streamable HTTP MCP transport.]

## Skill Version(s):

2.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
