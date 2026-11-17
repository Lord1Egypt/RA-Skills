## Description:

Independent skill for Cortex Memory operations in OpenClaw, covering cross-session memory retrieval, durable event storage, graph relationship tracing, and memory maintenance workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deki18](https://clawhub.ai/user/deki18)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to install, configure, and operate OpenClaw Cortex Memory for cross-session recall, durable preference and decision storage, graph-based relationship lookup, and memory health diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to install and enable an external OpenClaw plugin.

Mitigation: Verify the plugin source or checksum before installation, and review the exact install and enable commands before running them.

Risk: The plugin uses memory-related API credentials for embeddings, LLM calls, and reranking.

Mitigation: Provide scoped credentials through environment variables, avoid hardcoding secrets in configuration files, and rotate credentials if exposed.

Risk: The memory workflow can retain, import, reflect, export, or delete cross-session conversation history.

Mitigation: Define explicit rules for what may be stored, synced, reflected into rules, exported, or deleted, and require user confirmation for deletions and conflict resolution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deki18/skills/openclaw-cortex-memory)
- [Cortex Memory Agent Manual](artifact/references/agent-manual.md)
- [Configuration Reference](artifact/references/configuration.md)
- [Cortex Memory Tool Reference](artifact/references/tools.md)
- [Cortex Memory System Prompt Template](artifact/references/system-prompt-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose OpenClaw plugin commands, configuration settings, and memory tool workflows; memory writes should be limited to durable user-approved information.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
