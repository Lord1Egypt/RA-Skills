## Description:

Integrates Groq and OpenRouter models with smart free-ride optimization and bilingual Saudi Arabic/English text-to-speech for high-speed OpenClaw agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rvigoo](https://clawhub.ai/user/rvigoo)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this bundle to configure Groq/OpenRouter text models and generate bilingual Saudi Arabic/English speech output from agent responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup installs third-party Python packages, including an unpinned package invoked by configure.py.

Mitigation: Install in a virtual environment, pin or audit dependencies before use, and run configure.py only from a trusted directory.

Risk: Groq/OpenRouter API use means keys and submitted text may be sent to external providers.

Mitigation: Provide only API keys intended for this skill and avoid sending sensitive text for TTS unless provider processing is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rvigoo/skills/openclaw-turbo-bundle5)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)
- [Groq OpenAI-Compatible API Base](https://api.groq.com/openai/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands; generated speech output is a WAV file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Groq/OpenRouter API credentials and may transmit user-provided text to external providers for model or speech generation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
