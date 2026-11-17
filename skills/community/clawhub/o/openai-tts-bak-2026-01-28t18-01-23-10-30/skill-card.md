## Description:

Text-to-speech via OpenAI Audio Speech API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicoataiza](https://clawhub.ai/user/nicoataiza)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to convert supplied text into speech through OpenAI's Audio Speech API, selecting supported voices, models, formats, speed, and output destination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text supplied to the skill is sent to OpenAI using the configured OPENAI_API_KEY.

Mitigation: Avoid passing secrets, private data, or regulated content unless that external disclosure is intended.

Risk: Malformed or untrusted option values could alter the API request before validation is improved.

Mitigation: Use trusted values for voice, model, format, speed, and output path, and review command arguments before execution.

## Reference(s):

- [OpenAI text-to-speech guide](https://platform.openai.com/docs/guides/text-to-speech)
- [ClawHub skill page](https://clawhub.ai/nicoataiza/skills/openai-tts-bak-2026-01-28t18-01-23-10-30)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with bash commands; generated speech is returned as an audio file or stdout stream.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENAI_API_KEY and curl; supports voice, model, audio format, speed, and output path options.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
