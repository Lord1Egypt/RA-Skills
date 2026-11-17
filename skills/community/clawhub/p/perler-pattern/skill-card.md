## Description:

Perler Pattern converts photos, local images, or image URLs into perler, hama, and fuse bead patterns with offline background removal and printable or viewable outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to transform photos, cartoons, logos, or image URLs into bead-pattern assets for crafting, printing, and assembly planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install Python image-processing libraries during dependency setup.

Mitigation: Review the package installation commands and run the skill in an isolated environment when package provenance matters.

Risk: The skill can fetch user-provided image URLs.

Mitigation: Prefer local image files or trusted public URLs, especially when internal-network request exposure is a concern.

## Reference(s):

- [Palette Reference](artifact/references/palettes.md)
- [Pattern Style Parameters](artifact/references/styles.md)
- [ClawHub Skill Page](https://clawhub.ai/tobewin/skills/perler-pattern)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python and shell code blocks that produce HTML, SVG, PNG, and text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated artifacts include an interactive HTML viewer, print-ready SVG, 3D bead preview PNG, flat preview PNG, and bead count list.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
