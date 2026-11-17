## Description:

Guides agents in converting audio or voice recordings to text with `miaoda-studio-cli speech-to-text`, including language selection and text or JSON output options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nice1234-h](https://clawhub.ai/user/nice1234-h)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn meeting recordings, interviews, and other audio files into transcripts. The skill helps an agent choose the correct CLI arguments for file path, language, and text or JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio processed through `miaoda-studio-cli` may be sent to or stored by services whose data handling is outside the skill artifact.

Mitigation: Confirm trust in `miaoda-studio-cli` and its audio data handling before use; avoid confidential recordings unless its privacy behavior matches requirements.

Risk: Long recordings, incorrect language settings, or mixed-language audio can lead to failed commands or lower-quality transcripts.

Mitigation: Split recordings longer than 10 minutes and set `--lang` to the primary spoken language, or split mixed-language audio by segment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nice1234-h/skills/miaoda-speech-to-text)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and CLI option tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide the downstream CLI to return plain text or JSON transcript output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
