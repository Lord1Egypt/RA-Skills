## Description:

Generate deterministic 6-slide portrait PNG slideshow assets plus caption text for TikTok-style posting workflows, including reusable templates and a strict validation pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jk-archivist](https://clawhub.ai/user/jk-archivist)

### License/Terms of Use:


## Use Case:

Developers, creators, and social content operators use this skill to generate deterministic six-slide portrait PNG carousels, captions, review artifacts, and optional Postiz draft uploads for TikTok-style posting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Postiz upload can send generated media, captions, and API credentials to an endpoint controlled by POSTIZ_BASE_URL.

Mitigation: Leave POSTIZ_BASE_URL unset unless you operate or trust the endpoint, use narrowly scoped Postiz credentials, and run without --postiz or with --no-upload unless upload is intended.

Risk: Troubleshooting guidance includes a destructive cleanup command.

Mitigation: Verify cleanup paths before running rm -rf and limit cleanup to generated output or temporary directories.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jk-archivist/skills/jk-archivist-tiktok-packager)
- [Skill Definition](artifact/SKILL.md)
- [README](artifact/README.md)
- [Setup](artifact/references/setup.md)
- [Spec Schema](artifact/references/spec-schema.md)
- [Renderer Spec](artifact/references/renderer-spec.md)
- [Outputs and Validation](artifact/references/outputs-and-validation.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [TikTok Render Tool Notes](artifact/tools/tiktok_render.tool.md)
- [Postiz Tool Notes](artifact/tools/postiz.tool.md)

## Skill Output:

**Output Type(s):** [Files, Text, Markdown, JSON metadata, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with shell commands; generated artifacts include PNG slides, caption text, JSON metadata, logs, and review materials.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs follow a six-slide 1024x1536 portrait contract and can include optional Postiz upload state and response files.]

## Skill Version(s):

1.6.0 (source: server release metadata; artifact package and changelog list 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
