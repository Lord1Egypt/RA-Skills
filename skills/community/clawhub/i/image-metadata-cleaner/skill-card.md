## Description:

Clean privacy-sensitive metadata (C2PA, EXIF, XMP, IPTC, GPS) from user-owned images by writing sanitized copies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiwork4me](https://clawhub.ai/user/aiwork4me)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content creators, and privacy-conscious users use this skill to prepare user-owned or authorized images for sharing by removing file-level metadata and writing sanitized copies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional manifest path can overwrite another writable file without the same confirmation protections promised for image outputs.

Mitigation: Use dry-run first, avoid custom --manifest paths unless the destination is trusted, and choose a new output directory or inspect the path before writing.

Risk: Processing untrusted image files exercises local image parsing code.

Mitigation: Do not run the skill on untrusted images in a privileged environment, and prefer a pinned or locked Pillow installation.

Risk: The verification scan is a quality check, not proof that every possible provenance signal, watermark, or external platform record was removed.

Mitigation: Treat scan results as limited file-level evidence and do not use the skill to hide authorship, evade provenance checks, bypass platform labels, or misrepresent image origin.

## Reference(s):

- [Technical Reference](references/technical-details.md)
- [Image Metadata Cleaner on ClawHub](https://clawhub.ai/aiwork4me/skills/image-metadata-cleaner)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files, JSON]

**Output Format:** [Markdown guidance with inline shell commands; sanitized image files and optional JSON manifest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes copies instead of modifying originals, reports processed files, output locations, file sizes, dimensions, and residual metadata or provenance markers.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
