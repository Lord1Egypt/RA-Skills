## Description:

Local speech-to-text with the Whisper CLI (no API key).

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohdalhashemi98-hue](https://clawhub.ai/user/mohdalhashemi98-hue)

### License/Terms of Use:


## Use Case:

Developers, engineers, and other agent users use this skill to run local Whisper CLI speech-to-text or translation commands for audio files without an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the skill dependency may install the Whisper CLI and related dependencies through Homebrew.

Mitigation: Review the Homebrew install target and dependency changes before installation.

Risk: First use may download Whisper models into the local cache and commands may write outputs to the selected directory.

Mitigation: Review model cache expectations, audio file paths, and output directories before running commands.

## Reference(s):

- [OpenAI Whisper](https://openai.com/research/whisper)
- [ClawHub skill page](https://clawhub.ai/mohdalhashemi98-hue/skills/mh-openai-whisper)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying Whisper CLI writes transcription, translation, text, or subtitle files according to the selected command options.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
