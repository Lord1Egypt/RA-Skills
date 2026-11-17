## Description:

ElevenLabs text-to-speech with mac-style say UX.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffpignataro](https://clawhub.ai/user/jeffpignataro)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to generate ElevenLabs speech audio through the sag CLI, preview voices, and return MP3 voice replies when spoken responses are requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text passed to the voice command may be sent to ElevenLabs and can include secrets, personal data, or regulated content.

Mitigation: Do not pass sensitive or regulated content unless that use is acceptable for the configured ElevenLabs account.

Risk: Installation depends on the sag Homebrew tap and local CLI availability.

Mitigation: Confirm the Homebrew tap and CLI are trusted before installation or execution.

Risk: Generated MP3 files can persist locally and may contain sensitive speech.

Mitigation: Delete generated audio files when they contain sensitive or private content.

Risk: Long or character-specific voice output can use an unintended speaker or voice style.

Mitigation: Confirm the voice and speaker settings before generating long output.

## Reference(s):

- [sag homepage](https://sag.sh)
- [ClawHub skill page](https://clawhub.ai/jeffpignataro/skills/miranda-sag)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Configuration, Guidance, Files]

**Output Format:** [Markdown with inline bash code blocks and optional local audio file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the sag CLI and an ElevenLabs API key; voice responses may create local MP3 files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
