## Description:

在本地工作区审阅素材、确认故事，并按章节交付同步分镜与 HTML 选材页，再按题材剪辑 Vlog。

This skill is ready for commercial/non-commercial use.

## Publisher:

[milanor1970](https://clawhub.ai/user/milanor1970)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要在本地素材工作区制作或修订 Vlog 的创作者，帮助他们审阅素材、确认故事、交付同步分镜与 HTML 选材页，并完成剪辑和交付检查。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Story-derived prompts may expose personal details when sent to an image-generation service.

Mitigation: Check whether the service is local or external and share only the prompt details needed for the requested image.

Risk: Media processing may run without a time limit.

Mitigation: Set an execution timeout and treat interrupted or incomplete checks as unfinished until the affected media is reviewed.

Risk: Dependency versions are unpinned, and the available security analysis is partial.

Mitigation: Review and pin dependencies for the deployment environment; do not treat the available analysis as establishing that the artifact is safe.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/milanor1970/skills/local-vlog-production)
- [Publisher profile](https://clawhub.ai/user/milanor1970)
- [Storyboard and selection workflow](artifact/references/storyboard-review.md)
- [First-run guide](artifact/references/first-run.md)
- [Validation guide](artifact/references/validation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, JSON, Code, Video, Images, Guidance]

**Output Format:** [Markdown, HTML, JSON, and media files such as video and images]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project-specific files and reports; deliverables depend on the supplied footage and confirmed story.]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
