## Description:

Tạo ảnh infographic, banner hoặc poster trực tiếp bằng 1 prompt gửi tới API tạo ảnh qua 9Router.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuanminhhole](https://clawhub.ai/user/tuanminhhole)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent gather required infographic details, compose an English image-generation prompt, and run a Node.js generator for Vietnamese infographics, banners, newsletters, or posters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API credentials and sends prompts to a configured 9Router image-generation endpoint.

Mitigation: Review the skill before installing, use it only in trusted workspaces, configure a known HTTPS 9Router endpoint, and avoid sensitive prompt content.

Risk: Generated images are instructed to include the publisher footer unless the skill is changed.

Mitigation: Confirm the footer is acceptable for the intended use or modify the skill before publishing generated images.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tuanminhhole/skills/infographic-generator)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline Node.js shell commands; the generator writes a PNG image file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, network access to a configured 9Router endpoint, and valid 9Router credentials.]

## Skill Version(s):

1.0.1 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
