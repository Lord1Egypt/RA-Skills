## Description:

Generates images from text prompts using the configured Team AI model endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrshu](https://clawhub.ai/user/lrshu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to invoke supported text-to-image models and return generated image task results from a configured API service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send TEAM_API_KEY to a configurable API endpoint.

Mitigation: Install only when the publisher and endpoint are trusted, and pin or verify TEAM_BASE_URL before use.

Risk: Prompt text and supplied image or video paths may be uploaded as request data.

Mitigation: Avoid sensitive prompts and local media files; review file paths before invoking the skill.

Risk: The skill directs the agent to run local Python directly instead of the normal OpenClaw runner.

Mitigation: Prefer a release that uses the normal runner with explicit upload consent and endpoint validation, or review the command before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lrshu/skills/lrshuai-text-to-image)
- [Publisher profile](https://clawhub.ai/user/lrshu)

## Skill Output:

**Output Type(s):** [text, shell commands, API calls, JSON]

**Output Format:** [Console text with JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python and TEAM_API_KEY; may submit asynchronous generation jobs and poll until completion.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
