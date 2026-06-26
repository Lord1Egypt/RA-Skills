## Description: <br>
Extracts structured fields from medical invoice images or PDFs by sending the selected file to the SCNet OCR API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to OCR medical invoice files and extract invoice fields such as invoice number, date, payer, payee, and amount. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical invoice files may contain sensitive personal, billing, or healthcare information and are sent to SCNet's OCR service for processing. <br>
Mitigation: Use the skill only when that data transfer is acceptable for the user and organization, and verify SCNET_API_BASE before sending files. <br>
Risk: SCNET_API_KEY is a sensitive credential that could permit unauthorized API use if exposed. <br>
Mitigation: Store SCNET_API_KEY in an environment variable or chmod-600 config/.env file, and do not paste the key into chat or logs. <br>
Risk: Rapid repeated calls can hit the OCR service rate limit and cause failed or delayed recognition. <br>
Mitigation: Call the skill serially and back off before retrying when rate-limit responses occur. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/scnet-sugon/medical-invoice-ocr) <br>
- [SCNet Publisher Profile](https://clawhub.ai/user/scnet-sugon) <br>
- [Sugon-Scnet OCR API Docs](references/api-docs.md) <br>
- [Medical Invoice Field Summary](assets/templates/fields-summary.md) <br>
- [SCNet Website](https://www.scnet.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, json] <br>
**Output Format:** [Structured JSON written to stdout containing OCR result data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returned data includes OCR result entries whose elements vary by ocrType; errors are emitted as human-readable messages.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
