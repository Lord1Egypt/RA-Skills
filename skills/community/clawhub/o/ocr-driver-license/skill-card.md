## Description:

Recognizes fields from Chinese driver's license main and secondary pages, including license number, name, gender, nationality, address, birth date, vehicle class, issue date, validity period, and archive number.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xby-skill](https://clawhub.ai/user/xby-skill)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route driver-license image URLs or base64 image data to XiaoBenYang OCR and summarize the returned recognition results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Driver-license images or base64 data are sent to the XiaoBenYang OCR API.

Mitigation: Use the skill only with appropriate consent and data-handling assurances for identity document data.

Risk: The XiaoBenYang API key may be stored in a local plaintext .env file.

Mitigation: Use a dedicated low-privilege API key, keep .env out of version control and backups, and rotate the key if exposure is suspected.

Risk: The skill sends sensitive ID data to a configurable external endpoint.

Mitigation: Verify the endpoint configuration before use and avoid processing real identity documents unless the external service is approved for the intended data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xby-skill/skills/ocr-driver-license)
- [XiaoBenYang API key site](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, json, api calls, configuration, guidance]

**Output Format:** [Markdown summary of JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key and either an image URL or base64-encoded image data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
