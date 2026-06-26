## Description: <br>
Extracts text and household-register fields from images, PDFs, or archives by sending the selected file to the Scnet OCR API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents use this skill when a user needs OCR extraction from a household-register document and can provide a local file path plus the HOUSEHOLD_REGISTER recognition type. It is intended for workflows that need structured JSON fields from sensitive identity documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Household-register images, PDFs, archives, and extracted text may contain highly sensitive personal data and are sent to Scnet for OCR processing. <br>
Mitigation: Upload only the pages needed for the task, avoid unnecessary personal data, and review Scnet privacy and retention terms before use. <br>
Risk: The skill requires a Scnet API key, and exposing the key in chat or logs could allow unauthorized API use. <br>
Mitigation: Store SCNET_API_KEY in a protected environment variable or config/.env file with restricted permissions, and do not paste credentials into chat. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scnet-sugon/household-book-ocr) <br>
- [Scnet website](https://www.scnet.cn) <br>
- [Scnet OCR API documentation summary](references/api-docs.md) <br>
- [Household-register field summary](assets/templates/fields-summary.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON on stdout for successful OCR results; text error messages for configuration, credential, network, and API failures.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ocrType and filePath inputs, supports HOUSEHOLD_REGISTER, and uses SCNET_API_KEY for authenticated API calls.] <br>

## Skill Version(s): <br>
1.0.8 (source: skill.yaml, SKILL.md frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
