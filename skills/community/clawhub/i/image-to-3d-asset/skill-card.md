## Description:

Turn a photo or a text prompt into a real 3D model: a textured mesh you can drop into a game engine, AR scene, or product viewer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runware](https://clawhub.ai/user/runware)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, artists, and technical content teams use this skill to prepare Runware 3D generation requests that convert reference images or text descriptions into GLB assets for games, AR, product viewers, hero renders, or 3D printing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images, prompts, or file metadata may be processed by Runware or the selected external model provider.

Mitigation: Do not submit sensitive faces, private locations, confidential products, regulated data, or files containing metadata that should not be shared externally.

Risk: Generated meshes may not match the intended topology, polygon budget, material setup, or downstream use case on the first attempt.

Mitigation: Review the returned GLB in the target viewer or engine, then adjust model settings such as mesh mode, quality, polyCount, material, or pose and rerun generation when needed.

## Reference(s):

- [Image-to-3D asset worked recipes](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/runware/skills/image-to-3d-asset)

## Skill Output:

**Output Type(s):** [guidance, JSON, configuration, files]

**Output Format:** [Markdown guidance with JSON request examples and GLB file URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [3D generation is asynchronous; completed assets are GLB files returned at outputs.files[].url.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
