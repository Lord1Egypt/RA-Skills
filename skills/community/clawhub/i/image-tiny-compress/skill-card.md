## Description:

Compress PNG, JPEG, and WebP images using the TinyPNG/Tinify free web endpoint with support for single files, batches, directories, retries, and rate-limit handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aga-j](https://clawhub.ai/user/aga-j)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to compress PNG, JPEG, and WebP assets through an agent workflow for file-size reduction before publishing or sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images are uploaded to TinyPNG/Tinify through an unofficial web endpoint.

Mitigation: Do not use the skill for sensitive, personal, confidential, or proprietary images; use the official TinyPNG API or a local compressor for controlled environments.

Risk: Overwrite mode can replace original files with downloaded compressed content.

Mitigation: Prefer separate output files or an output directory, and use overwrite only after explicit confirmation and backup.

Risk: The unofficial endpoint and spoofed request headers may change, fail, or trigger rate limits.

Mitigation: Keep request volume low, review failures before retrying large batches, and prefer the official API for heavy or production batch processing.

## Reference(s):

- [TinyPNG](https://tinypng.com)

## Skill Output:

**Output Type(s):** [Shell commands, Files, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and per-image JSON result data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces compressed image files and reports output paths, original size, compressed size, saved bytes, and saved percent.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
