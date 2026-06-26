## Description: <br>
Provides agent workflows for OpenClaw Cortex Memory, including plugin setup, memory retrieval, durable event storage, relationship queries, conflict handling, and memory maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deki18](https://clawhub.ai/user/deki18) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to add long-term memory workflows to OpenClaw sessions, including recalling prior decisions, tracing entity relationships, persisting durable facts, and diagnosing memory plugin issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install or enable an external memory plugin and, if needed, use an npm fallback package. <br>
Mitigation: Install only from trusted sources, inspect the plugin before enabling it, and require explicit approval for plugin or configuration changes. <br>
Risk: The memory workflow can persist durable facts and import historical conversations as long-lived records. <br>
Mitigation: Confirm what history may be imported, enable auto-sync or reflection only after consent, and verify how stored memories can be reviewed or deleted. <br>
Risk: The configuration requires API keys and trusted endpoints for embedding, LLM, and reranker services. <br>
Mitigation: Use scoped credentials through environment variables and route requests only to trusted endpoints. <br>
Risk: Graph relationship conflicts or stale memory records can affect answers about prior decisions or preferences. <br>
Mitigation: Retrieve evidence before answering, surface conflicts to the user, and resolve graph conflicts only after confirmation. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/deki18/openclaw-cortex-memory) <br>
- [Cortex Memory Agent Manual](references/agent-manual.md) <br>
- [Configuration Reference](references/configuration.md) <br>
- [Cortex Memory Tool Reference](references/tools.md) <br>
- [System Prompt Template](references/system-prompt-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to call Cortex Memory tools for retrieval, persistence, graph conflict handling, diagnostics, synchronization, and reflection when the plugin is available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
