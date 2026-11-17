## Description:

Huo15 Multi Agent helps an agent coordinate multiple OpenClaw subagents for parallel task assignment, worker execution, and result aggregation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jobzhao15](https://clawhub.ai/user/jobzhao15)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to split independent work across multiple OpenClaw subagents, monitor worker status, and summarize the resulting work back into the main agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled scripts may make local file changes or trigger command execution if they receive crafted task names, worker IDs, or result text.

Mitigation: Review before installing, use trusted inputs only, and avoid enabling exec/process for subagents until strict input validation, safe JSON serialization, confirmation for deletion, and clear permission limits are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jobzhao15/skills/huo15-multi-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline JavaScript, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes suggested OpenClaw subagent commands, coordination workflow guidance, and local configuration examples.]

## Skill Version(s):

2.0.0 (source: server release metadata and skill version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
