## Description:

Memory Dream Consolidation guides OpenClaw agents through structured memory classification, periodic Dream consolidation, and pruning of persistent memory files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xwz119](https://clawhub.ai/user/xwz119)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure and run memory maintenance for OpenClaw agents, including classifying memory entries, consolidating daily notes into durable memory, pruning stale facts, and updating Dream cycle state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may consolidate, prune, or replace persistent remembered facts.

Mitigation: Review memory changes periodically and confirm that retained facts are still useful and accurate.

Risk: Stale memory entries can mislead future agent behavior.

Mitigation: Verify recalled file paths, functions, configuration, and state snapshots against current project sources before acting on them.

## Reference(s):

- [Claude Code Memory System - Source Analysis](references/claude-code-memory-design.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide edits to persistent memory files and Dream cycle state.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
