## Description:

Manage multiple git repositories with a daemon model for periodic add, commit, pull, and push workflows on macOS launchd or Linux systemd.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samwei12](https://clawhub.ai/user/samwei12)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to set up, run, and troubleshoot unattended synchronization for multiple git repositories with per-repository configuration and service lifecycle commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Linux systemd installer can create a persistent service that runs from a user-writable script path.

Mitigation: Avoid the sudo systemd installer unless it is changed to use a dedicated unprivileged user, validate the unit name, and copy scripts to a protected root-owned location.

Risk: The daemon can automatically commit and push changes from registered repositories.

Mitigation: Use daemon mode only for intentionally trusted repositories, validate run-once behavior first, and register only clean repos with the intended branch and remote.

## Reference(s):

- [Git Sync Daemon skill page](https://clawhub.ai/samwei12/skills/git-sync-daemon)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include service lifecycle guidance for launchd or systemd and repository registration steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
