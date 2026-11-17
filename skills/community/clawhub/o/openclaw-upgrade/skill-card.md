## Description:

Helps developers upgrade OpenClaw in GitHub-restricted network environments by using Yarn and related verification and troubleshooting commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hyqdq888](https://clawhub.ai/user/hyqdq888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and server operators use this skill to upgrade OpenClaw when direct GitHub access prevents npm-based updates. It provides Yarn install, verification, troubleshooting, registry configuration, backup, compatibility, and gateway restart guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends persistent global package-manager registry changes that can affect future installs.

Mitigation: Confirm the intended registry source before applying the configuration and restore the prior registry after the upgrade if it is no longer needed.

Risk: The skill provides package-manager install commands and gateway restart guidance that can affect a running OpenClaw environment.

Mitigation: Confirm the target OpenClaw version, avoid running package-manager installs as root, back up configuration, verify plugin compatibility, and schedule any gateway restart appropriately.

## Reference(s):

- [OpenClaw Upgrade on ClawHub](https://clawhub.ai/hyqdq888/skills/openclaw-upgrade)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
