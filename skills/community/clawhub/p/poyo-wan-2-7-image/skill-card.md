## Description:

Helps agents prepare and submit Wan 2.7 text-to-image and image-editing requests to PoYo, including payload construction, curl submission, polling, and webhook follow-up guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate PoYo Wan 2.7 image payloads, submit trusted requests with a server-side API key, and plan polling or webhook handling for generated images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API keys, prompts, source image URLs, or callback URLs could expose sensitive information if logged, shared, or submitted to an untrusted environment.

Mitigation: Treat POYO_API_KEY as a secret, keep it in server-side environment variables or a secret manager, review payload JSON before submission, and avoid confidential prompts, private images, or private callback URLs unless PoYo and the callback receiver are trusted.

Risk: Live submissions send chosen payloads to PoYo and may start asynchronous image-generation tasks.

Mitigation: Make live API calls only after the user explicitly requests submission from a trusted shell and confirms the payload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-wan-2-7-image)
- [PoYo Wan 2.7 Image model page](https://poyo.ai/models/wan-2-7-image)
- [PoYo Wan 2.7 Image API docs](https://docs.poyo.ai/api-manual/image-series/wan-2-7-image)
- [API reference](references/api.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with JSON payloads and bash curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model id, request mode, selected size, image count, reference-image use, task_id after submission, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
