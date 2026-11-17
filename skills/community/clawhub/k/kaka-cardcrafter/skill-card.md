## Description:

Helps agents create Xiaohongshu posts with illustrations, multi-format covers, and illustrated knowledge cards using Cardcrafter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fan-look](https://clawhub.ai/user/fan-look)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and marketing teams use this skill to draft social posts and generate accompanying images, platform covers, and knowledge cards. Agents can show an outline for approval before generating Xiaohongshu images and present the resulting images as Markdown links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested content is sent to Cardcrafter for generation or transformation.

Mitigation: Avoid submitting confidential, regulated, or highly sensitive content unless Cardcrafter's handling policies meet your needs.

Risk: Exposure of the Cardcrafter API key could allow unauthorized use.

Mitigation: Store KAKA_API_KEY as a secret; do not paste it into prompts or commit it to repositories.

Risk: Generation consumes paid account energy, and published material may contain inaccurate or noncompliant claims.

Mitigation: Confirm content and expected generation scope before producing images, and review generated text and images before publication.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/fan-look/skills/kaka-cardcrafter)
- [Cardcrafter WorkBuddy integration guide](https://www.cardcrafter.cn/platforms/workbuddy)
- [Cardcrafter open platform API guide](https://api.cardcrafter.cn/openapi/skill.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Image links]

**Output Format:** [Markdown text and image links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outlines can be revised before image generation; image results may require asynchronous polling and may complete partially.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
