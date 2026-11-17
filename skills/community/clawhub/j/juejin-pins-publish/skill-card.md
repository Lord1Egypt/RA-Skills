## Description:

Publishes Juejin Pins through a logged-in browser session when a user asks to post content, club or topic selections, images, links, or code blocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itcastwsy](https://clawhub.ai/user/itcastwsy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through publishing short-form Juejin community posts with optional circles, topics, images, links, and code snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish public Juejin posts from a logged-in browser session without enforcing a final confirmation step.

Mitigation: Review the post text, selected club or topic, links, code, and images before allowing the final publish action.

Risk: The skill depends on the user's active Juejin session to perform publishing actions.

Mitigation: Install and use it only when the user is comfortable letting the agent operate within that logged-in browser session.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itcastwsy/skills/juejin-pins-publish)
- [Juejin Pins](https://juejin.cn/pins)
- [Juejin Pin clubs](https://juejin.cn/pin/clubs)
- [Juejin Pin topics](https://juejin.cn/pin/topics)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline browser automation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include post text, club and topic choices, image paths, links, or code snippets supplied by the user.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
