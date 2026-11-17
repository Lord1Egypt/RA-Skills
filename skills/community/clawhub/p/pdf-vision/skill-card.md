## Description:

Extract text content from image-based/scanned PDFs using multiple vision APIs with automatic fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lpq6](https://clawhub.ai/user/lpq6)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract text, tables, and structured content from scanned or image-only PDFs by converting pages to images and sending them to configured vision models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF page images and API payloads may contain sensitive document content and are sent to configured third-party vision APIs.

Mitigation: Use only PDFs that are approved for those providers, review data handling requirements, and avoid submitting confidential documents without authorization.

Risk: Temporary page images, request payloads, and API responses may remain in shared temporary directories.

Mitigation: Use a private temporary directory or cleanup process after extraction, especially for sensitive documents.

Risk: The release includes unrelated GitHub repository helper code that reads GitHub tokens.

Mitigation: Remove or ignore the GitHub helper before deployment and do not run it as part of PDF extraction workflows.

Risk: The legacy shell extractor is called out by security guidance as something to avoid.

Mitigation: Prefer the Python wrapper and enhanced extractor, and review shell script behavior before any use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lpq6/skills/pdf-vision)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, json, files]

**Output Format:** [Plain text or prompt-directed structured text, optionally written to an output file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one PDF page per invocation and uses configured third-party vision APIs.]

## Skill Version(s):

1.0.0 (source: evidence release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
