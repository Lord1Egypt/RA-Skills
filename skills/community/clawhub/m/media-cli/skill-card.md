## Description:

Media Cli helps agents manage a remote *arr media stack from the terminal through an SSH-aware bash CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent builders use this skill to let an agent inspect and manage Sonarr, Radarr, Prowlarr, qBittorrent, Bazarr, Jellyseerr, and Tdarr without exposing those services publicly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install external code that can control media services through API keys or SSH access.

Mitigation: Review the external repository before installing, prefer a pinned commit or signed release, and grant only the service credentials and SSH access needed for the intended workflow.

Risk: Media and download management commands can remove downloads, delete files, pause activity, or trigger broad refresh operations.

Mitigation: Require human review before destructive or bulk actions, especially commands that remove downloads, delete files, pause all downloads, or rescan libraries.

Risk: Stored API keys and SSH configuration may give an agent persistent access to personal media services.

Mitigation: Keep the media-cli configuration file permission-restricted, rotate credentials when access changes, and avoid configuring services the agent should not manage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/solomonneas/skills/media-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that affect media libraries, downloads, API-backed services, or SSH-connected hosts.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
