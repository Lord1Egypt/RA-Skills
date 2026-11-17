## Description:

Helps agents submit Wan 2.6 text-to-video, image-to-video, and video-to-video generation jobs through PoYo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare and submit PoYo Wan 2.6 video generation requests, choose the appropriate model variant, and report task IDs for follow-up status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, media URLs, and optional callback URLs are sent to PoYo.

Mitigation: Use the skill only when sending that content to PoYo is acceptable, and avoid sensitive prompts, private media URLs, or callback endpoints that should not be shared.

Risk: The helper script can expose the PoYo API key through command and process arguments.

Mitigation: Avoid passing the API key on the command line; prefer safer secret handling or modify the helper so the bearer token is not placed in process arguments.

## Reference(s):

- [PoYo Wan 2 6 API Reference](references/api.md)
- [PoYo Wan 2.6 Model Page](https://poyo.ai/models/wan-2-6)
- [PoYo Wan 2.6 API Docs](https://docs.poyo.ai/api-manual/video-series/wan-2-6)
- [PoYo Wan 2.6 OpenAPI JSON](https://docs.poyo.ai/api-manual/video-series/wan-2-6.json)
- [PoYo Task Status Docs](https://docs.poyo.ai/api-manual/task-management/status)
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-wan-2-6)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected model ID, request payload summary, reference media usage, returned task_id, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
