## Description:

Automatically monitors and optimizes conversation context by summarizing key points, preserving facts, and splitting large tasks to reduce prompt overflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blackworm](https://clawhub.ai/user/blackworm)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to keep long-running conversations within context limits, preserve important facts in memory, and split oversized tasks into smaller subtasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic cleanup and context rewriting can remove or alter active conversation context.

Mitigation: Review configuration before installation and disable automatic cleanup or scheduled optimization until behavior is verified in a test workspace.

Risk: Memory updates can persist extracted facts to MEMORY.md, including facts produced from sample or unintended inputs.

Mitigation: Disable MEMORY.md updates or manually review generated memory entries before relying on them.

Risk: Manual optimization scripts can write sample data as if it were real user memory.

Mitigation: Do not run the supplied manual optimization scripts as-is in a production workspace.

## Reference(s):

- [ClawHub Optimize Context Skill Page](https://clawhub.ai/blackworm/skills/optimize-context)
- [Package Overview](artifact/SKILL.md)
- [Context Optimizer README](artifact/skills/context-optimizer/README.md)
- [Context Optimizer Skill Definition](artifact/skills/context-optimizer/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, command output, JavaScript execution results, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write context summaries, memory updates, history files, optimized message lists, and task-splitting status.]

## Skill Version(s):

1.0.0 (source: server evidence release.version and artifact config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
