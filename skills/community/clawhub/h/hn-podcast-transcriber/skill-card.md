## Description:

Automatically fetch, transcribe, and archive Hacker News podcast episodes as searchable markdown transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to set up a local pipeline that fetches podcast RSS episodes, transcribes audio with Whisper, and stores searchable markdown archives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can fetch arbitrary RSS and audio URLs repeatedly without explicit URL allowlists or size limits.

Mitigation: Use a trusted feed, avoid attacker-provided RSS URLs, set practical run limits, and avoid unattended scheduling until allowlists and size limits are added.

Risk: Downloaded media and generated transcripts are written to a local archive path.

Mitigation: Run the skill as a low-privilege user in a contained directory and choose an archive location with appropriate storage limits.

Risk: The workflow depends on local Whisper and FFmpeg installations.

Mitigation: Install Whisper and FFmpeg in an isolated environment with reviewed versions.

## Reference(s):

- [HN Podcast Archive Directory Layout](references/archive-layout.md)
- [FFmpeg](https://ffmpeg.org)
- [Hacker News Morning Brief RSS Feed](https://media.rss.com/hacker-news-morning-brief/feed.xml)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands and generated local transcript archives]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces state.json, episode metadata, downloaded audio, raw text transcripts, and cleaned transcript.md files in a local archive.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
