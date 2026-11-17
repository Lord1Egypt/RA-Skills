## Description:

Converts audio/video to MP3, transcribes speech to verbatim text and meeting notes, parses .tty terminal recordings to text, then formats structured output for OpenClaw to classify and judge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to turn local audio, video, and terminal recordings into readable transcripts, meeting notes, and structured OpenClaw handoff blocks for downstream classification and follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead users to install and run local media tooling and Python ASR packages.

Mitigation: Use a virtual environment and install only when the operator is comfortable running ffmpeg, Whisper or WhisperX, and related Python packages locally.

Risk: WhisperX diarization may require Hugging Face credentials.

Mitigation: Use minimally scoped tokens and avoid passing Hugging Face tokens directly on command lines where shell history or process listings may expose them.

Risk: Saving transcripts or Word exports can overwrite or expose local files containing sensitive meeting content.

Mitigation: Choose fresh output filenames, confirm the destination, and verify any external office-doc skill before using Word export.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-openclaw-asr)
- [Publisher profile](https://clawhub.ai/user/zhaobod1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with transcript text, meeting-note sections, command examples, and an OpenClaw delivery block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file paths for generated transcript or note files when the user asks to save outputs.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
