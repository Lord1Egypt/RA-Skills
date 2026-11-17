## Description:

Access Last.fm listening history, music stats, and discovery. Query recent tracks, top artists/albums/tracks, loved tracks, similar artists, and global charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gumadeiras](https://clawhub.ai/user/gumadeiras)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query Last.fm listening history, profile statistics, music discovery endpoints, and global charts through documented API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents sending the user's Last.fm API key and listening data over unencrypted HTTP.

Mitigation: Use HTTPS for Last.fm API calls where supported, avoid logging expanded URLs, and use a dedicated Last.fm API key.

Risk: Queries can expose a user's listening history, loved tracks, profile stats, and music preferences.

Mitigation: Configure only a Last.fm account whose listening history and profile statistics are acceptable to query through this skill.

## Reference(s):

- [Last.fm API Account Creation](https://www.last.fm/api/account/create)
- [Last.fm API Documentation](https://lastfm-docs.github.io/api-docs/)
- [Last.fm Skill Page](https://clawhub.ai/gumadeiras/skills/lastfm)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, API Calls, JSON, Guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON-oriented jq examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LASTFM_API_KEY and LASTFM_USER environment variables; generated commands query Last.fm read-only endpoints.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
