## Description:

通过 liblib.tv 生成 AI 图片/视频

This skill is ready for commercial/non-commercial use.

## Publisher:

[lg0219](https://clawhub.ai/user/lg0219)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and creators use this skill to generate and edit AI images and videos through LibLib.tv workflows, including text-to-image, image-to-image, text-to-video, image-to-video, animation, and download/status operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation depends on an unpinned global npm package that was not included for review.

Mitigation: Install in an isolated environment, prefer a pinned package version, and confirm the npm package is the intended publisher before use.

Risk: The external CLI and LibLib.tv service may handle login tokens and uploaded image or video content.

Mitigation: Avoid elevated privileges, protect account tokens, and review what media is uploaded to the external service.

## Reference(s):

- [LibLib.tv](https://www.liblib.tv)
- [LibLib.tv API Documentation](https://www.liblib.tv/docs/api)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and API endpoint descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides use of an external CLI and service for generated image and video assets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
