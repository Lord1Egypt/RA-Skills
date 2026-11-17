## Description:

Compress PNG, JPEG, WebP images using TinyPNG/Tinify free web API. No API key required, no login needed. Supports single/batch/directory compression with automatic retry and rate-limit handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aga-j](https://clawhub.ai/user/aga-j)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to compress PNG, JPEG, and WebP image files through TinyPNG/Tinify for smaller image assets, batch outputs, or directory-level optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images are uploaded to third-party TinyPNG/Tinify servers for compression.

Mitigation: Avoid sensitive, personal, or regulated images unless the user has approved third-party processing.

Risk: Overwrite mode can replace original image files irreversibly.

Mitigation: Prefer suffix or output-directory mode, and use overwrite only after confirming backups or user intent.

Risk: Security evidence flags file and network safety gaps, including download URL validation and dependency pinning.

Mitigation: Run with limited filesystem and network access until URL validation, overwrite confirmation, and pinned dependencies are added.

## Reference(s):

- [TinyPNG](https://tinypng.com)
- [ClawHub skill page](https://clawhub.ai/aga-j/skills/imgae-compress)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Guidance]

**Output Format:** [Compressed image files with console status and optional JSON result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-file, batch, and directory compression; default output uses a _compressed filename suffix unless overwrite mode is selected.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
