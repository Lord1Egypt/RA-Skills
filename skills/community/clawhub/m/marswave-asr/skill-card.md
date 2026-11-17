## Description:

Transcribes audio files to text using local speech recognition and supports optional transcript polishing and Markdown export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xfango](https://clawhub.ai/user/0xfango)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to transcribe local audio files, optionally improve transcript readability, and save transcript metadata in Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the external `@marswave/coli` CLI and may download speech models on first use.

Mitigation: Install only from a trusted source, preinstall and verify the CLI and models in controlled environments, and avoid unnecessary privileges for install commands.

Risk: Sensitive audio may be transcribed or saved to a Markdown file in the current working directory.

Mitigation: Use the skill in a trusted local environment and review the transcript filename and destination before saving Markdown output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xfango/skills/marswave-asr)
- [Publisher profile](https://clawhub.ai/user/0xfango)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Conversation text, Markdown transcript files, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May polish raw transcripts for readability and may export a Markdown file with source, date, model, duration, and language metadata.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
