## Description:

Replicates PPT screenshots, slide photos, and design mockups as editable PPTX files by reconstructing layout, colors, text, and graphic elements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dami2010](https://clawhub.ai/user/dami2010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and presentation authors use this skill to convert slide images, screenshots, photos, or design mockups into editable PowerPoint files. It guides image classification, extraction, PPTX code generation, preflight checks, and visual QA.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal use can modify the host environment through unpinned system, npm, or Python package installation.

Mitigation: Run the skill in an isolated disposable environment with dependencies pre-provisioned and pinned; require explicit approval before apt-get, global npm installs, or pip --break-system-packages on shared hosts.

Risk: Generated output and preview cleanup commands can write to or remove workspace paths.

Mitigation: Restrict outputs and preview cleanup to disposable workspace directories and review target paths before execution.

Risk: OCR and geometric reconstruction can produce inaccurate text, layout, colors, or shapes when source images are complex or low quality.

Mitigation: Use the bundled preflight checks and visual QA loop to verify boundaries, overlaps, text fit, and fidelity before delivering the PPTX.

## Reference(s):

- [PptxGenJS API Quick Reference](artifact/references/pptxgenjs-cheatsheet.md)
- [PPT Shape Recognition and Code Quick Reference](artifact/references/shapes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown guidance with JavaScript, Python, and shell snippets, plus generated editable .pptx files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses OCR, color sampling, shape reconstruction, preflight checks, and visual QA; output fidelity depends on source image quality and complexity.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
