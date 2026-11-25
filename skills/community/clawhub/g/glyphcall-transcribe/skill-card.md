## Description:

Transcribes public audio URLs into text with optional speaker labels, and turns text into natural speech for MP3 playback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nutshell2000](https://clawhub.ai/user/nutshell2000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use the skill to turn public meeting, interview, voice-note, or podcast audio into readable transcripts, optionally labeled by speaker, or generate spoken MP3 responses from text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio URLs and text are sent to Glyphcall for processing, which may expose sensitive recordings or spoken text.

Mitigation: Use only recordings and text you are authorized to share; avoid sensitive material unless you understand the provider's handling and are comfortable with it.

Risk: The usage examples run the changing agentcash@latest package.

Mitigation: Review the package before running it and use a specific reviewed version instead of an unpinned latest release.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/nutshell2000/skills/glyphcall-transcribe)

## Skill Output:

**Output Type(s):** [Text, Audio]

**Output Format:** [Transcript text with optional speaker labels, or an MP3 audio response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Automatic transcripts may mishear names and numbers; unreadable or undecodable audio is not charged.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
