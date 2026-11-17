## Description:

Creates Xiaohongshu post packages from a theme, audience, and core message, including researched title options, a confirmed outline, short-form copy with hashtags, and a 3:4 cover image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffli2002](https://clawhub.ai/user/jeffli2002)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and agents use this skill to turn a topic, target audience, and core message into a Xiaohongshu-ready content package. The workflow emphasizes human confirmation of the title and outline before drafting copy or generating cover art.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External image-generation services may receive user topics, title text, and prompt content.

Mitigation: Use the skill only with non-sensitive topics and scoped API credentials, and document what data is sent to each external service before deployment.

Risk: The callback tunnel can expose a local service to the internet.

Mitigation: Avoid running the tunnel unless the exposed service is understood and intentionally scoped; prefer a hardened callback service for production use.

Risk: Downloaded image URLs and browser screenshot handling are not fully hardened in the artifact behavior.

Mitigation: Validate download URLs, run browser automation in an isolated environment, and avoid disabling sandbox protections unless the runtime requires it.

Risk: Generated marketing copy or cover text may be inaccurate, unsafe, or inconsistent with the confirmed title.

Mitigation: Require human review of the title, outline, final copy, hashtags, and cover image before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeffli2002/skills/jeff-xiaohongshu-post)
- [Seedream image generation API endpoint](https://ark.cn-beijing.volces.com/api/v3/images/generations)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown content, shell command guidance, and generated cover-image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a dated output folder with content.md, cover.png, and a compressed cover image when the image-generation path succeeds.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
