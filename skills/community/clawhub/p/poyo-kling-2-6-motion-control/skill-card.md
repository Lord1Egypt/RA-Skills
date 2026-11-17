## Description:

Helps agents submit PoYo Kling 2.6 Motion Control video-generation jobs for motion transfer using a character image, reference video, orientation mode, and output resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to prepare and submit PoYo Kling 2.6 Motion Control jobs when they need to animate a supplied character image from a supplied motion-reference video. The skill helps produce payload guidance, shell commands, and follow-up details such as the returned task_id.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill submits image, video, prompt, and optional callback URL values to PoYo as part of generation requests.

Mitigation: Review media URLs and callback_url values before submission, and use the skill only when sending those assets to PoYo is intended.

Risk: The skill requires a PoYo API key for authenticated requests.

Mitigation: Set POYO_API_KEY in a protected environment and avoid passing credentials on the command line or embedding secrets in payload files.

## Reference(s):

- [PoYo Kling 2.6 Motion Control Model Page](https://poyo.ai/models/kling-2-6-motion-control)
- [PoYo Kling 2.6 Motion Control API Docs](https://docs.poyo.ai/api-manual/video-series/kling-2.6-motion-control)
- [PoYo Kling 2.6 Motion Control OpenAPI JSON](https://docs.poyo.ai/api-manual/video-series/kling-2.6-motion-control.json)
- [PoYo Task Status Docs](https://docs.poyo.ai/api-manual/task-management/status)
- [PoYo API Key Page](https://poyo.ai/dashboard/api-key)
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-kling-2-6-motion-control)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON payloads and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include the selected model id, payload summary, reference-media usage, returned task_id, and next polling or webhook step.]

## Skill Version(s):

1.0.1 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
