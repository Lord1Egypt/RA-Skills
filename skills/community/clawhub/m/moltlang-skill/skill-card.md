## Description:

Translate between English and MoltLang, a compact AI language for efficient, validated, and error-handled agent communication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonlnheath](https://clawhub.ai/user/jasonlnheath)

### License/Terms of Use:


## Use Case:

Developers and AI agents use this skill to translate operational instructions between natural language and MoltLang, validate MoltLang expressions, list supported tokens, and estimate token-efficiency savings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a public API, which may expose prompts, credentials, private text, or proprietary content if users submit sensitive material.

Mitigation: Do not send secrets, credentials, private prompts, or proprietary text to the public API unless its privacy and retention guarantees have been independently reviewed.

Risk: The skill references package installation through pip or npm, so users may execute third-party package code in their environment.

Mitigation: Review the MoltLang package source before installation or install and test it in an isolated virtual environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jasonlnheath/skills/moltlang-skill)
- [MoltLang GitHub repository](https://github.com/jasonlnheath/moltlang)
- [MoltLang API](https://moltlang.up.railway.app)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text responses containing translations, validation results, efficiency calculations, command names, and installation guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can reference public API usage or local installation through pip or npm.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
