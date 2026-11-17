## Description:

Extracts five visually interesting square close-up crops from an uploaded image, displays them in chat with labels and explanations, and saves them as downloadable files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosemaxio](https://clawhub.ai/user/rosemaxio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to identify visually interesting regions in uploaded artwork, technical drawings, or detailed photographs and generate labeled square close-up crops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run local Python on uploaded image files.

Mitigation: Run it in an isolated environment and review image-handling commands before execution.

Risk: The skill recommends installing Pillow at runtime without a pinned version.

Mitigation: Use a prebuilt virtual environment or pinned dependency specification before using the skill.

Risk: Uploaded filenames could be handled unsafely if inserted directly into code.

Mitigation: Validate or sanitize filenames and pass paths as data rather than interpolating them into executable code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rosemaxio/skills/image-highlight-cropper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown summary with downloadable JPEG crop files and optional inline Python/shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces five square highlight crops by default, with labels and short explanations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
