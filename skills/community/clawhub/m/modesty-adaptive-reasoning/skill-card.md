## Description:

Automatically assess task complexity and adjust reasoning level before answering complex questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their operators use this skill as a preprocessing policy to assess request complexity and adjust reasoning depth before responding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically evaluate every request for reasoning depth and may change response style, token use, and final formatting.

Mitigation: Install only when automatic reasoning-depth control is desired, and honor explicit user controls to enable or disable reasoning escalation.

## Reference(s):

- [Skill artifact](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/modestyrichards/skills/modesty-adaptive-reasoning)
- [Publisher profile](https://clawhub.ai/user/modestyrichards)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text responses with optional reasoning-status indicators]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May change response style, token use, and final formatting when advanced reasoning is activated.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
