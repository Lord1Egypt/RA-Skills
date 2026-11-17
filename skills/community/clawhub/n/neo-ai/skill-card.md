## Description:

Generate images and videos via the Neodomain AI API, including text-to-image, image-to-video, text-to-video, universal multi-modal video, motion control video, and batch storyboard video workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bandwhite](https://clawhub.ai/user/bandwhite)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and content creators use this skill to select Neodomain models, authenticate with NEODOMAIN_ACCESS_TOKEN, and run image or video generation workflows from prompts, reference media, motion-control inputs, or storyboard frames.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference media, generated outputs, and selected storyboard images may be sent to Neodomain or OSS.

Mitigation: Use the skill only with content approved for external processing, and avoid sensitive local paths when uploading or batch-processing files.

Risk: Access tokens and verification codes can be exposed when passed directly on command lines or stored in long-lived shell startup files.

Mitigation: Prefer environment-scoped token handling, avoid command-line secrets where possible, and rotate or revoke tokens after use.

Risk: Python scripts call external services and may require additional dependencies such as oss2.

Mitigation: Review scripts before execution, use pinned dependencies, and run them in an isolated virtual environment.

## Reference(s):

- [neo-ai Skill Page](https://clawhub.ai/bandwhite/skills/neo-ai)
- [Publisher Profile: bandwhite](https://clawhub.ai/user/bandwhite)
- [Neodomain Image Generation Models Endpoint](https://story.neodomain.cn/agent/ai-image-generation/models)
- [SKILL.md](artifact/SKILL.md)
- [INSTALL.md](artifact/INSTALL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline bash commands; generated media files and metadata JSON when scripts run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts write image files, video files, thumbnails, and metadata.json to the configured output directory.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
