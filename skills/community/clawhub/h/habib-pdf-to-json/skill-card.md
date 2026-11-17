## Description:

Extract structured data from construction PDFs and convert specifications, BOMs, schedules, and reports to Excel, CSV, or JSON using pdfplumber and optional OCR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dbmoradi60](https://clawhub.ai/user/dbmoradi60)

### License/Terms of Use:


## Use Case:

Developers and data engineers use this skill to extract tables, text, bills of materials, schedules, and specification sections from construction PDFs for downstream analysis and integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation can introduce environment drift or unexpected package versions.

Mitigation: Install dependencies in a virtual environment and pin package versions for repeatable runs.

Risk: Extracted Excel, CSV, JSON, and text outputs may contain sensitive construction project data.

Mitigation: Write outputs only to approved directories and delete, restrict, or encrypt extracted files when no longer needed.

## Reference(s):

- [Data-Driven Construction](https://datadrivenconstruction.io)
- [pdfplumber documentation](https://github.com/jsvine/pdfplumber)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local extraction examples and export patterns for Excel, CSV, JSON, JSON Lines, and text files.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
