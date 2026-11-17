## Description:

Happy Horse 1.1 video generation on PoYo via its generation API for text-to-video, image-to-video, and reference-to-video workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare PoYo Happy Horse 1.1 video-generation payloads, submit trusted payloads from a shell when requested, and guide polling or webhook follow-up for generated video tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a PoYo API key and may submit prompts, image URLs, reference images, and callback URLs to PoYo.

Mitigation: Keep POYO_API_KEY in a server-side environment or secret manager, avoid logging secrets, and submit private prompts, media URLs, or callback URLs only when the user trusts PoYo and the callback receiver.

Risk: The bundled shell script can make a live PoYo API request with a prepared payload.

Mitigation: Review the payload JSON before execution and run the script only from a trusted shell when the user explicitly wants submission.

## Reference(s):

- [PoYo Happy Horse 1.1 model page](https://poyo.ai/models/happy-horse-1-1)
- [PoYo Happy Horse 1.1 API docs](https://docs.poyo.ai/api-manual/video-series/happy-horse-1-1)
- [PoYo API key page](https://poyo.ai/dashboard/api-key)
- [Local API reference](references/api.md)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-happy-horse-1-1)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with JSON payload examples and inline bash or curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a selected model id, workflow type, payload summary, task_id from submitted requests, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
