## Description:

Music Identify identifies songs from local audio clips with the AudD API, returns song details and Spotify links, can optionally queue matches to Spotify, and can recall prior identifications from its music log.

This skill is ready for commercial/non-commercial use.

## Publisher:

[playoffp](https://clawhub.ai/user/playoffp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to identify music from local audio clips, return song metadata and Spotify links, optionally queue matched tracks to Spotify, and recall prior identifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary reports a crafted-URI code execution flaw in the Spotify queue helper.

Mitigation: Do not use the Spotify queue feature until URI handling is fixed and reviewed.

Risk: Spotify credentials, OAuth tokens, and the music log contain private data.

Mitigation: Create credential and token files with mode 600, use a localhost OAuth callback with state validation, and treat the music log as private.

Risk: Audio clips are uploaded to AudD for recognition.

Mitigation: Only send audio clips that the user is comfortable uploading to AudD.

## Reference(s):

- [Music Identify ClawHub Skill Page](https://clawhub.ai/playoffp/skills/music-identify)
- [AudD API Reference](references/audd-api.md)
- [AudD API](https://api.audd.io/)
- [AudD](https://audd.io)
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [JSON from helper scripts and concise Markdown or plain-text responses for users.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append newline-delimited JSON identification records to memory/music-log.json and may call AudD and Spotify APIs when credentials are configured.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
