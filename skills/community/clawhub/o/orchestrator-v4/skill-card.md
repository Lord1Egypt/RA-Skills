## Description:

Orchestrator V4 scans a project, plans module-based subtasks, and coordinates multiple AI worker sessions for analysis or fix workflows with adaptive timeouts and progress handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eviost](https://clawhub.ai/user/eviost)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to split complex code analysis, debugging, research, and fix work into coordinated subagent tasks. It is intended for OpenClaw workflows that need project scanning, task planning, bounded parallel dispatch, progress reporting, and interruption handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scan broad project trees, which may expose sensitive files in the workspace.

Mitigation: Use it only on trusted workspaces, filter or exclude secrets such as .env files, and start with plan-only or analysis mode before broader execution.

Risk: The skill can spawn child agents with inherited authority and, in fix mode, lead to file modifications.

Mitigation: Require explicit confirmation before spawning workers or applying fixes, review generated plans, and keep human oversight on write-capable tasks.

Risk: The skill persists task context while coordinating multi-agent work.

Mitigation: Avoid using it with sensitive projects unless persistence is acceptable, and review retained task context according to the workspace's data-handling expectations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eviost/skills/orchestrator-v4)
- [SKILL.md](SKILL.md)
- [README.md](README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell command examples, Python snippets, JSON task plans, progress tables, and written summary reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bounded subagent prompts, timeout settings, max-parallel configuration, retry guidance, and generated analysis or fix plans.]

## Skill Version(s):

2.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
