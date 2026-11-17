## Description:

Create and manage isolated Docker workspaces on your tailnet with Claude Code and OpenCode pre-installed. Use when working with Perry workspaces, connecting to coding agents, or managing remote development environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gricha](https://clawhub.ai/user/gricha)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill as a concise command reference for creating, listing, stopping, removing, and connecting to Perry Docker workspaces on a tailnet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Perry commands described by the skill can create remote development environments, clone repositories, open SSH shells, and delete workspaces when explicitly run.

Mitigation: Install and run Perry only in trusted tailnet and workspace environments, and review each command before execution.

Risk: Workspace stop and remove commands can interrupt or delete an active development environment.

Mitigation: Confirm the target workspace name with `perry ls` before stopping or removing a workspace.

## Reference(s):

- [Perry Workspaces on ClawHub](https://clawhub.ai/gricha/skills/perry-workspaces)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise operational guidance for Perry workspace commands, SSH access, coding agent access, project paths, and troubleshooting.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
