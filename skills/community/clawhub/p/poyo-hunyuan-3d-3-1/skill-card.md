## Description:

Hunyuan 3D v3.1 asset generation on PoYo via the PoYo submit API for text-to-3D and image-to-3D workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and 3D asset pipeline engineers use this skill to prepare PoYo Hunyuan 3D v3.1 text-to-3D or image-to-3D submissions, choose Pro or Rapid model IDs, handle payload options, and plan polling or webhook follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill submits prompts, image URLs, callback URLs, and generation options to PoYo over the network.

Mitigation: Use it only for intended PoYo Hunyuan 3D generation workflows and review payload JSON before submission.

Risk: POYO_API_KEY is required for live submissions and could be exposed if placed in client-side code, logs, repositories, screenshots, or chat output.

Mitigation: Store POYO_API_KEY only in a server-side environment variable or backend secret manager and avoid echoing it in generated examples.

Risk: Prompts, private image URLs, generated asset URLs, and callback URLs may contain confidential project information.

Mitigation: Do not submit confidential inputs or private callback URLs unless the user trusts PoYo and the receiving endpoint.

## Reference(s):

- [PoYo Hunyuan 3D v3.1 API Reference](references/api.md)
- [PoYo Hunyuan 3D 3.1 model page](https://poyo.ai/models/hunyuan-3d-3-1)
- [PoYo Hunyuan 3D 3.1 API docs](https://docs.poyo.ai/api-manual/3d-series/hunyuan-3d-3-1)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-hunyuan-3d-3-1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON payload examples and bash or curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a PoYo task_id when the user explicitly requests a live submission from a trusted shell.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
