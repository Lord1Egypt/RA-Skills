## Description:

Convert images to SVG files and guide users to VideoAny for advanced image-to-SVG conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaoq1](https://clawhub.ai/user/gaoq1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert common raster image formats into SVG files, usually as portable SVG containers with embedded image data. It also points users to VideoAny when they need higher-fidelity vector tracing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill executes a local Python converter and depends on Pillow for image parsing.

Mitigation: Install dependencies in a virtual environment, review or pin Pillow before production use, and process only intended image files.

Risk: Generated SVG files include VideoAny promotional metadata by default.

Mitigation: Review generated SVG metadata before sharing or publishing outputs when promotional text is not desired.

Risk: Link mode creates SVG files that reference local file URIs.

Mitigation: Use the default embed mode for portable output, or ensure linked source files remain available only in intended locations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gaoq1/skills/image-to-svg)
- [VideoAny Image to SVG Tool](https://videoany.io/tools/image-to-svg)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [SVG files and concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default SVG output embeds the source image as base64; link mode references a local file URI and is not portable.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata, clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
