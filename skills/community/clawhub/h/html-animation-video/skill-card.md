## Description:

Creates an eight-second, 1080p animation in one of 29 visual styles and can optionally render it to MP4.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erich1566](https://clawhub.ai/user/erich1566)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to turn a chosen subject and visual style into reproducible HTML, Canvas, or Three.js animation source, with optional MP4 rendering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional MP4 rendering may install software and overwrite an existing output.mp4.

Mitigation: Render in a fresh project folder, use pinned project-local dependencies, control software installation separately, or use the manual-recording fallback.

Risk: Some styles use external CDN downloads that were not inspected.

Mitigation: Review and pin external dependencies before rendering, or choose a style that does not require a CDN.

## Reference(s):

- [ClawHub release](https://clawhub.ai/erich1566/skills/html-animation-video)
- [Publisher profile](https://clawhub.ai/user/erich1566)
- [29 visual style catalog](assets/README.md)
- [MP4 rendering guide](assets/RENDER.md)

## Skill Output:

**Output Type(s):** [Code, Files, Video, Guidance]

**Output Format:** [Single-file HTML/CSS/JavaScript source; optional MP4 video.]

**Output Parameters:** [1920×1080, 30 fps, 8 seconds.]

**Other Properties Related to Output:** [One of 29 visual styles; optional video rendering.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
