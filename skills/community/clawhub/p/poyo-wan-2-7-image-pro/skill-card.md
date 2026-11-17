## Description:

Wan 2.7 Image Pro generation and editing on PoYo via the PoYo async generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare Wan 2.7 Image Pro text-to-image or image-editing payloads, submit jobs to PoYo, and guide polling or webhook follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API credentials can be exposed if POYO_API_KEY is placed in client code, logs, public repositories, screenshots, or chat output.

Mitigation: Keep POYO_API_KEY in a server-side environment variable or backend secret manager and avoid logging or displaying it.

Risk: Submitted prompts, source image URLs, and callback URLs are sent to PoYo when the submit workflow runs.

Mitigation: Submit only content the user is willing to share with PoYo and use trusted callback receivers for webhook workflows.

Risk: The bundled submit script can make live external API calls.

Mitigation: Run it only from a trusted shell after the user explicitly requests submission and provides a prepared payload.

## Reference(s):

- [PoYo Wan 2.7 Image model page](https://poyo.ai/models/wan-2-7-image)
- [PoYo Wan 2.7 Image Pro API docs](https://docs.poyo.ai/api-manual/image-series/wan-2-7-image-pro)
- [PoYo API key page](https://poyo.ai/dashboard/api-key)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-wan-2-7-image-pro)
- [Local API reference](references/api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with JSON payload examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model selection, request type, payload details, image count, reference-image use, returned task_id, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
