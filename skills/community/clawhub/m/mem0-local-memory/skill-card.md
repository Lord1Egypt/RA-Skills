## Description: <br>
mem0 Local Memory helps agents set up a local OpenClaw long-term memory plugin backed by mem0 and ChromaDB, with DeepSeek for fact extraction and DashScope for embeddings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dream-star-end](https://clawhub.ai/user/dream-star-end) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install, configure, and verify shared long-term semantic memory across agents. It provides setup guidance, shell commands, configuration examples, and optional import steps for existing OpenClaw workspace memories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent cross-agent memory can capture and reuse sensitive workspace content across OpenClaw agents. <br>
Mitigation: Install only when shared long-term memory is intended, review MEMORY.md and TOOLS.md before import, consider disabling autoCapture until tested, and confirm how to stop the service and delete stored memories. <br>
Risk: Changing MEM0_URL away from localhost can send memory operations to a remote server. <br>
Mitigation: Keep MEM0_URL on localhost unless the remote endpoint is explicitly trusted. <br>
Risk: The setup depends on external DeepSeek and DashScope services for fact extraction and embeddings. <br>
Mitigation: Use dedicated API keys and review which text snippets may be sent to those providers before enabling the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dream-star-end/mem0-local-memory) <br>
- [DeepSeek Platform](https://platform.deepseek.com/) <br>
- [DashScope](https://dashscope.aliyuncs.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and service configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local service verification commands and optional memory import guidance.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
