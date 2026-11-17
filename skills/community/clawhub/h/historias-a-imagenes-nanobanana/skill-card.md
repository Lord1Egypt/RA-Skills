## Description:

Converts Instagram Stories scripts into finished 9:16 PNG story images using Gemini/Nano Banana by default, with Higgsfield as an optional alternative, and selects user-provided brand photos as visual inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and agents use this skill to turn a structured Instagram Stories script into ready-to-upload visual story assets. It parses the script, matches brand photos, builds image prompts, selects an image-generation engine, and returns generated PNGs with run metadata and regeneration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can send selected personal brand photos to Gemini or Higgsfield for image generation.

Mitigation: Use a dedicated curated photo folder and exclude unrelated private images before running the skill.

Risk: Generated images, prompts, run metadata, and photo-folder presets may remain on disk after use.

Mitigation: Periodically delete old files in `entregables/historias/` and remove `cerebro/preset-historias.json` when retained paths are no longer needed.

Risk: Image generation can incur external service costs.

Mitigation: Review the estimated cost confirmation before generation and prefer the default economical engine unless a premium visual style is required.

Risk: If a slide requires the user's face but no matching base photo is provided, generated output may not represent the intended person.

Mitigation: Require a matching user-provided photo for face-based slides and ask the user for a suitable photo when the folder is empty or no match is available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/historias-a-imagenes-nanobanana)
- [Parser del guion](artifact/references/parser-guion.md)
- [Sistema de diseno Instagram Stories nativo](artifact/references/instagram-design-system.md)
- [Prompt builder](artifact/references/prompt-builder.md)
- [Foto matcher](artifact/references/foto-matcher.md)
- [Motor selection](artifact/references/motor-selection.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, image files]

**Output Format:** [Markdown guidance with shell commands, JSON metadata, prompts, and generated PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates 9:16 Instagram Story PNGs, optional A/B engine variants, and run metadata under entregables/historias/.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
