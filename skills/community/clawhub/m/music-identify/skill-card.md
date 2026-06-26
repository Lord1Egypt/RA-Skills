## Description: <br>
Identify songs from audio clips using AudD API and optionally queue them to Spotify. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[playoffp](https://clawhub.ai/user/playoffp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent builders use this skill to identify songs from local audio clips, return artist and track details, optionally queue matches to Spotify, and recall prior identifications from a local music log. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chosen audio clips are sent to AudD for recognition. <br>
Mitigation: Use only audio clips the user intends to submit to AudD and avoid sending sensitive private recordings. <br>
Risk: Optional Spotify integration requires playback read/write OAuth access and local token storage. <br>
Mitigation: Enable Spotify only when queueing is needed, keep credential and token files restricted to the user, and revoke access if no longer required. <br>
Risk: The security review flagged the Spotify queue feature as review-needed until URI encoding and restrictive token-file permissions are fixed. <br>
Mitigation: Review the Spotify scripts before deployment, confirm URI handling with representative track URIs, and enforce restrictive permissions on token files. <br>
Risk: The local music log records identified songs and may reveal listening history. <br>
Mitigation: Review, rotate, or delete the local music log when song history should not be retained. <br>


## Reference(s): <br>
- [AudD API Reference](references/audd-api.md) <br>
- [AudD](https://audd.io) <br>
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) <br>
- [ClawHub Release Page](https://clawhub.ai/playoffp/music-identify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with JSON script results and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include song title, artist, album, Spotify URL, queue status, not-found messages, errors, and local music-log entries.] <br>

## Skill Version(s): <br>
1.2.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
