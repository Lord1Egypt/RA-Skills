## Description:

Provides a Whisper CLI-oriented speech-to-text helper for local transcription, with claims of multilingual and batch audio handling but inconsistent API-key requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content creators, and automation users can use this skill to guide local speech-to-text transcription workflows with Whisper-style command-line processing. Reviewers should verify the actual credential and execution requirements because the release evidence flags inconsistent no-key and API-key claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags inconsistent claims around local no-key Whisper usage versus API-key and credential handling.

Mitigation: Confirm whether the skill actually needs external API credentials before installation, and avoid providing API keys unless the publisher documents the requirement.

Risk: The skill requests command execution and file write capabilities for transcription workflows.

Mitigation: Run it in a constrained workspace, review proposed commands before execution, and limit file access to the audio and output paths required for the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/openai-whisper-v1)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe generated transcription results, execution status, troubleshooting steps, and environment configuration.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
