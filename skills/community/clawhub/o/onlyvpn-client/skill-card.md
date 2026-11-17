## Description:

Operates the OnlyVPN desktop client through vpn-cli.exe on Windows or vpn-cli on macOS after the main OnlyVPN client process is running.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlynet-dev](https://clawhub.ai/user/onlynet-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and automation agents use this skill to run user-directed OnlyVPN status, subscription, node selection, connect, disconnect, help, and version workflows through the desktop client's command-line interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OnlyVPN installers and downloads can establish trust in a local VPN client binary.

Mitigation: Confirm downloads are from the intended OnlyVPN provider before installing or invoking the CLI.

Risk: Copying vpn-cli to /usr/local/bin uses administrator privileges and changes a system PATH directory.

Mitigation: Review the source path and command before using sudo, and install only the intended trusted binary.

Risk: Subscription removal commands delete the named VPN subscription or configuration until it is re-added.

Mitigation: List subscriptions and confirm the target name before running removal commands.

## Reference(s):

- [OnlyVPN homepage](https://onlyvpn.net)
- [OnlyVPN CLI full reference](artifact/reference.md)
- [Only VPN ClawHub release](https://clawhub.ai/onlynet-dev/skills/onlyvpn-client)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the OnlyVPN GUI or main process to be running before CLI commands are used.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
