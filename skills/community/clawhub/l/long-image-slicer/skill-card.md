## Description:

Long Image Slicer helps agents split long screenshots or chat captures into text-aware image slices and produce printable PDF, ZIP, and document outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yunkai](https://clawhub.ai/user/yunkai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to process long screenshots, chat records, or other tall images into readable slices and print-ready documents without cutting through detected text regions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided image URLs or local paths may introduce untrusted input.

Mitigation: Use trusted image sources and run the skill in an isolated virtual environment with reviewed or pinned dependencies.

Risk: Generated JPG, ZIP, DOCX, and PDF files may overwrite or clutter important directories if the output path is chosen poorly.

Mitigation: Choose a dedicated output directory and review the destination before running the scripts.

## Reference(s):

- [Long Image Slicer on ClawHub](https://clawhub.ai/yunkai/skills/long-image-slicer)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated JPG, ZIP, DOCX, and PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated outputs are written to the selected output directory, including a slices_v7 image folder, ZIP archive, Word document, and optional A4 PDF.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
