## Description:

Access Last.fm user profile, now playing, top tracks/artists/albums by period, loved tracks, and optionally love/unlove tracks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dennisooki](https://clawhub.ai/user/dennisooki)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent retrieve and summarize Last.fm listening data, including profile details, current or recent tracks, top charts, and loved tracks. When optional write credentials are configured, the skill can also love or unlove tracks on the user's Last.fm account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change the user's Last.fm account when love or unlove operations are enabled.

Mitigation: Prefer read-only use unless write actions are needed, and configure LASTFM_SESSION_KEY and LASTFM_API_SECRET only for users who intentionally enable those actions.

Risk: Long-lived write credentials may be locally exposed through process arguments during write operations.

Mitigation: Avoid using write credentials on shared or heavily monitored machines, and revoke the Last.fm session key if exposure is suspected.

Risk: The skill requires a Last.fm API key and username for read operations.

Mitigation: Store credentials only in the agent environment configuration and do not commit them to source control.

## Reference(s):

- [Last.fm API Endpoints Reference](artifact/references/api-endpoints.md)
- [Last.fm Authentication Guide](artifact/references/auth-guide.md)
- [Last.fm API Documentation](https://www.last.fm/api)
- [Last.fm Web Authentication](https://www.last.fm/api/webauth)
- [ClawHub Skill Page](https://clawhub.ai/dennisooki/skills/lastfm-openclaw)
- [ClawHub Publisher Profile](https://clawhub.ai/user/dennisooki)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style text with Last.fm profile, track, artist, album, and error summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LASTFM_API_KEY, LASTFM_USERNAME, curl, and jq; write operations require LASTFM_SESSION_KEY and LASTFM_API_SECRET.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
