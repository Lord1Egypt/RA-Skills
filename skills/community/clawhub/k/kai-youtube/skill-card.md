## Description:

Download and transcribe YouTube videos using yt-dlp and Whisper CLI, saving audio and transcripts for playback and summary from any YouTube URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ogdegenblaze](https://clawhub.ai/user/ogdegenblaze)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to download YouTube audio, transcribe it with Whisper CLI, and return or summarize the transcript while saving the source audio and transcript files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unvalidated URL text can influence local audio and transcript paths that are deleted and rewritten.

Mitigation: Validate exact YouTube hosts and canonical 11-character video IDs before deleting or writing files.

Risk: The skill makes outbound network requests and retains downloaded audio and transcript files in the workspace.

Mitigation: Use only trusted YouTube URLs and review or remove retained audio and transcript files according to local data-handling requirements.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, files]

**Output Format:** [Plain text transcript output with saved MP3 and TXT files; agent-facing responses may be Markdown with shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires yt-dlp and Whisper CLI; accepts a YouTube URL and optional language argument.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
