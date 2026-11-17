## Description:

Image-to-video generation on RunComfy that helps an agent turn still images into short video clips through the RunComfy Model API, including general animation, lip-sync, and multi-modal image-to-video routes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and agent users use this skill to classify image-to-video requests, choose the appropriate RunComfy model route, and produce CLI commands and JSON inputs for generating short video clips from still images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image, video, audio URLs and prompts are sent to a third-party RunComfy service.

Mitigation: Use only with content that may be processed by RunComfy, review privacy requirements, and avoid submitting sensitive media unless approved.

Risk: The skill requires a local RunComfy CLI installation and account token.

Mitigation: Use a pinned or reviewed CLI version, avoid elevated-privilege installs, and use a revocable RunComfy token such as RUNCOMFY_TOKEN for CI.

Risk: Ambiguous user requests may choose the wrong video generation route.

Mitigation: Confirm unclear requests before invoking the skill, especially when lip-sync, reference audio, or multi-modal inputs may be involved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/permew/skills/image-to-video-runcomfy)
- [RunComfy](https://www.runcomfy.com)
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=image-to-video-runcomfy)
- [RunComfy image-to-video models](https://www.runcomfy.com/models?utm_source=clawhub&utm_medium=skill&utm_campaign=image-to-video-runcomfy)
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=image-to-video-runcomfy)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline bash commands and JSON inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces RunComfy CLI invocations and request bodies; generated media is downloaded by the RunComfy CLI to the selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
