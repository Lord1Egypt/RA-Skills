## Description:

This placeholder skill directs users to install the GLM-Image-Generation skill for image generation.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[superdongdongyan](https://clawhub.ai/user/superdongdongyan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this placeholder release to find installation guidance for a referenced GLM image generation skill. The artifact evidence states that this skill does not provide image generation functionality itself.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install another image-generation skill with an unpinned ClawHub CLI command.

Mitigation: Install only when the ClawHub CLI source and JaredforReal/glm-image-gen skill are trusted; prefer a pinned or verified installer version when available.

Risk: Enabling the referenced skill in an environment with sensitive files or credentials could expand exposure if the referenced skill is not reviewed first.

Mitigation: Review the referenced skill before enabling it in environments that contain sensitive files, credentials, or production access.

## Reference(s):

- [Image Generation Test on ClawHub](https://clawhub.ai/superdongdongyan/skills/img-gen-fork)
- [GLM-Image-Generation skill on ClawHub](https://clawhub.ai/JaredforReal/glm-image-gen)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No direct image output; the skill points users to another skill and an install command.]

## Skill Version(s):

0.1.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
