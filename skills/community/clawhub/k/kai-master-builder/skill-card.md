## Description:

Developer, Code, Engineer. Guide the Agent to build apps/features/goals efficiently and securely. Creates project plans, task lists, and provides building prompts. Can run autonomously via cron or user-driven.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ogdegenblaze](https://clawhub.ai/user/ogdegenblaze)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn an app, feature, or fix goal into a structured project plan, task list, and builder prompt for iterative implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages broad autonomous coding workflows that may modify project files over time.

Mitigation: Keep unattended cron or spawned-session execution disabled unless the skill runs in a dedicated project directory with planned file changes reviewed first.

Risk: Generated plans, tasks, or builder prompts may lead an agent toward incorrect implementation steps or unsafe project changes.

Mitigation: Review the project plan, task list, and validation commands before execution, and scan or test resulting changes before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ogdegenblaze/skills/kai-master-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with project planning templates, task lists, prompts, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct creation or updates of project planning, task tracking, changelog, README, and source files.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
