## Description:

Pixel2Motion turns raster logos into clean motion-ready SVGs and standalone HTML logo animations with motion specs and QA evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frede2010](https://clawhub.ai/user/frede2010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and brand engineers use this skill to convert PNG, JPG, WebP, or screenshot logos into editable SVG assets, choreographed logo reveals, interactive HTML demos, and QA artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can execute browser content derived from SVG or CSS inputs.

Mitigation: Use trusted logo, SVG, and motion.css inputs only, and review generated HTML before opening or publishing it.

Risk: Logo and brand assets may be confidential or unlicensed for public release.

Mitigation: Confirm asset rights and remove confidential material before publishing generated pages or previews.

Risk: Unpinned local tooling can change rendering or QA behavior across environments.

Mitigation: Pin and verify dependencies in controlled environments before relying on generated assets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frede2010/skills/pixel2motion)
- [Live interactive demo](https://nolangz.github.io/pixel2motion/)
- [HTML Delivery Template](references/html-delivery-template.md)
- [Motion Personality: Brand to Parameters](references/motion-personality.md)
- [Logo Choreography Pattern Library](references/reveal-patterns.md)
- [Closed / Self-Intersecting Ribbon Fitting](references/ribbon-fitting.md)
- [The 12 Principles, Applied to Logo Motion](references/twelve-principles-for-logos.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands plus generated SVG, HTML, CSS, PNG, and QA evidence files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces motion-ready logo assets, standalone browser-rendered animation demos, motion specifications, and geometry or motion QA artifacts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
