## Description: <br>
Guides agents through installing, configuring, and using memory-lancedb-pro, a long-term memory MCP plugin for OpenClaw agents with Smart Extraction, hybrid retrieval, lifecycle management, scope isolation, and memory tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaoyang78](https://clawhub.ai/user/chaoyang78) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install, configure, verify, and operate memory-lancedb-pro for persistent agent memory, including provider selection, API-key checks, local Ollama setup, and smoke testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask users to provide raw API keys while configuring paid embedding, reranking, or LLM providers. <br>
Mitigation: Configure credentials through environment variables or a local secret manager, and avoid pasting API keys into chat. <br>
Risk: The skill recommends quick-install or downloaded validation scripts that can execute remote code. <br>
Mitigation: Inspect downloaded scripts and pin versions before execution. <br>
Risk: The skill can modify persistent OpenClaw configuration and affect gateway behavior. <br>
Mitigation: Back up openclaw.json, review proposed edits before applying them, and confirm any gateway restart. <br>
Risk: Automatic capture or recall can store or expose data through the memory plugin. <br>
Mitigation: Enable autoCapture or autoRecall only after deciding what data may be stored and how it will be deleted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chaoyang78/memory-lancedb-pro-skill-main) <br>
- [memory-lancedb-pro full technical reference](references/full-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include provider-specific API-key checks, OpenClaw configuration edits, validation steps, and smoke-test instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
