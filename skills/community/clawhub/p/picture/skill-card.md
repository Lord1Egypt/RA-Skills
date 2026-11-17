## Description:

Picture helps agents guide local image-processing work with Pillow, including loading, saving, resizing, cropping, format conversion, enhancements, filters, image stitching, background removal, and text overlays.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgta23](https://clawhub.ai/user/hgta23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate Python image-processing guidance, examples, and commands for common local editing tasks such as resizing, filtering, compositing, removing simple backgrounds, and adding text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save output images to local paths, so an agent may overwrite files if given an existing destination.

Mitigation: Run in a least-privileged workspace and review output paths before writing image files.

Risk: The Pillow dependency is version-ranged, which can reduce reproducibility across environments.

Mitigation: Pin Pillow to a reviewed version when reproducible or higher-assurance installs are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hgta23/skills/picture)
- [README](artifact/README.md)
- [Skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe local file inputs and output image paths; users should review paths before saving files.]

## Skill Version(s):

1.0.0 (source: release evidence, artifact/SKILL.md, artifact/src/p_skill/__init__.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
