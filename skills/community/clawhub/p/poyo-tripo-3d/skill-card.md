## Description:

Tripo3D asset generation on PoYo via the Tripo H3.1 and P1 text-to-3D, image-to-3D, and multiview-to-3D API workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and asset pipeline engineers use this skill to plan or submit PoYo Tripo3D generation jobs, choose the appropriate model, prepare payloads, and handle follow-up polling or webhook workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a PoYo API key and can submit live 3D generation requests.

Mitigation: Keep POYO_API_KEY in a server-side environment or secret manager and make live submissions only after the user explicitly chooses to run them.

Risk: Prompts, source image URLs, generated asset URLs, and callback URLs may contain confidential or proprietary information.

Mitigation: Avoid sending sensitive inputs unless the user trusts PoYo and the callback receiver, and avoid logging secrets or private asset data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-tripo-3d)
- [PoYo Tripo H3.1 Model Page](https://poyo.ai/models/tripo-h31-3d)
- [PoYo Tripo H3.1 API Documentation](https://docs.poyo.ai/api-manual/3d-series/tripo-h31-3d)
- [PoYo Tripo P1 API Documentation](https://docs.poyo.ai/api-manual/3d-series/tripo-p1-3d)
- [API Reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and bash/curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected model id, request type, payload summary, mesh and texture settings, source-image notes, returned task_id, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
