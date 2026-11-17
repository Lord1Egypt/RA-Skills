## Description:

Text-to-speech via OpenAI Audio Speech API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pors](https://clawhub.ai/user/pors)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to convert supplied text into speech through OpenAI's audio speech endpoint, choosing supported voices, models, formats, speed, and optional file output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text provided to the skill is sent to OpenAI for speech generation.

Mitigation: Avoid using the skill with secrets or confidential content unless that use is allowed in the deployment environment.

Risk: The --out option writes generated audio to a user-selected local path.

Mitigation: Review output paths before execution to avoid overwriting or placing files in unintended locations.

## Reference(s):

- [OpenAI Text-to-Speech Documentation](https://platform.openai.com/docs/guides/text-to-speech)
- [ClawHub OpenAI TTS Skill](https://clawhub.ai/pors/skills/openai-tts)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Shell command output and generated audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and OPENAI_API_KEY; --out writes generated audio to the selected local path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
