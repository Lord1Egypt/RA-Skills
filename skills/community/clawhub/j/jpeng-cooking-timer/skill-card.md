## Description:

Kitchen cooking timer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to automate cooking timer tasks and food-related timer operations through an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for TIMER_API_KEY without explaining the receiving service, permissions, or protection model.

Mitigation: Review the publisher's service documentation and key permissions before providing a TIMER_API_KEY.

Risk: The skill points to scripts/cooking_timer.py, but that script is not included in the release artifact.

Mitigation: Confirm the referenced script exists and inspect it before running the command.

Risk: The authoritative security verdict is suspicious and recommends review before installation.

Mitigation: Review the skill and release artifact before installing or executing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-cooking-timer)
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The described workflow requires TIMER_API_KEY and returns JSON results.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
