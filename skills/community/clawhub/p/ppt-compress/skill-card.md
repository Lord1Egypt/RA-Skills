## Description:

Compress PPT/PPTX file size by decompressing presentations, compressing large images, repackaging them, and converting the result to PDF for easier sharing or upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[accidwar](https://clawhub.ai/user/accidwar)

### License/Terms of Use:


## Use Case:

Developers and end users use this skill to reduce large PowerPoint presentations into smaller PDF files for sharing or upload workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can overwrite and delete a predictable intermediate PPTX file in the selected output folder.

Mitigation: Use an output folder you control and check for an existing file named after the input basename plus '_压缩版.pptx' before running the skill.

Risk: Sensitive presentation contents are extracted and transformed locally during compression and conversion.

Mitigation: Run the skill only on presentations and output folders appropriate for the document's sensitivity.

Risk: PDF conversion depends on a local LibreOffice installation.

Mitigation: Install LibreOffice only from a trusted source before using the conversion workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/accidwar/skills/ppt-compress)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline bash commands and local file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a compressed PDF through a local Python script that depends on macOS sips and LibreOffice.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
