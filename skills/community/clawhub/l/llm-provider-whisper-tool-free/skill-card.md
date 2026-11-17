## Description:

Local Whisper CLI speech-to-text guidance for transcribing common audio formats and translating audio without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to install and run a local Whisper command-line workflow for single-file transcription, subtitle generation, and speech translation. It is aimed at personal or workflow automation use where local processing is preferred.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags inconsistent API-key guidance.

Mitigation: Do not provide API keys for this skill unless new authoritative release evidence requires them; use it only for local transcription, subtitle generation, or speech translation tasks.

Risk: The security summary flags an overbroad trigger that could cause exec-enabled agents to use the skill for unrelated media tasks.

Mitigation: Limit use to explicit transcription, subtitle generation, or speech translation requests, and review setup or execution commands before running them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/llm-provider-whisper-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command guidance and output-format choices for local Whisper transcription, subtitle files, JSON, TSV, or translated text.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
