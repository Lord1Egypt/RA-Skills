## Description: <br>
Parse a PDF into structured JSON: text, layout-aware blocks with bounding boxes, tables, and image metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rishabhdugar](https://clawhub.ai/user/rishabhdugar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract text, tables, image metadata, and layout-aware blocks from PDFs for document processing workflows such as invoices, forms, reports, contracts, resumes, and research papers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected PDFs or PDF URLs are sent to pdfapihub.com for parsing. <br>
Mitigation: Use the skill only with documents approved for that provider, and avoid confidential or regulated PDFs unless your organization has approved the workflow. <br>
Risk: The skill requires a CLIENT-API-KEY credential. <br>
Mitigation: Store and transmit the API key as a sensitive secret, rotate it if exposed, and avoid placing real keys in prompts, examples, or logs. <br>


## Reference(s): <br>
- [PDF API Hub](https://pdfapihub.com) <br>
- [PDF API Hub Documentation](https://pdfapihub.com/docs) <br>
- [ClawHub Skill Page](https://clawhub.ai/rishabhdugar/pdf-parse) <br>
- [Publisher Profile](https://clawhub.ai/user/rishabhdugar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for invoking an external PDF parsing API that returns structured JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
