## Description:

Generates synchronized voiceover narration for a video by analyzing scenes, creating or refining timed narration, synthesizing audio with Azure TTS, and merging it into an output video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[feiskyer](https://clawhub.ai/user/feiskyer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content creators, and agents use this skill to add professional voiceover narration to screen recordings, demos, tutorials, presentations, or other video files while keeping audio aligned with visual scene timing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private video frames may remain in predictable shared temporary paths during scene extraction.

Mitigation: Use a unique private temporary directory for frame extraction and remove extracted frames after verification.

Risk: Narration text is sent to Azure TTS and may incur cloud usage costs.

Mitigation: Confirm the user expects Azure Speech processing before generation and keep Azure credentials private.

## Reference(s):

- [Azure TTS Voice Reference](artifact/references/voices.md)
- [Narration Script Template](artifact/scripts/narration_script_template.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python configuration and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a timed narration segment list and a configured local Python script that can generate Azure TTS audio segments and assemble a narrated video file.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
