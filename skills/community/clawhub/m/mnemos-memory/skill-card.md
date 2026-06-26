## Description: <br>
Use when users or OpenClaw/ClawHub agents need to install, configure, self-bootstrap, troubleshoot, or operate Mnemos for persistent scoped agent memory, or when they mention Mnemos, agent memory, scoped memory, memory MCP tools, or memory automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anthony-maio](https://clawhub.ai/user/anthony-maio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install, configure, and troubleshoot Mnemos persistent scoped memory for Claude Code, Codex, Cursor, OpenClaw, ClawHub, and generic MCP hosts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can retain prompts, project facts, and other sensitive context across sessions. <br>
Mitigation: Use separate Mnemos config paths or scopes for projects that should not share memory, and avoid storing secrets or sensitive prompts unless later retrieval and embedding-provider processing are acceptable. <br>
Risk: Automatic capture behavior differs by host, so users may overestimate what is stored or recalled outside Claude Code. <br>
Mitigation: Confirm host-specific automation before relying on capture, and use mnemos_retrieve, mnemos_store, and mnemos_consolidate explicitly where hooks are not available. <br>


## Reference(s): <br>
- [Host Setup](artifact/references/hosts.md) <br>
- [Operations](artifact/references/operations.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/anthony-maio/mnemos-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
0.6.0 (source: server evidence release version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
