## Description:

Print local files, including PDFs, images, and Office documents, with options for copy count, duplex printing, and page ranges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[147258xuan](https://clawhub.ai/user/147258xuan)

### License/Terms of Use:

MIT-0

## Use Case:

External users can print local PDFs and images, convert images to PDF, and follow guidance for printing Office documents. They can select pages and configure copy counts or a manual duplex workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Duplex printing may ignore the selected printer and page range, potentially sending the full document to the default printer.

Mitigation: Review duplex printer and page-selection behavior before installing; confirm the destination printer and pages, especially for sensitive documents or shared default printers.

Risk: The security scan was partial because it reports a missing referenced path, so its findings may be incomplete.

Mitigation: Review the package contents and the missing referenced path before relying on the scan results.

## Reference(s):

- [Print Helper on ClawHub](https://clawhub.ai/147258xuan/skills/print-helper)
- [SumatraPDF](https://www.sumatrapdfreader.org/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance with PowerShell command examples; printed documents or converted PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Printing options include page selection, copy count, and manual duplex timing.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
