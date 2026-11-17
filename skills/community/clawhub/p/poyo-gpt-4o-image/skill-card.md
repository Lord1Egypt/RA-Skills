## Description:

Use PoYo AI GPT-4o Image to prepare payloads, submit image generation or image editing jobs, and track task status through the PoYo API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to choose a PoYo GPT-4o Image model, build a valid request payload, submit it with a PoYo API key, and preserve the returned task ID for polling or webhook follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and request payloads can be exposed locally when supplied through command arguments or process-visible curl data.

Mitigation: Use POYO_API_KEY from the environment, avoid typing secrets as command arguments, and prefer submission paths that keep credentials and payloads out of process listings.

Risk: Prompts, reference image URLs, and callback URLs are sent to a third-party PoYo service.

Mitigation: Avoid submitting sensitive prompts, private or internal URLs, proprietary source images, or confidential webhook endpoints unless the user has approved that disclosure.

Risk: The security scan verdict is suspicious because the helper script handles API keys and request data in a locally exposable way.

Mitigation: Review the helper script before installation or execution and use safer credential and payload handling for production workflows.

## Reference(s):

- [PoYo GPT-4o Image model page](https://poyo.ai/models/gpt-4o-image-api)
- [PoYo GPT-4o Image API docs](https://docs.poyo.ai/api-manual/image-series/gpt-4o-image)
- [PoYo GPT-4o Image OpenAPI JSON](https://docs.poyo.ai/api-manual/image-series/gpt-4o-image.json)
- [PoYo task status docs](https://docs.poyo.ai/api-manual/task-management/status)
- [Bundled API reference](artifact/references/api.md)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-gpt-4o-image)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads, curl examples, and task-status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a chosen model ID, payload summary, reference-image status, returned task_id, and the next polling or webhook step.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
