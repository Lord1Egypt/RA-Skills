## Description: <br>
HeartFlow is a cognitive engine for AI agents that supports self-reflection, dream synthesis, emergent personality, AI psychology, AI philosophy, memory, reasoning, and self-healing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yun520-1](https://clawhub.ai/user/yun520-1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add cognitive reflection, memory retrieval, dream-style experience synthesis, reasoning checks, and MCP or CLI-based HeartFlow operations to an AI agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run as a high-privilege local tool with broad access to local files and memory stores. <br>
Mitigation: Install and run it in a sandbox or low-privilege account, and review local file access before enabling persistent memory features. <br>
Risk: The MCP HTTP server and daemon interfaces can create local service exposure if reachable by browsers or untrusted pages. <br>
Mitigation: Keep the service bound to trusted local use, avoid exposing it to untrusted clients, and require the documented shutdown token for daemon control. <br>
Risk: Code execution, self-initiation, and code-writing behavior can be unsafe when driven by untrusted input. <br>
Mitigation: Do not route untrusted input to codeExecutor, selfInitiator, or codeWriter paths without manual review and execution limits. <br>
Risk: Stored memory can influence prompts or be exported, which can leak or reintroduce sensitive or malicious content. <br>
Mitigation: Inspect, prune, or limit stored memory before enabling memory injection or export workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yun520-1/heartflow-core-v2) <br>
- [README](README.md) <br>
- [Agent integration guide](AGENTS.md) <br>
- [CHANGELOG](CHANGELOG.md) <br>
- [Skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text responses, JSON-like MCP payloads, and command-line output depending on interface.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or write local memory files and may expose local CLI, daemon, and MCP HTTP server workflows when enabled.] <br>

## Skill Version(s): <br>
2.14.3 (source: server release evidence; artifact frontmatter and changelog report 2.14.0, package.json reports 2.14.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
