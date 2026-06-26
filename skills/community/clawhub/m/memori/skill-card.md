## Description: <br>
Agent-native memory for OpenClaw that structures memory from agent trace, execution history, decisions, tool calls, and conversations into durable long-term memory primitives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rpkruse](https://clawhub.ai/user/rpkruse) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and OpenClaw users use Memori to add opt-in, persistent long-term memory from agent execution, tool usage, workflow history, decisions, and conversations. Agents can retrieve relevant stored context through explicit recall tools while memory creation runs in the background after interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent conversations, tool traces, workflow history, and decisions may be sent to Memori and stored as long-term memory once the integration is configured. <br>
Mitigation: Enable the skill only with explicit user consent, use scoped credentials and a dedicated project ID, avoid sharing secrets while enabled, and confirm how to pause, clear, or delete stored memories. <br>
Risk: The skill requires sensitive credentials and project identifiers for remote memory storage. <br>
Mitigation: Store MEMORI_API_KEY, ENTITY_ID, and PROJECT_ID in the configured environment or OpenClaw configuration, rotate credentials when needed, and avoid exposing them in chat or logs. <br>


## Reference(s): <br>
- [Memori ClawHub Release](https://clawhub.ai/rpkruse/memori) <br>
- [Memori API Service](https://api.memorilabs.ai) <br>
- [Memori npm Package](https://www.npmjs.com/package/@memorilabs/openclaw-memori) <br>
- [Memori Documentation](https://memorilabs.ai/docs/memori-cloud/openclaw/overview/) <br>
- [Memori Repository](https://github.com/MemoriLabs/Memori) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MEMORI_API_KEY, ENTITY_ID, PROJECT_ID, the memori binary, and the external service https://api.memorilabs.ai.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
