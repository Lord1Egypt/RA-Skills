## Description:

Pixel Art Processing helps agents process pixel art and sprite assets, including video frame extraction, GIF and frame conversion, sprite sheet composition and splitting, matting, pixelation, resizing, cropping, chroma keying, RPG Maker workflows, and watermark removal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anlinxi](https://clawhub.ai/user/anlinxi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, game creators, and technical artists use this skill to guide local or browser-based conversion of GIFs, frames, videos, and sprite sheets into game-ready pixel assets, including RPG Maker layouts and index metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary says the release can run local services from unverified sibling code.

Mitigation: Prefer the local image-processing script or browser tool in a sandbox, and do not run deploy.py unless the sibling backend directory has been reviewed.

Risk: The server security summary says the browser page loads third-party scripts and may expose private images through CDN-backed browser processing.

Mitigation: Use the browser tool only in an isolated profile for non-sensitive media, or use the local processor for private assets.

Risk: The server security summary says watermark removal lacks guardrails.

Mitigation: Use watermark removal only for media you own or are authorized to modify.

Risk: The server security summary says process termination behavior is overbroad.

Mitigation: Review process-management behavior before running deploy.py on a shared workstation.

## Reference(s):

- [API Reference](references/api.md)
- [RPG Maker Workflow](references/rpgmaker.md)
- [Sprite Sheet Math](references/sprite_math.md)
- [rembg](https://github.com/danielgatis/rembg)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, code snippets, API descriptions, and generated file descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can guide generation of PNG sprites, GIFs, ZIP archives, and index.json metadata through bundled local or browser tools.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
