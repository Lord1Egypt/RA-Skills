## Description:

Quickly deploys a new OpenClaw assistant agent by selecting the next assistant number, creating the workspace and agent directory structure, and updating the local OpenClaw configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhou19931993](https://clawhub.ai/user/zhou19931993)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to add a new local assistant agent without manually creating directories or editing the agent list. It is intended for requests such as adding another assistant, creating assistant2 or assistant3, or deploying a daily helper agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the deployment script can change the local OpenClaw agent configuration and create new agent workspace directories.

Mitigation: Review or back up ~/.openclaw/openclaw.json before execution and require explicit confirmation before creating agents in shared or production OpenClaw environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhou19931993/skills/multi-agent-deploy)
- [Publisher profile](https://clawhub.ai/user/zhou19931993)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and terminal output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local OpenClaw workspace and agent directories and update the local OpenClaw configuration when its deployment script is run.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
