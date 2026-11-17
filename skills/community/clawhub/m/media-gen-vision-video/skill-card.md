## Description:

Generate and analyze images and generate videos using OpenClaw's preferred Google media workflows for image creation, editing, inspection, comparison, description, and video generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielwpp](https://clawhub.ai/user/danielwpp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route image generation, image editing, screenshot or photo analysis, and video generation requests through preferred Google media workflows while preserving media constraints and reporting blockers clearly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The broad trigger may cause the skill to be selected for many image-related tasks.

Mitigation: Use it when Google media workflows are desired, and confirm task fit before following the workflow for unrelated image requests.

Risk: Generated video availability depends on the current runtime and tool access.

Mitigation: Report the blocker clearly and avoid claiming success unless an actual video file was produced.

Risk: Image or screenshot interpretation can be wrong when visual evidence is unclear.

Mitigation: Use multimodal analysis when available, state only visible or strongly supported observations, and separate inference from confirmed details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danielwpp/skills/media-gen-vision-video)
- [Publisher profile](https://clawhub.ai/user/danielwpp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with generated media files when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or attach generated image or video assets when the runtime supports media delivery.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
