## Description:

Searches ten music platforms for a requested song, retrieves a playable media URL, and downloads an MP3 file to /tmp/music with automatic source fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wehaha](https://clawhub.ai/user/wehaha)

### License/Terms of Use:

MIT-0

## Use Case:

Agents can use this skill to help users search supported third-party music sources and download a matching MP3 file. It is most relevant for workflows that need command-line music lookup, automatic source fallback, and a returned local file path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader bypasses HTTPS certificate validation while contacting third-party music sites.

Mitigation: Use a fixed version that keeps TLS verification enabled before deploying in higher-trust environments.

Risk: The downloader saves remote-provided files without enough validation or download size limits.

Mitigation: Validate media URL domains and file types, and enforce a reasonable maximum download size before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wehaha/skills/music-downloader)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [MP3 file path or failure message from command-line execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloaded files are saved under /tmp/music with artist_song.mp3-style filenames.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
