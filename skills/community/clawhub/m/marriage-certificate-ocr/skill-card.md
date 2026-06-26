## Description: <br>
Automatically extracts marriage-certificate holder, registration date, certificate number, names, birth dates, identity numbers, and related fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to submit a local marriage-certificate image or PDF to Scnet's OCR service and receive structured recognition results. It is intended for extracting key certificate fields and confidence data into JSON for downstream review or processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends marriage-certificate files and extracted identity details to Scnet's OCR service. <br>
Mitigation: Use it only with appropriate consent and a valid privacy or compliance basis for processing the documents. <br>
Risk: A misconfigured API base URL could send sensitive documents to an unintended endpoint. <br>
Mitigation: Verify SCNET_API_BASE before use and keep the default service endpoint unless a trusted alternate endpoint is required. <br>
Risk: The SCNET_API_KEY is a sensitive credential. <br>
Mitigation: Store the key in the local config/.env file with restricted permissions and do not paste it into chat transcripts or shared logs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/scnet-sugon/marriage-certificate-ocr) <br>
- [Sugon-Scnet OCR API documentation summary](references/api-docs.md) <br>
- [Marriage certificate field summary](assets/templates/fields-summary.md) <br>
- [Scnet website](https://www.scnet.cn) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Shell commands, Configuration instructions] <br>
**Output Format:** [Structured JSON written to standard output, with friendly error text when calls fail] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCNET_API_KEY; optional SCNET_API_BASE controls the OCR API endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, skill.yaml, changelog, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
