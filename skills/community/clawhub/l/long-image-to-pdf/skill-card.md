## Description:

Slices long images/screenshots into overlapping segments and auto-arranges them into a paginated PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byronleeeee](https://clawhub.ai/user/byronleeeee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and external users use this skill to convert very long screenshots, chat captures, or webpage captures into paginated PDF documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can overwrite files in the selected output directory, including an existing PDF with the chosen name.

Mitigation: Run it in a dedicated empty output directory and choose a simple, unique PDF filename.

Risk: Cleanup can remove intermediate image slices that the user may need to inspect or keep.

Mitigation: Avoid cleanup when intermediate images are needed, and keep unrelated files out of the output directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/byronleeeee/skills/long-image-to-pdf)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown with command-line invocation and generated PDF path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a PDF file and may produce intermediate image slice files unless cleanup is enabled.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
