## Description:

PDF helper skill for reading, extracting, creating, modifying, merging, splitting, watermarking, OCR, encryption, and form filling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[climbkim](https://clawhub.ai/user/climbkim)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and agents use this skill to choose PDF processing tools and produce code or shell commands for extracting content, manipulating documents, running OCR, and filling forms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Annotation-based form filling can silently make persistent host font or cache changes from workspace-adjacent font files.

Mitigation: Use an isolated workspace or container, inspect nearby assets/fonts directories first, and require explicit approval before persistent environment changes.

Risk: Untrusted PDFs or directories can expose sensitive data or trigger risky PDF parsing and rendering paths.

Mitigation: Avoid running annotation-based form filling on untrusted PDFs or directories, and work on copies of sensitive PDFs.

Risk: Incorrect form coordinates or field values can produce misleading completed PDFs.

Mitigation: Validate field IDs and bounding boxes, convert output PDFs to images for inspection, and verify final documents before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/climbkim/skills/pdf-nano)
- [PDF form workflow](artifact/forms.md)
- [PDF processing advanced reference](artifact/reference.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python, JavaScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May lead an agent to create or modify local PDF, image, text, and JSON files when the recommended commands are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
