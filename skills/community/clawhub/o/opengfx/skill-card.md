## Description:

OpenGFX helps agents generate complete logo systems with icon, wordmark, lockups, and production-ready SVG vector assets from natural language prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aklo360](https://clawhub.ai/user/aklo360)

### License/Terms of Use:


## Use Case:

Designers, developers, and brand builders use OpenGFX to turn a natural language brand brief into a logo asset set with SVG lockups and machine-readable logo metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SVG logo assets may be malformed, include live text, or be unsuitable for publication without design review.

Mitigation: Review the generated SVGs and logo-system.json against the artifact's quality checklist before publishing or using them in production.

Risk: Hosted workflows may upload generated logo assets or saved design learnings as part of an automated ACP flow.

Mitigation: Confirm upload handling, retention, and access controls for any hosted workflow before submitting sensitive brand concepts.

## Reference(s):

- [OpenGFX ClawHub Skill Page](https://clawhub.ai/aklo360/skills/opengfx)
- [Geometric Foundations for Logo Design](artifact/references/GEOMETRY.md)
- [Logo Lockup Construction](artifact/references/LOCKUPS.md)
- [Logo Modernism Principles](artifact/references/MODERNISM.md)
- [Logo System Output Schema](artifact/references/OUTPUT_SCHEMA.md)
- [Typography for Logo Wordmarks](artifact/references/TYPOGRAPHY.md)
- [Logo System JSON Schema](https://opengfx.aklo.io/schemas/logo-system.v1.json)

## Skill Output:

**Output Type(s):** [Code, Files, Configuration, Guidance]

**Output Format:** [SVG files, JSON metadata, and concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces icon.svg, wordmark.svg, stacked.svg, horizontal.svg, and logo-system.json; generated SVGs should be reviewed before publishing.]

## Skill Version(s):

1.3.1 (source: server release metadata; artifact frontmatter reports 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
