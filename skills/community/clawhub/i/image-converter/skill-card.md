## Description:

Converts image files between PNG, JPG, WEBP, GIF, BMP, and limited SVG-related workflows, with batch conversion and adjustable quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to ask an agent for local image format conversion guidance, Python code, and batch conversion commands. It is suited to raster conversion workflows where users can review dependency setup and output format tradeoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SVG support is documented but may not be fully implemented by the included raster conversion helper.

Mitigation: Treat the skill as a raster image converter unless SVG handling is verified or real CairoSVG-based conversion is added.

Risk: Installing image-processing dependencies into a shared Python environment can affect other projects.

Mitigation: Install and run the dependencies in a virtual environment or another limited Python environment.

Risk: Converting PNG images with transparency to JPG removes the alpha channel.

Mitigation: Keep the original file or choose PNG/WEBP output when transparency must be preserved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobewin/skills/image-converter)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local file conversion guidance; output quality may be user-configurable.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
