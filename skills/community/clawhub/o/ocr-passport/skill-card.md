## Description:

Recognizes passport numbers, Chinese and English names, gender, nationality, birth dates, issue dates, expiration dates, issuing locations, and MRZ machine-readable code from passport images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to route passport OCR requests to the Xiaobenyang service, collect either an image URL or Base64 image input, and return structured passport identity fields to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes passport images and extracted identity data through an external service.

Mitigation: Install only if the Xiaobenyang service is trusted with passport images and identity data.

Risk: API keys may be written to a local .env file and exposed from shared or untrusted working directories.

Mitigation: Use a low-privilege API key, prefer temporary or session-only key handling, inspect .env files before use, and rotate the key if exposure is possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/ocr-passport)
- [Xiaobenyang API key service](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API Calls, guidance]

**Output Format:** [Markdown summary of JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns success status, raw OCR response data, and a status message.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
