## Description:

Transcribes local video or audio files and public video links into cleaned text, with optional prompts for summaries, rewrites, quotes, and translations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, media teams, and developers use this skill to transcribe completed video or audio and produce summaries, meeting notes, or adapted copy from the resulting content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected media, prompts, and task metadata are sent to an external paid service.

Mitigation: Obtain consent before sending media, check the vendor's privacy and retention terms for confidential material, and monitor paid usage.

Risk: Temporary downloads and the last task ID may remain locally until cleanup runs.

Mitigation: Remove temporary files and saved task identifiers after processing sensitive content.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/engheng-art/skills/guaikei-all-platform-video-transcript)
- [GuaiKei service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text or prompt-directed structured text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcription or generated copy is returned on standard output; progress messages use standard error.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
