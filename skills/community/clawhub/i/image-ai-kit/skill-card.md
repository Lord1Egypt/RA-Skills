## Description:

Image AI Kit provides local image processing and enhancement utilities for resizing, cropping, filtering, OCR text extraction, and format-oriented image workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate code and command guidance for local image enhancement, OCR extraction, smart or center cropping, and image format handling workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned Python dependencies can change over time and affect reproducibility or dependency assurance.

Mitigation: Install in an isolated Python environment and use pinned, hash-verified dependencies for higher-assurance deployments.

Risk: OCR can turn confidential image content into easily copied text.

Mitigation: Run OCR only on approved images and handle extracted text under the same confidentiality controls as the source image.

Risk: The smart subject crop behavior is simpler than the feature description may imply.

Mitigation: Review crop outputs before use in production workflows, especially when composition or subject placement matters.

## Reference(s):

- [Image AI Kit Homepage](https://github.com/openclaw/image-ai-kit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local file paths and OCR text outputs depending on the image-processing workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
