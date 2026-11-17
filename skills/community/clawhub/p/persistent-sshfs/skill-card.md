## Description:

Helps bring up SSHFS mounts with retry-until-connected behavior and provides instructions for periodically rerunning the script to restore mounts that later drop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system administrators use this skill to set up SSHFS mounts with key-based authentication and arrange periodic reruns to recover mounts that fully disconnect.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing a mutable remote script with sudo could run unreviewed changes with elevated privileges.

Mitigation: Review the downloaded script before installation and pin it to a known commit or verify its checksum.

Risk: Recurring mount jobs keep connections and remote filesystems available across sessions.

Mitigation: Enable cron or systemd reruns only for trusted SSH hosts and mount paths you intend to keep active.

## Reference(s):

- [Setup instructions](references/setup.md)
- [Persistent Sshfs on ClawHub](https://clawhub.ai/psyb0t/skills/persistent-sshfs)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mounts need key-based SSH authentication; periodic reruns restore fully dropped mounts.]

## Skill Version(s):

1.0.7 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
