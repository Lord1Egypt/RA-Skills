## Description:

Generates standardized Chinese meeting agenda documents as Word (.docx) and PDF files from user-provided meeting details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ywwzzsgit](https://clawhub.ai/user/ywwzzsgit)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, and administrative staff use this skill to turn meeting titles, times, locations, agenda items, hosts, and participant lists into standardized Chinese government/enterprise meeting agenda documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install Python packages during execution.

Mitigation: Preinstall reviewed dependencies in a controlled environment and avoid runtime package installation where possible.

Risk: Crafted filename values may write generated files outside the intended output folder.

Mitigation: Use a dedicated output directory and validate filename inputs before running the generator.

Risk: PDF conversion depends on local Office, LibreOffice, docx2pdf, and Chinese font availability.

Mitigation: Confirm both generated files before delivery; if PDF conversion fails, deliver the Word file and export PDF manually from a trusted office suite.

## Reference(s):

- [会议议程模板规范](references/template.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Word (.docx) and PDF files generated from structured JSON input]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces paired document outputs; PDF generation can depend on local Office, LibreOffice, docx2pdf, and Chinese font availability.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
