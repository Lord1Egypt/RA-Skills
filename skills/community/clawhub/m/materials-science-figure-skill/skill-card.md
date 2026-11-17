## Description:

Use when the user wants to generate or edit images with Google's Nanobanana/Gemini image models using the official Gemini API shape, or when they need publication-style scientific figures rendered exactly from data with the bundled Python plotting tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grenzlinie](https://clawhub.ai/user/grenzlinie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical authors use this skill to create publication-style materials-science schematics, graphical abstracts, image edits, and exact matplotlib-based plots from numeric data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image generation can send prompt text, selected image files, and the configured API key to Google or another allowed endpoint.

Mitigation: Use the official Google endpoint by default, confirm any third-party endpoint before use, and avoid sending sensitive inputs unless the endpoint is trusted.

Risk: API keys may be exposed if passed directly on the command line.

Mitigation: Store credentials in an API-key file or environment variable and avoid inline command-line secrets.

Risk: The plotting script uses a fixed temporary cache path, which can matter on shared machines.

Mitigation: Run plotting workflows in a trusted workspace and review local file handling before shared or multi-user deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/grenzlinie/skills/materials-science-figure-skill)
- [Project Homepage](https://github.com/siyuliu/materials-science-figure-skill)
- [API Reference](references/api-reference.md)
- [Materials Science Figure Template](references/materials-science-figure-template.md)
- [Natural-Language Plot Workflow](references/natural-language-plot-workflow.md)
- [Publication Figure Design](references/publication-figure-design.md)
- [Publication Plot API](references/publication-plot-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, JSON plot specifications, and generated image or plot files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image mode can send prompts, selected image files, and credentials to the configured Gemini-compatible endpoint; plot mode produces local PNG, PDF, or SVG files.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
