## Description: <br>
Build music recommendations and create Spotify playlists using Last.fm similarity and listening history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanestane](https://clawhub.ai/user/stanestane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn Last.fm listening history, top artists, or seed tracks into ranked music recommendations and optional Spotify playlists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spotify playlist write access can create playlists and add tracks for the authenticated Spotify account. <br>
Mitigation: Install only when this access is acceptable, keep credential and token JSON files private, use explicit token paths when tighter control is needed, and revoke the Spotify app or delete the saved token when no longer used. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/stanestane/lastfm-spotify-playlists) <br>
- [Last.fm API endpoint](https://ws.audioscrobbler.com/2.0/) <br>
- [Spotify Web API](https://api.spotify.com/v1) <br>
- [Spotify OAuth authorization](https://accounts.spotify.com/authorize) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, API calls] <br>
**Output Format:** [JSON results printed to stdout, with guidance and shell commands when setup or execution is needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Spotify playlists when run with Spotify output mode and playlist creation enabled.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
