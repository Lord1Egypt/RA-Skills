## Description:

OpenAI Text-to-Speech API for high-quality speech synthesis. Use for generating natural-sounding audio from text with customizable voices and tones.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnj22](https://clawhub.ai/user/lnj22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate natural-sounding speech from text with OpenAI TTS models, select suitable voices and formats, and chunk long documents into audiobook-style audio files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for speech synthesis is sent to OpenAI's API.

Mitigation: Review input text for sensitive data before using the API and apply the organization's data-handling policy.

Risk: The examples create local audio files at caller-selected output paths.

Mitigation: Choose output paths intentionally and review generated files before sharing or deploying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lnj22/skills/pg-essay-to-audiobook-openai-tts)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown with Python code examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for API calls that can create local audio files such as MP3 or WAV.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
