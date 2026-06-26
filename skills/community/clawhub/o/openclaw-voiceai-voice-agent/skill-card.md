## Description: <br>
Create, manage, and deploy Voice.ai conversational AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gizmoGremlin](https://clawhub.ai/user/gizmoGremlin) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and teams use this skill to create, list, update, deploy, pause, and delete Voice.ai conversational agents, including agents with knowledge bases, phone deployment, and MCP server integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage a Voice.ai account and perform deploy, pause, delete, phone-number, knowledge-base, and MCP-server actions. <br>
Mitigation: Use only with a trusted publisher and manually confirm the exact agent ID and intended action before account-changing operations. <br>
Risk: The skill requires Voice.ai API credentials and may use MCP server credentials. <br>
Mitigation: Use a scoped API key if available, keep secrets out of logs and commits, and review MCP server credentials before use. <br>


## Reference(s): <br>
- [Voice.ai Developer Dashboard](https://voice.ai/app/dashboard/developers) <br>
- [Voice Agents Guide](https://voice.ai/docs/guides/voice-agents/quickstart) <br>
- [Agent API Reference](https://voice.ai/docs/api-reference/agent-management/create-agent) <br>
- [Voice.ai Status Page](https://status.voice.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON snippets, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the Voice.ai API when invoked through the bundled JavaScript CLI or SDK.] <br>

## Skill Version(s): <br>
0.1.4 (source: ClawHub release metadata; artifact files also reference 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
