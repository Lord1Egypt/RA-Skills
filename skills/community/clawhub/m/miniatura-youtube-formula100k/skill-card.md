## Description:

Generates YouTube thumbnail concepts, prompts, image-generation variants, and optimization guidance using user photos, competitive thumbnail analysis, and the Formula 100K thumbnail methodology.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and channel operators use this skill to plan, generate, refine, and compare YouTube thumbnail variations. It supports both original thumbnail creation and reference-style thumbnail adaptation using the user's own photos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User selfies and reference images may be processed by Gemini or Higgsfield and delivered through Telegram.

Mitigation: Add an explicit consent step before uploads, disclose which providers process images, and document where images are saved and when they are deleted.

Risk: The clone-style workflow may encourage close copying of another creator's recognizable thumbnail style.

Mitigation: Use references for high-level composition and contrast only, avoid direct replication of distinctive branding or creator identity, and ask the user to confirm they have rights to reference material.

Risk: Provider safety filters may block some image-generation requests.

Mitigation: Treat safety-filter blocks as refusals and simplify or redirect the request instead of repeatedly retrying blocked prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/miniatura-youtube-formula100k)
- [MODO CLONAR ESTILO - Higgsfield](artifact/references/clonar-estilo-higgsfield.md)
- [Metodologia de Miniaturas - FORMULA 100K](artifact/references/metodologia-miniaturas.md)
- [9 Estilos de Miniatura + Prompts Base para NanoBanana](artifact/references/estilos-plantillas.md)
- [Configuracion NanoBanana para Miniaturas YouTube](artifact/references/banana-thumbnail-config.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with prompts, command snippets, file paths, and thumbnail recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or reference image files when connected to Gemini, Higgsfield, Telegram, or local image-processing tools.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact metadata version is 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
