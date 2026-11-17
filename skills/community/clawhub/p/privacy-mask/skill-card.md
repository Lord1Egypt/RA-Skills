## Description:

Privacy Mask helps agents detect and locally redact sensitive information in screenshots and images using OCR, regex rules, and optional NER before further analysis or sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fullstackcrew-alpha](https://clawhub.ai/user/fullstackcrew-alpha)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support engineers, and other users handling screenshots use this skill to detect PII or secrets in image files, generate masked copies, and avoid sending unredacted images to external services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on unpinned external code through the privacy-mask CLI.

Mitigation: Install only from a trusted source, pin a reviewed privacy-mask version, and verify the package before enabling the skill.

Risk: The reviewed artifact references an automatic prompt-submit image-processing hook, but the hook script is missing from the artifact.

Mitigation: Review the hook script and confirm its behavior before enabling automatic prompt-submit masking.

Risk: The skill reads and writes screenshots or cached prompt images that may contain sensitive data.

Mitigation: Run processing locally, preserve originals unless in-place masking is explicitly intended, and review masked output before sharing.

## Reference(s):

- [Privacy Mask homepage](https://github.com/fullstackcrew-alpha/privacy-mask)
- [ClawHub Privacy Mask skill page](https://clawhub.ai/fullstackcrew-alpha/skills/privacy-mask)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON CLI output, and masked image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local tesseract, python3, and privacy-mask binaries; masked files are written locally.]

## Skill Version(s):

0.3.5 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
