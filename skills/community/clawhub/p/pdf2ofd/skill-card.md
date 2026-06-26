## Description: <br>
Converts PDF documents, including invoices and reports, to high-fidelity OFD format with layout-focused precision. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xzw](https://clawhub.ai/user/xzw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document automation users use this skill to convert PDF invoices or reports into OFD files while preserving text placement, fonts, vector graphics, images, and transparency. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted PDFs and document parser dependencies carry ordinary document-handling risk. <br>
Mitigation: Use an isolated Python environment, pin current patched dependency versions, and process only PDFs intended for conversion. <br>
Risk: Input PDFs and generated OFD files may contain sensitive invoice or report content. <br>
Mitigation: Store and handle source and output files according to the user's data protection requirements. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xzw/pdf2ofd) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Code, Guidance] <br>
**Output Format:** [OFD file output with text status messages and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local .ofd document from a specified PDF input; no API keys are required.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter and package.json report 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
