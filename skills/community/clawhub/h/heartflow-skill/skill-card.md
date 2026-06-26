## Description: <br>
HeartFlow is a cognitive engine for AI agents that supports self-reflection, dream-based experience synthesis, emergent personality, memory retrieval, verification, and self-healing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yun520-1](https://clawhub.ai/user/yun520-1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add local cognitive memory, reflection, dream synthesis, MCP/CLI access, and verification-oriented reasoning workflows to an AI agent. It is suitable when the operator wants an active local memory and middleware package, not just a passive reflection prompt. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes broad code execution, local service, and persistent memory capabilities that exceed a passive reflection prompt. <br>
Mitigation: Install it only when an active local memory and middleware engine is intended, review the daemon, MCP, plugin, shell, Python, and JavaScript execution paths before use, and run it in a sandboxed workspace when isolation is required. <br>
Risk: Daemon and MCP paths can expose long-running local service behavior. <br>
Mitigation: Disable daemon and MCP paths unless needed, set SHUTDOWN_TOKEN when using the daemon, and restrict runtime access to the intended local user and workspace. <br>
Risk: Persistent memory files may affect future agent behavior or retain sensitive project context. <br>
Mitigation: Use a dedicated workspace, inspect memory and data directories before deployment, and clear or scope stored memory when handling sensitive projects. <br>
Risk: Optional external embedding or fact-checking integrations can send data outside the local environment if enabled. <br>
Mitigation: Keep external provider features disabled unless the operator trusts the provider and has approved the data flow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yun520-1/heartflow-skill) <br>
- [SKILL.md](SKILL.md) <br>
- [README.md](README.md) <br>
- [Agent Integration Guide](AGENTS.md) <br>
- [CHANGELOG.md](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, JavaScript API calls, shell commands, MCP tool responses, and local memory records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or read local memory, Q-table, graph, and runtime data files when the corresponding engine, daemon, MCP, or memory-tool paths are used.] <br>

## Skill Version(s): <br>
2.10.1 (source: server release metadata, SKILL.md frontmatter, package.json, CHANGELOG.md, README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
