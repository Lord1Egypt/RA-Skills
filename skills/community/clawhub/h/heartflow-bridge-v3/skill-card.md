## Description: <br>
HeartFlow is a cognitive engine for AI agents that adds self-reflection, dream-based experience synthesis, emergent personality, multi-layer memory, self-healing RL, and psychology/philosophy analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yun520-1](https://clawhub.ai/user/yun520-1) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to integrate a local AI cognition and memory framework that can analyze inputs, retrieve memory, synthesize experiences, expose MCP/CLI tools, and guide agent self-reflection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad local execution and tool surfaces may run actions beyond the reader's intended use. <br>
Mitigation: Review enabled CLI, daemon, MCP, and code-execution routes before installation, and disable routes that are not required. <br>
Risk: Persistent memory and behavior tracking can retain sensitive local context. <br>
Mitigation: Inspect storage locations regularly, delete memory/state files when no longer needed, and avoid using the skill with sensitive data unless retention is acceptable. <br>
Risk: Unauthenticated local service capabilities can expose functionality to local clients. <br>
Mitigation: Restrict MCP HTTP and daemon access to trusted local users and networks, and avoid running persistent services unless required. <br>
Risk: Memory injection can affect prompts and downstream agent behavior. <br>
Mitigation: Treat injected memory as prompt-affecting context and review retrieved or injected memories before relying on agent outputs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yun520-1/heartflow-bridge-v3) <br>
- [README](artifact/README.md) <br>
- [Agent Integration Guide](artifact/AGENTS.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples; runtime use can produce CLI, MCP, memory, and local state outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local memory/state files and expose local CLI or MCP service responses when installed.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence; artifact frontmatter 2.14.0 and package.json 2.14.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
