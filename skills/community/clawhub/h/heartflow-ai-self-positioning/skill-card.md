## Description: <br>
HeartFlow is a cognitive engine for AI agents that provides self-reflection, dream-based experience synthesis, emergent personality, memory, psychology, philosophy, and self-positioning analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yun520-1](https://clawhub.ai/user/yun520-1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add local cognitive-engine behavior to an AI agent, including reflective state analysis, memory retrieval, dream-style synthesis, self-healing strategy selection, and self-positioning summaries through CLI or MCP interfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store conversation-derived data in local memory files. <br>
Mitigation: Avoid storing secrets or sensitive personal data, and review memory contents and retention behavior before enabling persistent use. <br>
Risk: The skill exposes local daemon and MCP interfaces, including an HTTP SSE service. <br>
Mitigation: Run only in a trusted local environment, review daemon and MCP startup settings, and set SHUTDOWN_TOKEN when using the daemon. <br>
Risk: The security summary flags broad code or command execution surfaces through codeExecutor and selfInitiator routes. <br>
Mitigation: Review or disable those routes before deployment and require explicit approval for any generated code, shell command, or file-writing workflow. <br>
Risk: The release is marked with sensitive capability tags including requires-wallet and requires-sensitive-credentials. <br>
Mitigation: Do not provide wallet data, keys, tokens, or credentials unless the exact operation has been reviewed and isolated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yun520-1/heartflow-ai-self-positioning) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and command-oriented guidance with JavaScript examples and MCP/CLI usage details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or retrieve local memory data when enabled and may expose local daemon or MCP service interfaces.] <br>

## Skill Version(s): <br>
2.14.0 (source: server release metadata, SKILL.md frontmatter, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
