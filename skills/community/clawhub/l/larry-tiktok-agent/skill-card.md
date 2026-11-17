## Description:

Automatically creates and schedules six-slide TikTok slideshows with trending hooks and images linked to affiliate articles using NVIDIA FLUX and Postiz.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sonnenberglauramarie-afk](https://clawhub.ai/user/sonnenberglauramarie-afk)

### License/Terms of Use:


## Use Case:

External creators, affiliate-site operators, and developers use this skill to generate TikTok slideshow concepts, captions, slide images, local draft JSON, and optional Postiz drafts for multiple content portals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled configuration contains real-looking credentials.

Mitigation: Do not use the bundled values; rotate any exposed keys and passwords, replace them with least-privilege credentials, and restrict local file permissions.

Risk: Non-dry-run and scheduled modes can upload generated media and create TikTok/Postiz drafts through network calls.

Mitigation: Start with dry-run mode and manually review draft JSON, captions, images, and connected account settings before enabling unattended runs.

Risk: Postiz traffic can be pointed at an untrusted or weakly protected destination.

Mitigation: Use only a trusted HTTPS Postiz endpoint or a verified local instance and confirm the configured TikTok account before publishing.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/sonnenberglauramarie-afk/skills/larry-tiktok-agent)
- [Postiz](https://github.com/gitroomhq/postiz-app)
- [NVIDIA build portal](https://build.nvidia.com)
- [NVIDIA FLUX API endpoint](https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-dev)

## Skill Output:

**Output Type(s):** [Text, JSON, Image files, Shell commands, Configuration guidance, API calls]

**Output Format:** [Markdown-style usage instructions, Python shell commands, JSON draft records, generated slide image files, captions, and Postiz draft creation calls.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run mode writes local draft JSON without API calls; non-dry-run mode can generate images and upload media to create TikTok drafts through Postiz.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
