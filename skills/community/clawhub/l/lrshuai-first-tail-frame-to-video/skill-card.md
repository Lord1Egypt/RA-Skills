## Description:

Generates video from first-frame and tail-frame images, using a text prompt and a selected supported video model to control the starting and ending visuals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrshu](https://clawhub.ai/user/lrshu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to call a remote video-generation API with a prompt plus first and tail frame images when they need a video whose opening and closing frames are constrained.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local frame images or videos to a remote API.

Mitigation: Use only non-sensitive media files and confirm the configured remote endpoint before execution.

Risk: The skill depends on TEAM_API_KEY and optionally TEAM_BASE_URL for remote API access.

Mitigation: Store credentials outside prompts and allow only trusted TEAM_BASE_URL values.

Risk: The polling loop can continue without a fixed timeout while waiting for generation status.

Mitigation: Run with supervision or add a timeout before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lrshu/skills/lrshuai-first-tail-frame-to-video)
- [Publisher profile](https://clawhub.ai/user/lrshu)
- [Configured remote API endpoint](https://dlazy.com/api/ai/tool)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Terminal text and JSON returned by the remote API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TEAM_API_KEY and may use TEAM_BASE_URL to select the remote service endpoint.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
