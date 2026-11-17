## Description:

Runs web research and orchestrates image/video/3D generation, logo and product visuals, upload, and Markdown reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[typisin](https://clawhub.ai/user/typisin)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, marketers, and content production teams use this skill to combine web research with generated images, video, 3D assets, product visuals, uploads, and a final Markdown delivery report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Upload handling can transmit any readable local file path to remote storage, which is broader than the skill's stated asset-upload purpose.

Mitigation: Invoke upload only for files the user explicitly selected, avoid arbitrary local paths, and prefer runtime restrictions to session or generated asset directories.

Risk: Network calls and generation stages require OPENCLOW_KEY and remote Gateway access.

Mitigation: Keep OPENCLOW_KEY in environment variables, stop at precheck when it is missing, and avoid enabling request logging except for temporary debugging.

Risk: Upload policy endpoints and returned links can affect where assets are sent and distributed.

Mitigation: Use HTTPS upload endpoints, enforce the configured allowlist, validate image content and size, and verify returned URLs before including them in reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/typisin/skills/hopola)
- [README.en.md](README.en.md)
- [examples.md](examples.md)
- [Hopola Gateway](https://hopola.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with structured errors, generated asset links, and optional shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include links to generated images, videos, 3D assets, uploaded files, and stage-level status details.]

## Skill Version(s):

1.0.9 (source: server release evidence and VERSION.txt)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
