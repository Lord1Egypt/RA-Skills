## Description: <br>
PDF.co API integration with managed OAuth for converting, merging, splitting, editing PDFs, and extracting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to call PDF.co through Maton for PDF conversion, merging, splitting, editing, text and table extraction, invoice parsing, barcode operations, and connection management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents and extracted content are processed by Maton and PDF.co external services. <br>
Mitigation: Install only if third-party document processing is allowed for the intended files; avoid sensitive or regulated documents unless approved. <br>
Risk: The MATON_API_KEY grants access to the user's Maton-connected PDF.co workflow. <br>
Mitigation: Keep MATON_API_KEY private and supply it only through the expected environment variable or secret-management path. <br>
Risk: Write operations can modify PDFs, change passwords, or delete connections. <br>
Mitigation: Confirm the target file, selected connection, operation, and intended effect with the user before executing write, password, parsing, or deletion actions. <br>


## Reference(s): <br>
- [PDF.co ClawHub Listing](https://clawhub.ai/byungkyu/pdf-co) <br>
- [Maton Homepage](https://maton.ai) <br>
- [PDF.co API Documentation](https://docs.pdf.co) <br>
- [PDF.co API Reference](https://docs.pdf.co/api-reference) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with inline HTTP, Python, JavaScript, shell, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and PDF.co connection selection when multiple connections exist.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
