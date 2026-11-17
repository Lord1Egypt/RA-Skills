## Description:

Docker container lifecycle management for listing containers, starting and stopping containers, viewing logs, checking stats, and pruning unused containers or images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppopen](https://clawhub.ai/user/ppopen)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to ask an agent for Docker CLI commands that inspect containers, manage container lifecycle, view logs and resource usage, and clean up unused Docker resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup and prune requests may remove stopped containers or unused images.

Mitigation: Ask the agent to show the Docker resources that would be removed and require explicit confirmation before running prune commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ppopen/skills/openclaw-skill-docker-manager)

## Skill Output:

**Output Type(s):** [shell commands, code, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Docker CLI and a running Docker daemon.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
