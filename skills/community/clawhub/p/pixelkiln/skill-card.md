## Description:

Use PixelKiln to plan, generate, review, recover, audit, pack, and export manifest-driven pixel-art projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gfargo](https://clawhub.ai/user/gfargo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use PixelKiln to manage manifest-driven pixel-art projects, including planning generation costs, reviewing and recovering assets, checking quality, and packaging or exporting results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment is benign, but confidence is medium and the evidence is incomplete because some local references could not be resolved.

Mitigation: Review the referenced files and inspect any unresolved material before installing or running workflows that depend on it.

Risk: Reference or style images can be uploaded to PixelLab, which may expose unreleased or confidential artwork; paid generation can also consume provider budget.

Mitigation: Name each image and get consent before uploading it, and obtain an explicit provider-specific budget before paid generation.

## Reference(s):

- [PixelKiln release on ClawHub](https://clawhub.ai/gfargo/skills/pixelkiln)
- [Server-resolved source repository](https://github.com/gfargo/pixelkiln/tree/main/skills/pixelkiln)
- [PixelLab workflows](references/pixellab.md)
- [ComfyUI workflows](references/comfyui.md)
- [Quality checks](references/quality.md)
- [Tiles and export workflows](references/tiles.md)
- [Visual effects workflows](references/vfx.md)
- [Model workflows](references/models.md)
- [Parallax guide](https://pixelkiln.griffen.codes/docs/research-parallax)
- [ComfyUI guide](https://pixelkiln.griffen.codes/docs/comfyui)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration files, Image assets]

**Output Format:** [Markdown guidance and shell commands; manifest and lockfile configuration; pixel-art image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated work follows a project manifest and may include provenance and review records.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
