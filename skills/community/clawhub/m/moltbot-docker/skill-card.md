## Description:

Enables the bot to manage Docker containers, images, and stacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkrdiop](https://clawhub.ai/user/mkrdiop)

### License/Terms of Use:


## Use Case:

Developers and operators use MoltDocker to ask an agent for common Docker container, image, and stack management tasks, including listing resources, starting or stopping containers, viewing logs, checking stats, cleanup, and troubleshooting with logs and inspect output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may run Docker commands that modify or remove local containers, images, or other Docker resources.

Mitigation: Confirm destructive commands such as docker rm, docker rmi, and docker system prune before execution, and review the target resource names carefully.

Risk: Docker logs and inspect output can expose secrets, internal configuration, or other sensitive environment details.

Mitigation: Limit shared command output to the needed diagnostic details, summarize large outputs, and avoid pasting secrets into follow-up prompts or reports.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill expects Docker CLI access and asks for confirmation before destructive Docker removal or prune commands.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
