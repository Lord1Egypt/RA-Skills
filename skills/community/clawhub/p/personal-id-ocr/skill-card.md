## Description: <br>
Recognizes Chinese personal ID card images and extracts structured fields such as name, gender, nationality, birth date, address, ID number, issuing authority, and validity period. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to send local ID card images or PDFs to the Scnet OCR API and receive structured JSON fields for identity-document extraction workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected files can contain sensitive identity or financial data and are uploaded to Scnet for OCR processing. <br>
Mitigation: Use only documents intentionally selected for OCR, verify the Scnet endpoint and privacy terms, and avoid sending files that should not leave the local environment. <br>
Risk: The skill requires a Scnet API key. <br>
Mitigation: Store SCNET_API_KEY in a protected environment variable or local configuration file, avoid pasting it into chat, and rotate it if it is exposed. <br>
Risk: High-volume or accidental parallel calls can hit the documented OCR API rate limit. <br>
Mitigation: Call the skill serially and retry later when rate-limited. <br>


## Reference(s): <br>
- [Sugon-Scnet OCR API Documentation](references/api-docs.md) <br>
- [ID Card Field Summary](assets/templates/fields-summary.md) <br>
- [Scnet Website](https://www.scnet.cn) <br>
- [ClawHub Skill Page](https://clawhub.ai/scnet-sugon/personal-id-ocr) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Structured JSON printed to standard output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCNET_API_KEY and uploads the selected local file to the Scnet OCR endpoint.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata, SKILL.md frontmatter, skill.yaml, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
