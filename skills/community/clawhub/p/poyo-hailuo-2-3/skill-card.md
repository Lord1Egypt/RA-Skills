## Description:

Hailuo 2.3 video generation on PoYo via the PoYo async generation API, including prompt-only and optional first-frame guided workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare, submit, and follow up on PoYo Hailuo 2.3 text-to-video or first-frame guided video generation jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, source image URLs, callback URLs, and generated task metadata may be sent to PoYo during use.

Mitigation: Use the skill only when the user accepts PoYo processing, and avoid submitting confidential prompts, private source images, or sensitive callback URLs unless the receiving systems are trusted.

Risk: The required POYO_API_KEY could be exposed if placed in client-side code, logs, screenshots, public repositories, or chat output.

Mitigation: Keep POYO_API_KEY in a server-side environment variable or secret manager and avoid echoing or logging it.

Risk: The submit helper sends the contents of a local payload file to the PoYo generation endpoint.

Mitigation: Run the script only with payload files that were intentionally prepared and reviewed for submission.

## Reference(s):

- [PoYo Hailuo 2.3 model page](https://poyo.ai/models/hailuo-2-3)
- [PoYo Hailuo 2.3 API documentation](https://docs.poyo.ai/api-manual/video-series/hailuo-2-3)
- [PoYo API key dashboard](https://poyo.ai/dashboard/api-key)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-hailuo-2-3)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with JSON payloads and curl commands when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model id, payload summary, duration, resolution, prompt optimizer setting, task_id, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
