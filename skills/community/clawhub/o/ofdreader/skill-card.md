## Description: <br>
Ofd Reader extracts text from OFD (Open Fixed-layout Document) files and converts document content into Markdown with basic headings, paragraphs, and tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhanjian1972](https://clawhub.ai/user/zhanjian1972) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and document-processing users use this skill to locally extract text from OFD files or convert OFD content into Markdown for review, archival workflows, or downstream editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Converted output may contain sensitive text from user-selected OFD documents. <br>
Mitigation: Process only documents the user is allowed to handle and protect generated text or Markdown like the source document. <br>
Risk: The optional dependency installer invokes pip to install an external package. <br>
Mitigation: Use the standard-library conversion scripts by default and run the installer only when the Python package source is trusted. <br>
Risk: Complex OFD layout, table, heading, or scanned image-only content may not convert completely. <br>
Mitigation: Review converted output against the source document before relying on it. <br>


## Reference(s): <br>
- [OFD file format reference](references/ofd-format.md) <br>
- [ClawHub skill page](https://clawhub.ai/zhanjian1972/ofdreader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Plain text or Markdown written to stdout or an output file, with shell commands for invoking the bundled scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local OFD input path and optional output path; extracted content may include sensitive document text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
