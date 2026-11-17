## Description:

OCR Web Service (ocrwebservice.com). Use this skill for ANY OCR Web Service request — searching and reading data. Whenever a task involves OCR Web Service, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can check their OCR Web Service account limits and subscription details, or submit a public image or PDF URL for OCR. The skill returns extracted text or output file metadata through the connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions run remote installer code whose contents have not been verified.

Mitigation: Review the CLI release and installer, and install a verified CLI release yourself before enabling the skill.

Risk: Startup synchronization can make persistent changes to agent skills that the skill does not explain.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 if you do not want additional agent skills installed or refreshed.

Risk: Documents sent for OCR are processed by OOMOL and OCR Web Service and may consume page credits.

Mitigation: Send only documents you authorize them to process, and consider page-credit costs.

## Reference(s):

- [OCR Web Service](https://www.ocrwebservice.com)
- [OCR Web Service API documentation](https://www.ocrwebservice.com/api/restguide)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-ocr-web-service)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [OCR results and account information as JSON, including extracted text or output file metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected action and submitted document.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
