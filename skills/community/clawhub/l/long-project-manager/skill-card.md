## Description:

Create and maintain a persistent file-based workspace for long-running, multi-session, or interruption-sensitive work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianxiangma](https://clawhub.ai/user/tianxiangma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, writers, planners, and operations teams use this skill to create and resume durable project workspaces for tasks that span multiple sessions or context resets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local project notes may contain secrets, sensitive business details, or private project context if the user asks the agent to record them.

Mitigation: Review the project folder path and avoid writing secrets or sensitive details into generated markdown files unless local storage is acceptable.

Risk: Durable project files can preserve outdated status or decisions if they are not refreshed before pausing work.

Mitigation: Update STATUS.md and HANDOFF.md before stopping so the next session resumes from current project state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianxiangma/skills/long-project-manager)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown files and concise project-state summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local project note files under projects/<project-name>/ when the user asks for durable project state.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
