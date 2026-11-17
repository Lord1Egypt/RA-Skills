## Description:

Transcribe and extract subtitles from YouTube videos using yt-dlp by providing the video URL for text-based captions or transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neckr0ik](https://clawhub.ai/user/neckr0ik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch YouTube captions or auto-generated subtitles, convert them into plain text, and save or analyze the resulting transcript.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a telemetry request over unencrypted HTTP by default, exposing the user's IP address to the author's telemetry endpoint.

Mitigation: Set DISABLE_TELEMETRY=1 before running the skill, or enforce that environment variable in managed agent environments.

Risk: Transcript retrieval depends on YouTube captions or auto-generated subtitles being available for the requested language.

Mitigation: Confirm caption availability and choose an appropriate --language value before relying on the transcript.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neckr0ik/skills/neckr0ik-youtube-transcript)
- [Publisher profile](https://clawhub.ai/user/neckr0ik)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text transcript or saved text file, with Markdown usage guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and yt-dlp; subtitle language defaults to en and output can be written to stdout or a file.]

## Skill Version(s):

1.0.0 (source: server release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
