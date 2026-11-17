## Description:

Takes a URL, HTML file path, or raw HTML code and generates a printable image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upwell](https://clawhub.ai/user/upwell)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to render a URL, local HTML file, or raw HTML string into a printable image with configurable format, viewport width, and full-page capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell wrapper can be abused to run arbitrary commands when given untrusted format or source inputs.

Mitigation: Validate source_type, source_content, and format before execution, and avoid using the skill with untrusted URLs, HTML, file paths, or format values until input handling is hardened.

Risk: The skill downloads an unpinned browser tool at runtime.

Mitigation: Pin or vendor agent-browser before deployment so runtime behavior is reproducible and reviewable.

Risk: Rendering URLs, local files, or raw HTML may involve network access and temporary or output file handling.

Mitigation: Document network access, temporary-file behavior, and output-directory behavior before broad use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upwell/skills/html-to-image)

## Skill Output:

**Output Type(s):** [Files, JSON]

**Output Format:** [JSON object with the generated image path and metadata; image file output in PNG, JPEG, or WebP]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes output path, file size, image format, and source type.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
