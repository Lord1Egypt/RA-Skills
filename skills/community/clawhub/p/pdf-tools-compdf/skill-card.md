## Description: <br>
PDF Toolkit helps agents process PDFs through ComPDF Cloud REST APIs for conversion, page editing, compression, OCR, comparison, and document extraction workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[compdf-youna](https://clawhub.ai/user/compdf-youna) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
External users and developers use this skill to route PDF conversion, editing, OCR, compression, comparison, and document extraction requests through ComPDF Cloud after confirming external file upload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents are uploaded to ComPDF Cloud for processing, which can expose sensitive or confidential content to third-party processing. <br>
Mitigation: Proceed only after explicit user confirmation, and do not approve uploads for highly sensitive documents unless the user accepts third-party processing. <br>
Risk: A ComPDF API key may be saved locally in config/public_key.txt if the user opts in. <br>
Mitigation: Save the key only with user consent and delete config/public_key.txt to revoke local storage. <br>


## Reference(s): <br>
- [ComPDF Cloud API Reference](https://www.compdf.com/guides/api-reference/v2/overview?utm_source=clawhub&utm_medium=skillhub&utm_campaign=pdf_skill_pdf_toolkit&ref_platform_id=clawhub_skills) <br>
- [ComPDF API Complete Tool Type Reference](references/tool-list.md) <br>
- [ComPDF API Tool Parameter Details](references/parameters.md) <br>
- [ComPDF API Error Code Reference](references/error-codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Configuration guidance] <br>
**Output Format:** [Markdown status text with download links, processing metadata, and troubleshooting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request a ComPDF API key, external upload confirmation, network region selection, and optional JSON parameters; result download links expire at 24:00 the next day.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
