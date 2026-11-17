## Description:

Use OCR.space through an OOMOL-connected account to extract text from images and view conversion statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users with an OOMOL-connected OCR.space account can extract text from public images or uploaded Base64 files and retrieve conversion statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute unverified remote code and make broader, persistent changes to agent skills.

Mitigation: Review and install a verified CLI release yourself, and disable unwanted automatic skill synchronization.

Risk: Documents sent for OCR are processed by OOMOL and OCR.space, and processing may incur charges.

Mitigation: Send only documents you intend both services to process, and check applicable charges.

## Reference(s):

- [OCR.space](https://ocr.space)
- [OCR.space API documentation](https://ocr.space/ocrapi)
- [oo CLI on GitHub](https://github.com/oomol-lab/oo-cli)
- [oo CLI install guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON action results and shell commands with usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [OCR results are returned as normalized page data; statistics cover the current or previous month.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
