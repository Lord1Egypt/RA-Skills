## Description:

Create, manage, and deploy Voice.ai conversational AI agents for listing, creating, and configuring voice agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gizmogremlin](https://clawhub.ai/user/gizmogremlin)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to create, inspect, update, deploy, pause, and delete Voice.ai conversational agents, including agents with knowledge-base and MCP integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change or delete live Voice.ai resources.

Mitigation: Require explicit confirmation before deploy, delete, knowledge-base deletion, or phone-number changes.

Risk: API-key handling can expose credentials if keys are echoed or committed.

Mitigation: Use a narrowly scoped Voice.ai API key, avoid echoing keys, and do not commit .env files.

Risk: A custom API endpoint can redirect credentials or resource operations if it is not trusted.

Mitigation: Prefer the default HTTPS endpoint unless the custom endpoint has been separately verified.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gizmogremlin/skills/openclaw-voiceai-voice-agent)
- [Voice.ai Developer Dashboard](https://voice.ai/app/dashboard/developers)
- [Voice.ai Voice Agents Guide](https://voice.ai/docs/guides/voice-agents/quickstart)
- [Voice.ai Agent API Reference](https://voice.ai/docs/api-reference/agent-management/create-agent)
- [Voice.ai Status Page](https://status.voice.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, JSON snippets, and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform Voice.ai API operations when credentials are provided.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
