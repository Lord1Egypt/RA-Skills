## Description: <br>
Generate deterministic 6-slide portrait PNG slideshow assets plus caption text for TikTok-style posting workflows, including reusable templates and a strict validation pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JK-Archivist](https://clawhub.ai/user/JK-Archivist) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and social content operators use this skill to generate six-slide portrait PNG slideshow packs, captions, review artifacts, and optional Postiz draft uploads for TikTok-style workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Postiz mode sends rendered slides and captions to the configured Postiz API using account credentials and may create draft or private social posting artifacts. <br>
Mitigation: Run local-only by omitting --postiz or using --no-upload; review generated slides and captions before enabling upload. <br>
Risk: Generated slide or caption copy may be unsuitable for the intended TikTok workflow if the input spec or topic is inaccurate. <br>
Mitigation: Use the preflight checks and review artifacts, then manually review the slides and caption before publication. <br>


## Reference(s): <br>
- [TikTok Packager ClawHub Page](https://clawhub.ai/JK-Archivist/jk-archivist-tiktok-packager) <br>
- [Setup](references/setup.md) <br>
- [Spec Schema](references/spec-schema.md) <br>
- [Renderer Spec](references/renderer-spec.md) <br>
- [Outputs and Validation](references/outputs-and-validation.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Architecture](docs/ARCHITECTURE.md) <br>
- [Postiz Tool Notes](tools/postiz.tool.md) <br>
- [TikTok Render Tool Notes](tools/tiktok_render.tool.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Markdown, JSON, Shell commands, Configuration instructions, API Calls] <br>
**Output Format:** [PNG images, plain-text captions, JSON metadata and logs, Markdown review artifacts, and optional Postiz draft API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exactly six 1024x1536 portrait slides; optional Postiz upload uses account credentials and can be disabled by omitting --postiz or using --no-upload.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release metadata; artifact package.json and CHANGELOG report 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
