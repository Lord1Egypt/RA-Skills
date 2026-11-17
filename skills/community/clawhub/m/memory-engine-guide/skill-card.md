## Description:

Clawhub Memory Engine gives an OpenClaw agent persistent MemGPT-style memory with passive conversation capture, hybrid semantic search, knowledge graph recall, episodic summaries, reflection, and memory administration tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ytangguo](https://clawhub.ai/user/ytangguo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add persistent memory, search, recall, reflection, import/export, and dashboard workflows to OpenClaw agents. It is intended for agents that should retain and retrieve information across conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically stores conversation history for later search and recall.

Mitigation: Enable it only when persistent memory is intended, and confirm where memories are stored, how they are exported, and how they are deleted.

Risk: Setup may create persistent maintenance jobs and agent-instruction changes without enough rollback detail.

Mitigation: Inspect the setup script before running it, record any cron jobs or instruction patches it creates, and confirm the full uninstall or rollback procedure.

Risk: The installation depends on an external package and setup script.

Mitigation: Pin or verify the package version and review the installed setup script before enabling the plugin.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ytangguo/skills/memory-engine-guide)
- [npm package linked by skill artifact](https://www.npmjs.com/package/@icex-labs/openclaw-memory-engine)
- [GitHub repository linked by skill artifact](https://github.com/icex-labs/openclaw-memory-engine)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, architecture notes, and tool names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation, memory architecture, search behavior, multi-agent isolation, self-healing behavior, and administrative tool guidance.]

## Skill Version(s):

5.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
