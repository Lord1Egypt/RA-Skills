## Description:

hintme helps an agent analyze video game screenshots or descriptions and provide progressive, spoiler-free hints from a gentle nudge to an explicit answer when requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kewang0622](https://clawhub.ai/user/kewang0622)

### License/Terms of Use:

MIT-0

## Use Case:

External players use this skill through an agent when they are stuck in a video game and want help from screenshots or descriptions without story spoilers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Game screenshots may contain private chat, account names, or other personal information.

Mitigation: Ask users to crop or redact sensitive screenshot areas before sharing them with the agent.

Risk: Game-specific web lookups or uncertain screenshot interpretation may lead to incorrect or overly revealing guidance.

Mitigation: Use web lookup only for game-guide context when needed, verify details before giving Hint 3, and keep answers limited to the immediate stuck point.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kewang0622/skills/hintme)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with progressive hint sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Starts with Hint 1 and only provides clearer hints or the explicit answer when the user asks for more help.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
