## Description:

Plan India trips with specific neighborhoods, regional food calls, route choices, and grounded advice that avoids common travel mistakes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to plan India trips with route, city, food, lodging, safety, timing, transport, connectivity, and family-travel guidance. The skill is intended to narrow advice by traveler style, season, route, and friction point while keeping trip context in local memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local memory may retain trip preferences, dates, route details, group type, comfort level, and recommendations already given.

Mitigation: Use the skill only when local India trip memory is desired, and review or remove ~/india/memory.md if those notes should no longer persist.

Risk: The skill can store passport or payment details if the user intentionally asks to track them locally.

Mitigation: Avoid asking the skill to save passport or payment details unless local storage of those details is deliberate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/india)
- [Skill homepage](https://clawic.com/skills/india)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown travel guidance and local memory notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local trip memory under ~/india/memory.md when the user provides trip-relevant context.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
