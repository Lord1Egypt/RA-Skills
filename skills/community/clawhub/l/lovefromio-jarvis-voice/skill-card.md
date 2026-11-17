## Description:

A metallic AI voice persona that speaks assistant responses aloud with local TTS, robotic audio processing, and purple italic transcript styling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovefromio](https://clawhub.ai/user/lovefromio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and assistant users can use this skill to configure an OpenClaw assistant persona that reads responses aloud with a local JARVIS-like voice while also showing a styled transcript.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The referenced jarvis executable script is not included in the artifact.

Mitigation: Confirm the script source and contents before installing or running any executable.

Risk: Adding the SOUL.md communication protocol changes future assistant behavior to speak responses aloud.

Mitigation: Apply the protocol only where voice output is intended, and remove it when text-only responses are preferred.

Risk: Local audio playback depends on user-installed TTS and audio tools.

Mitigation: Install trusted copies of sherpa-onnx, ffmpeg, and ALSA playback tools, then verify the configured audio device before routine use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lovefromio/skills/lovefromio-jarvis-voice)
- [ClawHub publisher profile](https://clawhub.ai/user/lovefromio)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local TTS/audio playback through user-installed tooling; transcript styling depends on UI support.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
