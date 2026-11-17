## Description:

Build music recommendations and create Spotify playlists using Last.fm similarity and listening history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanestane](https://clawhub.ai/user/stanestane)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate Last.fm-based music recommendations, match them on Spotify, and optionally create playlists in a Spotify account they control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Last.fm and Spotify credentials, and the saved Spotify token can authorize future account access.

Mitigation: Use credentials only for accounts intended for this workflow, restrict token file access, and delete ~/.openclaw/spotify-token.json when the saved session is no longer needed.

Risk: Playlist creation modifies the connected Spotify account.

Mitigation: Use playlist creation only when requested, verify the target Spotify account during OAuth, and review playlist name, visibility, and generated track list before relying on the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stanestane/skills/lastfm-spotify-playlists)
- [Last.fm API endpoint](https://ws.audioscrobbler.com/2.0/)
- [Spotify Web API endpoint](https://api.spotify.com/v1)
- [Spotify authorization endpoint](https://accounts.spotify.com/authorize)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts can return recommendation lists, Spotify match details, unmatched tracks, and playlist metadata.]

## Skill Version(s):

1.5.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
