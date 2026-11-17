## Description:

hal-image helps agents inspect, transform, combine, watermark, convert, and losslessly compress images with local ImageMagick and oxipng commands before delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ofoxai](https://clawhub.ai/user/ofoxai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill when an agent needs to inspect, resize, crop, rotate, convert, combine, watermark, or compress image files before reading or sending them. It is intended for local image-handling workflows where smaller, losslessly compressed outputs reduce transfer size and token use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some image-processing and compression examples modify files in place.

Mitigation: Run commands on deliberate copies or staged outputs when preserving the original file matters.

Risk: The fail-open rule may send an original image unchanged when compression tooling is missing or errors.

Mitigation: Confirm required tools are installed and inspect file size or metadata before sending sensitive or large images.

Risk: Watermarking and annotation can fail when a usable system font is unavailable.

Mitigation: Specify an explicit font path and skip the annotation step if no suitable font is found.

## Reference(s):

- [hal-image recipes](references/recipes.md)
- [Project homepage](https://github.com/ofoxai/skills/tree/main/skills/hal-image)
- [ClawHub skill page](https://clawhub.ai/ofoxai/skills/hal-image)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may read image metadata, write transformed image files, and perform fail-open compression before delivery.]

## Skill Version(s):

1.1.0 (source: server release evidence, target metadata, frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
