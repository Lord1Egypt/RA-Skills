## Description:

Log agent activities to Mission Claw dashboard with token usage tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsangwailam](https://clawhub.ai/user/tsangwailam)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to record completed work, task status, project context, duration, and token usage in a local Mission Claw activity feed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can record agent activity, project names, task descriptions, and token usage through a globally installed CLI.

Mitigation: Install only when local activity tracking is intended, review or pin the npm package before global installation, and avoid logging sensitive task details.

## Reference(s):

- [Mission Claw repository](https://github.com/tsangwailam/mcclaw)
- [Mission Claw on ClawHub](https://clawhub.ai/tsangwailam/skills/mission-claw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces logging guidance for a local CLI and daemon; no model artifact is generated.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
