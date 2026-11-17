## Description:

This skill extracts knowledge from an image and saves it locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bondli](https://clawhub.ai/user/bondli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to ingest user-supplied images from URLs, base64 strings, or local paths, run OCR and lightweight content extraction, and preserve the resulting knowledge as a local JSON record.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images and OCR text may include sensitive content that the skill saves locally.

Mitigation: Use the skill only with images and source URLs that are appropriate to retain in a local knowledge record.

Risk: Remote image URLs can cause network requests to external hosts.

Mitigation: Avoid internal or private URLs unless local retention and outbound access are intended.

Risk: Dependency behavior may change because package dependencies use semver ranges.

Mitigation: Pin and review dependency versions before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bondli/skills/image-collect)
- [Publisher profile](https://clawhub.ai/user/bondli)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance]

**Output Format:** [Console text with a JSON knowledge record and local image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores original and processed image assets plus extracted text, summary, keywords, timestamp, and saved image path in a local JSON database.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
