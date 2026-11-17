## Description:

Create and publish an Instagram carousel post from a tabiji.ai itinerary, with Topaz Labs AI image enhancement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyduckler](https://clawhub.ai/user/psyduckler)

### License/Terms of Use:


## Use Case:

Developers, creators, or social media operators use this skill to turn a tabiji.ai itinerary into a six-slide Instagram carousel with sourced travel photos, Topaz enhancement, text overlays, captioning, and publishing steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish public Instagram posts without a required preview and approval gate.

Mitigation: Require human review and explicit approval of the slides, caption, destination account, hosted image URLs, and final publish request before calling Instagram media_publish.

Risk: The workflow handles Instagram and Topaz credentials and may place access tokens in URLs.

Mitigation: Use secure token storage, pass tokens in request bodies or headers where supported, and redact tokens from logs, shell history, and generated artifacts.

Risk: The workflow pushes carousel assets to a public GitHub repository and later deletes hosted files.

Mitigation: Use a per-run temporary path, push only files generated for the current run, and delete only those files after publication is confirmed.

Risk: The workflow sends sourced images to third-party services for enhancement and publication.

Mitigation: Confirm image usage rights, privacy expectations, and account authorization before enhancement, hosting, or publication.

Risk: The workflow applies tabiji.ai branding by default.

Mitigation: Make branding configurable and confirm authorization to use the brand before publishing.

## Reference(s):

- [Instagram Graph API Carousel Publishing Reference](references/instagram-graph-api.md)
- [ClawHub Skill Page](https://clawhub.ai/psyduckler/skills/itinerary-carousel-post-topaz)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, API request examples, captions, manifests, and generated image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a six-slide Instagram carousel workflow and can return a published Instagram post URL when executed with valid account, hosting, and API credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
