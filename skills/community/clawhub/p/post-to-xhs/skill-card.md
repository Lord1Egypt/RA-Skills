## Description:

Post To Xhs helps an agent prepare and publish Xiaohongshu image-text or video posts by validating required fields, previewing the post, and waiting for user confirmation before publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xmznini](https://clawhub.ai/user/xmznini)

### License/Terms of Use:


## Use Case:

External users and content operators use this skill to turn provided text and local media into Xiaohongshu posts. It is intended for publishing image-text notes or video notes after required fields, media constraints, visibility, scheduling, and user confirmation are checked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish content to Xiaohongshu from the user's account.

Mitigation: Require the agent to show a complete preview and wait for explicit user confirmation before publishing.

Risk: Incorrect media paths, visibility, scheduling, or account state could result in an unintended post.

Mitigation: Check media paths, visibility, scheduling details, and the logged-in Xiaohongshu integration before confirming.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xmznini/skills/post-to-xhs)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown previews and concise status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user preview and confirmation before publishing.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
