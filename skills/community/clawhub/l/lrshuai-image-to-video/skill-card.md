## Description:

Generates videos from an input image and text prompt through supported remote video-generation models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrshu](https://clawhub.ai/user/lrshu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to submit image-and-text video generation jobs to supported hosted models through a Python command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-provided media and prompts to a remote API for generation.

Mitigation: Use only non-sensitive media and prompts, and disclose remote upload behavior before use.

Risk: TEAM_BASE_URL can change the API destination.

Mitigation: Set TEAM_BASE_URL only for trusted HTTPS endpoints and keep TEAM_API_KEY narrowly scoped.

Risk: The skill attempts to force direct script execution outside the managed runner.

Mitigation: Review execution posture before installing and prefer managed execution controls where available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lrshu/skills/lrshuai-image-to-video)
- [Publisher profile: lrshu](https://clawhub.ai/user/lrshu)
- [Default Team AI API endpoint](https://dlazy.com/api/ai/tool)

## Skill Output:

**Output Type(s):** [text, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TEAM_API_KEY; local media may be encoded into request payloads or remote media URLs may be passed through.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
