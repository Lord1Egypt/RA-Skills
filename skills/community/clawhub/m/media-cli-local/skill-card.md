## Description:

Single-file Bash CLI for managing Sonarr, Radarr, Prowlarr, qBittorrent, Bazarr, Jellyseerr, and Tdarr from a local terminal or AI agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

External homelab users and developers use this skill to let an agent produce local media-stack shell commands for searching, adding, monitoring, pausing, resuming, and inspecting movies, TV shows, downloads, subtitles, requests, and transcoding status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install flow asks users to run code from an unpinned external repository.

Mitigation: Review the upstream media script before installation and prefer a pinned commit or verified release.

Risk: Agent-issued commands can change local media services or delete downloads when destructive command options are used.

Mitigation: Grant this skill only to trusted agents and require explicit user confirmation before pause, resume, remove, or delete-file operations.

Risk: The CLI stores media-service API URLs and keys in a local configuration file.

Mitigation: Keep the configuration file permissions restricted and avoid exposing its contents in logs, prompts, or shared terminal output.

## Reference(s):

- [Media Cli Source Repository](https://github.com/solomonneas/media-cli)
- [ClawHub Skill Page](https://clawhub.ai/solomonneas/skills/media-cli-local)
- [Publisher Profile](https://clawhub.ai/user/solomonneas)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Markdown with inline shell commands and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target local media services and may return parseable terminal output from the media CLI.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
