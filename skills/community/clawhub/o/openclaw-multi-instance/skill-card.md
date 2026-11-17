## Description:

OpenClaw multi-instance guidance for connecting multiple OpenClaw machines so they can communicate, transfer files, and share memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[milkteawithsoybeanmilktast](https://clawhub.ai/user/milkteawithsoybeanmilktast)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure trusted OpenClaw instances across machines for remote API handoff, SSH file transfer, and additive memory synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill establishes broad persistent trust between OpenClaw instances through API tokens and SSH access.

Mitigation: Use it only between machines you own and trust, verify SSH host keys and public-key fingerprints out of band, and keep gateway tokens confidential.

Risk: Exposing a gateway over plaintext HTTP or the public internet can allow token interception or unauthorized control.

Mitigation: Prefer private networking such as Tailscale, avoid plaintext exposure, and restrict network access to trusted peers.

Risk: Memory, identity, tools, and configuration files may contain sensitive data and are shared between machines.

Mitigation: Review synchronization actions manually, avoid syncing secret-bearing files unless required, and keep backups before automated merge or transfer operations.

Risk: The bundled synchronization script is not hardened for filename validation, safe argument handling, allowlists, backups, or disable and removal procedures.

Mitigation: Run synchronization manually or under review until those safeguards are added and tested.

## Reference(s):

- [peer-config.json5](references/peer-config.json5)
- [OpenClaw Multi-Instance ClawHub page](https://clawhub.ai/milkteawithsoybeanmilktast/skills/openclaw-multi-instance)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON5 configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may lead an agent to propose API endpoint settings, SSH trust setup, SCP file transfer, cron scheduling, and memory synchronization steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
