## Description:

Helps agents prepare and submit PoYo Meshy 6 text-to-3D, image-to-3D, and multi-image-to-3D generation requests, then guide polling or webhook follow-up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and asset pipeline engineers use this skill to choose a Meshy 6 workflow, assemble PoYo API payloads, submit prepared 3D generation jobs, and track follow-up through polling or webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the submit helper sends prompts, source image URLs, callback URLs, and PoYo API key authorization to PoYo.

Mitigation: Keep POYO_API_KEY server-side, avoid private image URLs unless intended, and run live submissions only when ready for provider-side processing or costs.

Risk: Generated task details and asset URLs may expose private project information if logged or shared.

Mitigation: Avoid logging API keys, private prompts, source image URLs, generated asset URLs, and callback URLs; store final asset URLs only after successful completion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-meshy-6-3d)
- [PoYo Meshy 6 3D model page](https://poyo.ai/models/meshy-6-3d)
- [PoYo Meshy 6 3D API docs](https://docs.poyo.ai/api-manual/3d-series/meshy-6-3d)
- [PoYo examples repository](https://github.com/PoyoAPI/poyo-examples)
- [API reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payload summaries and bash/curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include the chosen model id, request payload, task_id, polling or webhook next steps; live submissions only when explicitly requested.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
