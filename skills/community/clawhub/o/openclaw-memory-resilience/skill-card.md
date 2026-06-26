## Description: <br>
Configure OpenClaw agent memory to survive compaction and session restarts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ferosin](https://clawhub.ai/user/Ferosin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure memory durability, compaction safeguards, context visibility, and file-based memory archives for agent workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic memory flush can persist sensitive or unintended session details into files that future agents reload or index. <br>
Mitigation: Review before applying the configuration, disclose where memory is stored and how it can be deleted, and enable automatic flushing only when users understand which agents it affects. <br>
Risk: Durable memory files such as MEMORY.md, TOOLS.md, and daily logs may be misused to store secrets or credentials. <br>
Mitigation: Do not store API keys, passwords, tokens, cookies, or other secrets in memory files; use a secret manager or scoped environment configuration instead. <br>
Risk: Global compaction defaults can change memory and pruning behavior across all agents in an OpenClaw installation. <br>
Mitigation: Review the configuration in a controlled workspace before broader use and adjust thresholds for the relevant context window and tool usage. <br>


## Reference(s): <br>
- [Compaction Config - Field Reference](references/config-explained.md) <br>
- [Context Footer - Why It Matters](references/context-footer.md) <br>
- [File Architecture for Memory Durability](references/file-architecture.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Covers OpenClaw gateway configuration, memory file architecture, context footer thresholds, and diagnostic commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
