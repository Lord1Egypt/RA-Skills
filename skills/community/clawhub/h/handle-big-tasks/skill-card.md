## Description:

Guides agents through large tasks one reviewable phase at a time, with completion markers and optional Copilot CLI loop scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhauga](https://clawhub.ai/user/jhauga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to break multi-stage coding work into reviewable phases and resume it manually or through optional Copilot CLI loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated loops may continue coding across many phases and modify the workspace without approval when granted write or shell permissions.

Mitigation: Review the plan first, keep Copilot permissions narrow, and avoid allow-all-tools except in trusted repositories.

## Reference(s):

- [Handle Big Tasks on ClawHub](https://clawhub.ai/jhauga/skills/handle-big-tasks)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands]

**Output Format:** [Markdown phase reports with plain-text completion markers; optional code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a final-line CONTINUE? Y or N or TASK COMPLETE! marker; optional loop scripts append session logs.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
