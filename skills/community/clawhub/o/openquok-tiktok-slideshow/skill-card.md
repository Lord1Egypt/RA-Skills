## Description:

Generate TikTok photo-carousel slideshows with a locked character, AI images, text overlays, and OpenQuok CLI posting support for niche or channel personas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ratimon](https://clawhub.ai/user/ratimon)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, social media operators, and developers use this skill to research a TikTok niche, lock a consistent character, generate six-frame photo-carousel slideshows, add readable overlay text, and draft or schedule posts through OpenQuok.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles provider API keys and may upload prompts or reference images to third-party image providers.

Mitigation: Keep config.json out of source control, use environment variables or a secret manager for provider keys, and avoid uploading sensitive real-person or proprietary reference images unless the privacy implications are acceptable.

Risk: The skill can create social posts through OpenQuok.

Mitigation: Confirm OpenQuok privacy and posting settings before running the post script; prefer private draft mode when a human should review, add audio, or publish manually.

Risk: The release guidance includes installing from mutable sources.

Mitigation: Pin the installer and source revision before installing or deploying the skill.

## Reference(s):

- [OpenQuok TikTok Slideshow documentation](https://www.openquok.com/docs/other-skills/openquok-tiktok-slideshow)
- [TikTok account warm-up guide](https://www.openquok.com/blog/how-to-warm-up-a-tiktok-account-to-reach-a-us-audience)
- [Character lock](artifact/references/character-lock.md)
- [Character profile template](artifact/references/character-profile.template.json)
- [Channel research guide](artifact/references/competitor-research.md)
- [Slide structure and hook writing](artifact/references/slide-structure.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and generated workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scripts can produce channel research JSON, character profile JSON, slideshow image files, overlay image files, and OpenQuok post metadata when run with required credentials and integrations.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter and package.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
