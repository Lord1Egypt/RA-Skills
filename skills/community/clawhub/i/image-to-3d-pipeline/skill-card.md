## Description:

Converts product images into 3D model generation workflow guidance covering image preprocessing, optional enhancement, Tripo3D generation, and GLB/OBJ/USDZ outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m15010495895-sudo](https://clawhub.ai/user/m15010495895-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide image-to-3D asset generation pipelines for product imagery, including preprocessing, provider API calls, polling, error handling, and output format selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider ambiguity and under-disclosed Meshy examples may route requests to an unintended paid service.

Mitigation: Confirm the intended 3D provider before use, configure only the selected provider's credentials, and remove or disable snippets for providers that are not in scope.

Risk: Polling and batch examples can create unbounded paid API calls.

Mitigation: Add timeouts, retry limits, batch-size limits, cancellation handling, and cost monitoring before running the examples at scale.

Risk: Image uploads may expose sensitive or unauthorized product imagery to external services.

Mitigation: Use only non-sensitive images that the user is allowed to upload and review provider terms before sending images to third-party APIs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/m15010495895-sudo/skills/image-to-3d-pipeline)
- [Replicate TripoSR Model](https://replicate.com/baaas/triposr)
- [remove.bg API](https://www.remove.bg/api)
- [Upscale API](https://upscale.ai/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces procedural guidance and command examples; generated 3D assets are created by configured external providers.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
