## Description:

Guides an agent to generate a short video clip from text, images, or imported audio using Pruna's p-video-2 model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pruna-ai](https://clawhub.ai/user/pruna-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to direct an agent in making one short video clip from a prompt, optional start/end frames, and optional imported audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and supplied image or audio files are uploaded to Pruna's hosted API.

Mitigation: Only submit media and prompts approved for upload to Pruna.

Risk: Companion skills are installed through npx commands, and API access uses PRUNA_API_KEY.

Mitigation: Review companion skills before installing, pin versions where possible, and keep the API key in a controlled environment variable.

## Reference(s):

- [p-video-2 on ClawHub](https://clawhub.ai/pruna-ai/skills/p-video-2)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with video prompts and optional curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides one prediction per invocation; the hosted service returns a video clip.]

## Skill Version(s):

1.0.15 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
