## Description:

Download, track, and remove movies across Plex, Radarr, and qBittorrent from chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seriallazer](https://clawhub.ai/user/seriallazer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and self-hosted media administrators use MovieFetch to check Plex availability, request movies through Radarr, monitor qBittorrent downloads, and remove movies from the media stack by chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remove workflow can delete media files by default after a partial title match.

Mitigation: Require exact movie identity, including title and year, plus explicit confirmation before removal; keep file deletion disabled unless the user clearly asks for it.

Risk: The skill needs API access to Plex, Radarr, qBittorrent, and related services.

Mitigation: Use HTTPS or loopback-only service URLs, scope credentials to the local media stack, and rotate any exposed API keys or tokens.

## Reference(s):

- [MovieFetch ClawHub listing](https://clawhub.ai/seriallazer/skills/moviefetch)
- [seriallazer publisher profile](https://clawhub.ai/user/seriallazer)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON tool results and concise user-facing text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured Plex, Radarr, qBittorrent, and related API credentials.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
