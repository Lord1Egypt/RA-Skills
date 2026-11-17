## Description:

Recommends suitable prompts from a library of 14,000+ Nano Banana Pro image generation prompts and helps adapt selected prompts for user-specific image needs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dophinl](https://clawhub.ai/user/dophinl)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content creators use this skill to find image generation prompt templates, preview sample images, and customize a chosen template for articles, videos, social media, product marketing, avatars, posters, and related visual content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads prompt data from a mutable GitHub branch and persists it locally.

Mitigation: Use a reviewed version that pins or verifies downloaded manifests and prompt data, or review changed reference files before use.

Risk: Automatic update checks can make network requests during normal skill use.

Mitigation: Disable silent auto-update behavior where possible and run setup commands only in an environment where outbound network access is expected.

Risk: Prompt recommendations can include remote sample image handling.

Mitigation: Fetch or send media only from trusted URLs and avoid automatic media sending in sensitive workspaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dophinl/skills/nano-banana-pro-prompts-recommend)
- [YouMind Nano Banana Pro prompt gallery](https://youmind.com/nano-banana-pro-prompts)
- [Remote prompt reference files used by setup](https://github.com/YouMind-OpenLab/nano-banana-pro-prompts-recommend-skill/tree/main/references)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with prompt recommendations, links, optional image references, and setup command blocks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask clarifying questions, recommend up to three prompts, and generate a customized prompt after the user selects a template.]

## Skill Version(s):

1.5.9 (source: ClawHub release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
