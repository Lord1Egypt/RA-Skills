## Description:

PigBun RedNote helps agents automate RedNote/Xiaohongshu content search, publishing, comment management, social engagement, and creator analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pigbun-ai](https://clawhub.ai/user/pigbun-ai)

### License/Terms of Use:


## Use Case:

External social media operators, creators, and developers use this skill through an agent to search RedNote content, publish and manage posts, respond to comments, perform social interactions, and generate operational analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform visible RedNote account actions such as publishing, editing, deleting, commenting, following, liking, and collecting.

Mitigation: Require explicit user confirmation before any publish, edit, delete, comment, follow, like, or collect action, and review generated content before submission.

Risk: The skill uses a PigBun API key and an authenticated RedNote account session.

Mitigation: Store the API key as a secret, avoid committing account configuration, and use the skill only with accounts approved for agent-assisted automation.

Risk: The setup requires a Playwright Chromium installation flow.

Mitigation: Use a pinned, trusted Playwright installation and review browser automation dependencies before deployment.

## Reference(s):

- [PigBun RedNote ClawHub listing](https://clawhub.ai/pigbun-ai/skills/pigbun-rednote)
- [PigBun website](https://pigbunai.com)
- [PigBun-AI ClawHub profile](https://clawhub.ai/user/pigbun-ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON configuration snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce agent actions that use configured PigBun credentials and an authenticated RedNote account session.]

## Skill Version(s):

0.8.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
