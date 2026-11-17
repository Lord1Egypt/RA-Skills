## Description:

Audio transcription and text-to-speech generation using OpenRouter API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odubinkin](https://clawhub.ai/user/odubinkin)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to transcribe local audio files to text or generate speech from text through OpenRouter-backed audio models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio files and text provided to the skill are sent to OpenRouter using the configured API key.

Mitigation: Use the skill only for content that is appropriate to send to OpenRouter, and review OpenRouter's data handling terms before processing sensitive recordings.

Risk: Generated audio files are written locally and may remain in temporary or user-specified output paths.

Mitigation: Delete generated temporary audio files when they are no longer needed.

Risk: The skill requires an OpenRouter API key in the environment.

Mitigation: Provide OPENROUTER_API_KEY only in trusted environments and avoid exposing it in logs, prompts, or shared shell history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/odubinkin/skills/openrouter-audio)
- [Project homepage from skill metadata](https://github.com/odubinkin/openrouter-audio/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, files, guidance]

**Output Format:** [Plain text transcripts, JSON metadata for generated audio, and local audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated audio defaults to mp3 and is written to an OpenClaw workspace tmp directory when available, otherwise system tmp or an explicit output path.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
