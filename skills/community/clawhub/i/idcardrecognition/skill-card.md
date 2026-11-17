## Description:

Performs OCR on ID-card and similar document images, returning fields such as name, document number, birth date, address, issuing organization, and validity dates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to extract structured text from government ID cards, passports, driver licenses, residence permits, and similar document images through JisuAPI OCR. It is suited for workflows that need document fields summarized or passed to downstream systems with appropriate privacy controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Government ID, passport, license, or similar document images are sent to JisuAPI for OCR, and the returned fields may contain sensitive personal information.

Mitigation: Use the skill only when the user is comfortable sending the document image to JisuAPI, avoid retaining uploaded images locally, and redact returned PII when possible.

Risk: Path-based input can read files from the current workspace and submit their contents if the request points at an unintended local file.

Mitigation: Run the skill in a clean workspace without unrelated sensitive files or untrusted symlinks, and prefer explicit uploaded image paths or validated base64 image content.

Risk: The skill requires a JISU_API_KEY credential.

Mitigation: Use a dedicated low-privilege API key and keep it out of prompts, logs, and shared artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/idcardrecognition)
- [JisuAPI ID card recognition documentation](https://www.jisuapi.com/api/idcardrecognition/)
- [JisuAPI platform](https://www.jisuapi.com/)
- [JisuAPI recognition endpoint](https://api.jisuapi.com/idcardrecognition/recognize)
- [Publisher profile](https://clawhub.ai/user/jisuapi)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON result object or JSON error object, usually summarized for the user as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, requests, JISU_API_KEY, a document type ID, and either a local image path or base64 image content.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
