## Description: <br>
Enables the bot to manage Docker containers, images, and stacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mkrdiop](https://clawhub.ai/user/mkrdiop) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use MoltDocker to ask an agent for Docker container, image, stack, log, stats, and troubleshooting commands while preserving confirmations for destructive Docker actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Docker commands can stop containers, remove images, prune Docker data, or otherwise affect running services. <br>
Mitigation: Review proposed Docker commands and require explicit confirmation before destructive operations such as docker rm, docker rmi, and docker system prune. <br>
Risk: Docker logs, inspect output, and configuration details may expose sensitive environment or service information. <br>
Mitigation: Summarize large outputs and avoid sharing sensitive values from logs, environment variables, or container configuration unless the user explicitly needs them. <br>
Risk: Installing this skill allows an agent to operate Docker on the user's machine. <br>
Mitigation: Install it only in environments where agent-assisted Docker operations are intended and acceptable. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may include Docker actions that should be reviewed before execution; destructive actions require confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
