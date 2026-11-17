## Description:

Helps agents analyze local image files with `miaoda-studio-cli image-understanding`, including image description, targeted questions, text extraction, style analysis, and text or JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nice1234-h](https://clawhub.ai/user/nice1234-h)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when they need to understand, describe, question, or extract information from local image files through the Miaoda CLI. It is useful for image description, object or scene analysis, OCR-style extraction, visual style review, and structured JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local screenshots or photos may expose sensitive visual contents to the backend used by `miaoda-studio-cli`.

Mitigation: Use the skill only with images appropriate for that CLI and avoid submitting confidential, regulated, or private images unless the backend is approved for that data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nice1234-h/skills/miaoda-image-understanding)
- [Publisher Profile](https://clawhub.ai/user/nice1234-h)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; the underlying CLI can return text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local image file path and can accept an optional prompt and output-format option.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
