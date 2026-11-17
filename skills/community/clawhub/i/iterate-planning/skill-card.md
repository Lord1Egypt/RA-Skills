## Description:

需求迭代工作流 guides an agent through requirements interviewing, gap-based planning, and one-task iterative execution for OpenClaw projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudyli](https://clawhub.ai/user/cloudyli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product collaborators use this skill to turn unclear requirements into testable specs, implementation plans, and focused execution cycles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The execution phase can automatically edit project files and create Git commits.

Mitigation: Use the skill only in repositories where automated edits and commits are acceptable, and require review of changes before each commit.

Risk: The build prompt uses broad Git staging that may include unrelated files.

Mitigation: Replace broad staging with explicit file paths for the current task and inspect git status plus staged diffs before committing.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown specs, implementation plans, code changes, shell command guidance, and progress notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project files and Git commits during the execution phase.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
