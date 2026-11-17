## Description:

Provides agent guidance for local speech-to-text workflows with the Whisper CLI, including setup, file handling, command execution, and structured transcription output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users can use this skill to guide an agent through local audio transcription tasks, including environment checks, command execution, file handling, and structured text or Markdown output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad file read/write and local command execution authority.

Mitigation: Run it in a sandboxed workspace, inspect proposed commands before execution, and limit access to only the audio files and output paths needed for transcription.

Risk: The artifact gives inconsistent API-key guidance for a skill described as local Whisper transcription without an API key.

Mitigation: Verify the actual Whisper dependency and authentication requirements before use, and do not provide API keys unless the publisher clarifies the need.

Risk: The security evidence flags inconsistent, low-quality instructions that may mislead users about setup and behavior.

Mitigation: Review the skill manually before installation and validate transcription results and generated files in a non-production environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/openai-whisper-v1-2)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional JSON examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce transcription-oriented text, execution steps, troubleshooting guidance, and structured status output.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
