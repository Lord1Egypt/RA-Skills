## Description:

Portada animada para un carrusel de Instagram: genera o toma una foto gancho con la cara de la usuaria en Higgsfield, la anima como cinemagraph de cámara fija de 5 segundos sin audio y renderiza el título como PNG transparente con Chromium.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators and social media operators use this skill to create an animated first slide for Instagram carousels. It guides an agent through collecting or generating a cover image, animating it with Higgsfield, exporting a transparent title overlay, and handing off assets for final composition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may use local or Telegram-provided selfies and upload them to Higgsfield.

Mitigation: Confirm user consent and suitability before using selfies or external media-generation services.

Risk: The workflow depends on npm package installation, Chromium with --no-sandbox, Google Fonts access, and Higgsfield credits.

Mitigation: Run it only in an environment where those runtime requirements and service costs are acceptable.

Risk: Video generation can consume credits and may produce unsuitable results if the source image is poor.

Mitigation: Show the generated cover image to the user and wait for approval before starting the paid animation step.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/portada-video-carrusel-formula100k)
- [Plantilla del título de portada](references/plantilla-overlay.md)
- [Recetas Higgsfield](references/recetas-higgsfield.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files]

**Output Format:** [Markdown instructions with inline shell commands, HTML/CSS templates, and generated media asset paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or points to cover_anim_raw.mp4, title-overlay.png, slide-01.png, and the final slide-01-ANIMADO.mp4 when composition is completed.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
