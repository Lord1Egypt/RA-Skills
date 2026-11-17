## Description:

Guides agents in creating a single short video clip from text or images using Pruna's p-video model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pruna-ai](https://clawhub.ai/user/pruna-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to guide a single quick B-roll, draft, or frame-anchored clip through Pruna's video generation service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prerequisite skills are offered through unpinned remote install commands.

Mitigation: Review install commands, use trusted or pinned versions, and do not run installations unattended.

Risk: The guidance conflicts about when audio, 1080p, and draft modes belong in p-video rather than p-video-2.

Mitigation: Confirm the intended model before requesting imported audio, 1080p output, or draft previews.

Risk: Uploaded images or audio may contain sensitive content.

Mitigation: Only upload media approved for transfer to Pruna's API.

## Reference(s):

- [p-video on ClawHub](https://clawhub.ai/pruna-ai/skills/p-video)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides one video-generation request per invocation; resulting media is returned by the external service.]

## Skill Version(s):

1.0.15 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
