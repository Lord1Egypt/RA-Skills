## Description:

Generate meme images from memegen.rs by building a stable, shareable image URL from a template, captions, and optional image parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenequm](https://clawhub.ai/user/tenequm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create meme image links from memegen.rs templates, captions, and optional custom background image URLs when a user asks for a meme or shareable meme link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meme captions and custom background image URLs are exposed to memegen.rs.

Mitigation: Avoid private image URLs, secrets, internal links, personal data, and sensitive business text in captions or background parameters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tenequm/skills/memegen-rs)
- [Project homepage](https://github.com/tenequm/memegen-rs)
- [Release v0.1.2](https://github.com/tenequm/memegen-rs/releases/tag/v0.1.2)
- [memegen.rs OpenAPI spec](https://memegen.rs/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown link or plain URL for a PNG or animated GIF meme image]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated URL may include caption path segments and optional query parameters such as style, layout, width, height, color, or background.]

## Skill Version(s):

0.1.2 (source: evidence release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
