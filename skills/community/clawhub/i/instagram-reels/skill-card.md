## Description:

Download Instagram Reels, transcribe the audio, and extract the caption or description.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antoinedc](https://clawhub.ai/user/antoinedc)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn Instagram Reels and similar short-form videos into transcripts, timestamped transcription JSON, and extracted captions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private or sensitive media audio may be sent to Groq for transcription.

Mitigation: Process only media that may be shared with Groq, and avoid private or sensitive reels unless that transfer is acceptable.

Risk: Exported browser cookies can expose private account access if mishandled.

Mitigation: Use cookies only when necessary for private reels, keep cookie files in a protected location, and remove them after use.

Risk: The documented fixed /tmp file paths can expose or overwrite reel metadata and audio on shared systems.

Mitigation: Run in a dedicated environment and use a unique private temporary directory for each transcription workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/antoinedc/skills/instagram-reels)
- [Groq](https://groq.com)
- [Groq Console](https://console.groq.com)
- [Groq Audio Transcriptions API Endpoint](https://api.groq.com/openai/v1/audio/transcriptions)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON transcription responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GROQ_API_KEY plus curl, yt-dlp, ffmpeg, and python3; sends audio to Groq for Whisper transcription.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
