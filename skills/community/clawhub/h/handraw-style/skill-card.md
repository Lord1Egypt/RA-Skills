## Description:

261 hand-drawn style prompt catalog with a numbered system for GPT Image, Midjourney, and other AI image generators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsonbuilds](https://clawhub.ai/user/johnsonbuilds)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to choose numbered hand-drawn prompt styles and maintain visual consistency across generated images, social posts, blog art, or video assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Style numbers are arbitrary and may not be understood without the catalog.

Mitigation: Review the upstream catalog before relying on a style number for production image generation.

Risk: Different image-generation platforms may interpret the same style reference differently.

Mitigation: Validate sample outputs on the target platform before using a numbered style in a larger batch.

Risk: The skill can activate on broad requests about hand-drawn style consistency.

Mitigation: Confirm that numbered hand-drawn prompt guidance is desired before applying the catalog.

## Reference(s):

- [Server-resolved GitHub import](https://github.com/johnsonbuilds/awesome-hermes-skills/tree/main/creative/handraw-style)
- [Handraw Style upstream catalog](https://github.com/yang0/handraw-style)
- [ClawHub skill page](https://clawhub.ai/johnsonbuilds/skills/handraw-style)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with prompt snippets and numbered style references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable prompt reference for image-generation style selection.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
