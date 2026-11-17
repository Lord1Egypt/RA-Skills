## Description:

Use PoYo AI GPT Image 1.5 to prepare payloads, submit image generation or edit jobs, and track task status through PoYo's image-generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create PoYo-compatible GPT Image 1.5 requests, submit generation or editing jobs, and preserve the returned task ID for polling or webhook follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, callback URLs, and submitted payload data are sent to PoYo.

Mitigation: Install and use the skill only when PoYo is an approved service for the submitted content, and avoid secrets, private internal URLs, regulated data, or sensitive images unless approved.

Risk: API keys can be exposed if passed directly on the command line or included in shared payloads.

Mitigation: Provide POYO_API_KEY through an environment variable or secret manager and keep credentials out of prompts, payload files, logs, and command history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-gpt-image-1-5)
- [PoYo GPT Image 1.5 model page](https://poyo.ai/models/gpt-image-1-5-api)
- [PoYo GPT Image 1.5 API docs](https://docs.poyo.ai/api-manual/image-series/gpt-image-1.5)
- [PoYo GPT Image 1.5 OpenAPI JSON](https://docs.poyo.ai/api-manual/image-series/gpt-image-1.5.json)
- [PoYo task status docs](https://docs.poyo.ai/api-manual/task-management/status)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON payloads, curl examples, shell commands, and concise task-status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected model ID, request payload or parameter summary, reference-image usage, returned task_id, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
