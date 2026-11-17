## Description:

Recommends music tracks and playlist concepts tailored to mood, activity, BPM, energy, or genre using Spotify and Last.fm-style metadata workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codenova58](https://clawhub.ai/user/codenova58)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate mood-aware music recommendations, playlist sketches, and concise rationale for tracks that fit a listening context. It is intended for discovery workflows grounded in API results or user-provided taste information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled command records music-related inputs locally.

Mitigation: Avoid passing secrets, account tokens, or sensitive listening preferences as command arguments, and review or clear the local data file after use.

Risk: The skill asks for unnecessary unpinned Python packages.

Mitigation: Remove unused dependencies or pin approved package versions before installation.

Risk: The described recommendation behavior is broader than the bundled CLI behavior.

Mitigation: Validate recommendations against real API results or user-provided data and mark unavailable fields instead of guessing.

## Reference(s):

- [Music Discovery guide](references/music_discovery_guide.md)
- [Spotify Web API](https://developer.spotify.com/documentation/web-api)
- [MusicBrainz API](https://musicbrainz.org/doc/MusicBrainz_API)
- [Spotipy Python client](https://github.com/spotipy-dev/spotipy)
- [Daily Reddit digest OpenClaw use case](https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/daily-reddit-digest.md)
- [Hacker News mood-based music ML discussion](https://news.ycombinator.com/item?id=42457780)
- [Reddit Spotify music recommender discussion](https://www.reddit.com/r/spotify/comments/1014b31yyz/music_recommender_ai/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with optional JSON command output and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May record command inputs locally in the bundled data file when the CLI is run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
