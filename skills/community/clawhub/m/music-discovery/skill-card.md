## Description: <br>
Recommends tracks and playlist concepts for a user's mood, activity, BPM, energy, or genre using Spotify, Last.fm-style, and MusicBrainz-style music metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codenova58](https://clawhub.ai/user/codenova58) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn a listening context, mood, activity, or seed preference into grounded music picks and playlist outlines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Command arguments can contain sensitive listening preferences or credentials and may be saved in a local JSON history file. <br>
Mitigation: Avoid passing secrets or highly sensitive personal details as command arguments; use Spotify OAuth only when API-backed recommendations are needed. <br>


## Reference(s): <br>
- [Music Discovery Guide](references/music_discovery_guide.md) <br>
- [Spotify Web API](https://developer.spotify.com/documentation/web-api) <br>
- [MusicBrainz API](https://musicbrainz.org/doc/MusicBrainz_API) <br>
- [Spotipy Python Client](https://github.com/spotipy-dev/spotipy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown recommendation reports and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ground music claims in API results or user-stated taste; mark unavailable fields instead of guessing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
