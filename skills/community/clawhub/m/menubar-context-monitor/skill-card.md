## Description:

macOS menu bar context monitor for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hjklasdfg](https://clawhub.ai/user/hjklasdfg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install and configure a macOS SwiftBar menu-bar monitor that shows agent context usage, model aliases, status, and recent activity for local or remote OpenClaw hosts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags this release for review because it installs a persistent SwiftBar plugin that reads OpenClaw session data and may SSH to another machine every 30 seconds.

Mitigation: Review the setup guide and scripts before installation, install only for trusted OpenClaw hosts, and verify SSH host keys manually.

Risk: The security guidance warns against unattended installs and notes hidden agent setup steps.

Mitigation: Avoid unattended --yes installs unless the commands have been reviewed, and require explicit approval before installing SwiftBar or deploying remote collectors.

Risk: The security guidance says not to rely on environment-variable customization unless the SSH command handling is fixed.

Mitigation: Use explicit installer arguments or inspect the generated SwiftBar plugin configuration instead of depending on environment-variable overrides.

## Reference(s):

- [Context Monitor ClawHub release](https://clawhub.ai/hjklasdfg/skills/menubar-context-monitor)
- [SwiftBar](https://github.com/swiftbar/SwiftBar)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup guidance for macOS SwiftBar monitoring and may direct installation of local or SSH-based collector scripts.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
