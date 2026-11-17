## Description:

Manage Plex Media Server with optional Nvidia Shield ADB device management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grewingm](https://clawhub.ai/user/grewingm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media server operators use this skill to discover and configure Plex Media Server, search media metadata, monitor active sessions, manage libraries, check server health, and optionally control an Nvidia Shield over ADB.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Plex token that can grant full account and server access.

Mitigation: Use it only in trusted environments, avoid shared machines, protect the local configuration file, and rotate any token exposed in command examples.

Risk: Optional ADB support can control a Shield device, including rebooting the device and restarting Plex.

Mitigation: Enable ADB only when needed, restrict it to trusted networks, and review or add explicit confirmation before disruptive actions.

Risk: Token handling and local server transport may expose sensitive access on untrusted networks.

Mitigation: Review HTTPS use and token handling before relying on the skill outside a trusted local network.

## Reference(s):

- [ClawHub Plex Server Skill](https://clawhub.ai/grewingm/skills/plex-server)
- [Plex Web](https://app.plex.tv)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [JSON responses, Markdown/text summaries, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local Node.js, curl, and optional ADB commands against configured Plex and Shield endpoints.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
