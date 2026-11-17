## Description:

Creates and coordinates a multi-agent team that decomposes complex work into planning, research, coding, writing, design, analysis, review, communication, and automation tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lixiang1076](https://clawhub.ai/user/lixiang1076)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to plan, dispatch, and summarize work across specialized subagents for complex projects, research reports, code tasks, data analysis, content creation, and automation. It also provides setup guidance and helper scripts for creating agent workspaces, managing agent profiles, and recording reusable task experience.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can coordinate agents with broad local file-write, command-execution, browser-automation, and scheduled-job capabilities.

Mitigation: Use it only in a constrained workspace and require explicit approval before command execution, browser automation, scheduled jobs, deletion, or configuration changes.

Risk: Helper scripts create and manage persistent agent workspaces and memory files.

Mitigation: Validate agent IDs and base paths before running scripts, back up existing workspaces, and review generated files before relying on them.

Risk: Persistent memory can be injected into later prompts and may carry unsafe or stale instructions.

Mitigation: Review and sanitize memory entries before prompt injection, and avoid injecting raw memory from untrusted tasks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lixiang1076/skills/lx-agent-swarm)
- [Multi-Agent System Setup Guide](references/setup-guide.md)
- [CHJ-Private Model Configuration Guide](references/chj-private-guide.md)
- [CHJ-Private Configuration Template](references/chj-private-config-template.json)
- [Task Statistics and Cost Analysis Template](references/statistics-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks, task plans, configuration snippets, and execution statistics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local agent workspace files, configuration examples, and persistent experience records when the helper scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
