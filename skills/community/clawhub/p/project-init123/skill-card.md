## Description:

Automatically initializes Gitea research project repositories by collecting repository details, creating a standard directory structure, adding README.md, CONTRIBUTING.md, member profiles, collaborator permissions, startup issues, and email notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research teams use this skill to create or initialize Gitea project repositories with a consistent collaboration structure, baseline documentation, member profiles, starter issues, and notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Gitea personal access token that can create repositories, write files, manage collaborators, and create issues.

Mitigation: Use a minimally scoped bot token, rotate it regularly, store it only in the protected configuration file, and review token permissions before installation.

Risk: Default configuration examples use plain HTTP for the Gitea server.

Mitigation: Use HTTPS for production or shared organizations and verify the configured Gitea URL before running setup.

Risk: Conversation state is stored in a shared temporary file.

Mitigation: Use per-user or per-session protected state before deploying in a multi-user environment.

Risk: The setup script installs Python dependencies into the active environment.

Mitigation: Install dependencies in an isolated environment and review dependency changes before running setup on production hosts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/myd2002/skills/project-init123)
- [Publisher profile](https://clawhub.ai/user/myd2002)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown conversation responses, generated repository files, Gitea API changes, and setup/configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and python3; repository initialization depends on configured Gitea and email credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
