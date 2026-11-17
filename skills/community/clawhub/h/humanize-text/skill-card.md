## Description:

Humanize AI-generated text by removing telltale AI writing patterns from text such as punctuation habits, filler phrases, structural tells, and sycophantic openers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rustyorb](https://clawhub.ai/user/rustyorb)

### License/Terms of Use:


## Use Case:

Developers, writers, and other agent users use this skill to clean AI-like writing patterns from inline text or selected files while preserving meaning and technical accuracy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may edit user-selected files in place when asked to process files.

Mitigation: Ask for a diff or approval step before overwriting valuable documents.

Risk: Mechanical text cleanup can accidentally alter tone or meaning in important documents.

Mitigation: Review cleaned text before publishing or sending, especially for legal, policy, technical, or customer-facing material.

## Reference(s):

- [Extended AI Pattern Reference](references/extended-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or plain text, with optional file edits or shell command examples when processing files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves meaning and technical terms; supports clean, light, and preserve modes.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
