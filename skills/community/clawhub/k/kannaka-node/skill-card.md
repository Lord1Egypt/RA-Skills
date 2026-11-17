## Description:

Guides an agent through provisioning a fresh Linux server as a Kannaka node, including preflight checks, installer execution, node configuration, systemd services, verification, and hand-off reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickflach](https://clawhub.ai/user/nickflach)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to hand an agent SSH access to a Linux server and receive a configured Kannaka node with system service setup, verification, and a concise hand-off report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent SSH access and sudo authority on the target server.

Mitigation: Use it only on intended hosts, review the requested server actions before execution, and keep SSH keys and swarm credentials out of committed files and messages.

Risk: The install step downloads and runs a remote installer from a mutable URL.

Mitigation: Review or replace the installer path, pin and verify installer and binary provenance, and constrain INSTALL_URL before running installation.

Risk: The service step can install persistent systemd services and a nightly timer.

Mitigation: Inspect the generated unit files and binary before enabling services or the timer, then verify the active service and journal before hand-off.

## Reference(s):

- [Oracle Cloud free tier notes](artifact/references/oracle-cloud.md)
- [Known Kannaka node traps](artifact/references/traps.md)
- [ClawHub skill page](https://clawhub.ai/nickflach/skills/kannaka-node)
- [Kannaka installer endpoint](https://install.ninja-portal.com/kannaka)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with bash commands and hand-off report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to copy or run artifact/scripts/provision.sh on a target server and to report preflight warnings, verification status, service paths, and operational commands.]

## Skill Version(s):

1.0.2 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
