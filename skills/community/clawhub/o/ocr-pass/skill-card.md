## Description:

Recognizes Hong Kong/Macao and Taiwan travel-permit fields, including permit number, name, sex, birth date, validity period, issuing place, and MRZ data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xby-skill](https://clawhub.ai/user/xby-skill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to submit Hong Kong/Macao or Taiwan travel-permit images by URL or Base64 and receive structured OCR results for agent-facing summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends travel-permit or passport-like images and extracted identity data to the Xiaobenyang API service.

Mitigation: Use only when the user understands the provider's privacy and retention practices, and avoid submitting real identity documents unless that disclosure is acceptable.

Risk: The skill can save the Xiaobenyang API key to a plaintext .env file.

Mitigation: Prefer a managed secret or environment variable for the API key and review local storage before deploying the skill.

Risk: Security evidence marks the release as suspicious because safeguards and disclosure for sensitive document processing are limited.

Mitigation: Review the skill before installation and restrict it to workflows where external identity-document OCR is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xby-skill/skills/ocr-pass)
- [Xiaobenyang API service](https://xiaobenyang.com)
- [Xiaobenyang MCP endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Markdown summary of JSON OCR results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an API key and either an image URL or Base64-encoded image input.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
