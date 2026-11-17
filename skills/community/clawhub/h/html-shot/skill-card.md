## Description:

Render trusted HTML/SVG or a requested page to PNG/JPEG/WebP with Chromium, or convert a local raster/vector source into favicon/app-icon sets (.ico, .icns, apple-touch, PWA). Covers OG cards, transparent badges, element/full-page screenshots, Next, Electron and Tauri icons. Triggers on HTML 转图片, SVG 转 PNG, favicon, 应用图标. Raster retouching uses an image editor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rockbenben](https://clawhub.ai/user/rockbenben)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn trusted HTML, SVG, or web pages into image captures and to generate favicon and platform app-icon assets from local raster or vector sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is incomplete: coverage is 64.7%, several files were only partially inspected, and some static checks were degraded.

Mitigation: Review the uninspected files and confirm tool scope and dependency versions before installation.

Risk: Rendering executes page JavaScript and can fetch resources referenced by the input; local rendering also serves files from the input directory and nearest project public directory (or the selected base).

Mitigation: Render trusted input and use a minimal working directory with only the required assets; use OS or container isolation and egress controls when hostile content must be handled.

## Reference(s):

- [CLI and capture modes](references/cli.md)
- [Icon presets and size requirements](references/icons.md)
- [Security and reproducibility](references/security.md)
- [ClawHub skill page](https://clawhub.ai/rockbenben/skills/html-shot)

## Skill Output:

**Output Type(s):** [Image files, Favicon and app icon files]

**Output Format:** [PNG, JPEG, and WebP images; ICO, ICNS, Apple touch, and PWA icon assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pixel dimensions, capture mode, and icon variants depend on the requested options.]

## Skill Version(s):

1.2.8 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
