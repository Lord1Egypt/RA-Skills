## Description: <br>
Detect and redact sensitive information in PDFs, including ID numbers, phone numbers, addresses, and bank cards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing teams use this skill to scan PDFs for Chinese and international PII, choose redaction categories and modes, and produce sanitized PDFs with auditable redaction reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Redaction reports can contain truncated PII snippets and exact document locations. <br>
Mitigation: Store reports with the same protections as the source PDFs and prefer masked or category-only reporting for highly sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/pdf-sanitizer) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, PDF, guidance] <br>
**Output Format:** [Markdown guidance with command examples; runtime outputs include redacted PDF files and JSON reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON reports may include truncated PII snippets, categories, page numbers, bounding boxes, and applied redaction modes.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
