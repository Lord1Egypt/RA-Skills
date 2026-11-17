## Description:

LAN Media Server helps agents share images, screenshots, and files with users over a local-network HTTP file server when the interaction channel cannot display media inline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nagellack5c](https://clawhub.ai/user/nagellack5c)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to expose selected workspace media files through a local HTTP link for users who cannot receive inline files in the current channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup creates a persistent unauthenticated HTTP file share listening on all network interfaces.

Mitigation: Install only when local sharing is intended; restrict network access with firewall or bind-address controls, and stop or disable the systemd user service when sharing is no longer needed.

Risk: Files placed in the shared directory may be reachable by anyone with access to the local network port.

Mitigation: Use a dedicated empty shared directory, do not place secrets there, and avoid symlinks or broad workspace paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nagellack5c/skills/lan-media-server)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Links]

**Output Format:** [Markdown with inline shell commands and HTTP links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May install and manage a persistent local-network HTTP file-sharing service.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
