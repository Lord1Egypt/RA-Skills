## Description:

Navigate Hong Kong like a local with district-specific food spots, transport tips, hikes, neighborhoods, and honest advice on what is worth your time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wingchiu](https://clawhub.ai/user/wingchiu)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning agents use this skill to plan Hong Kong trips with neighborhood, food, transport, family, nightlife, hiking, beach, and practical safety guidance. It helps tailor recommendations by trip length, interests, group type, budget, season, and pace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store trip preferences locally in ~/hongkong/, which may include travel dates, budget, mobility needs, or other personal planning details.

Mitigation: Keep sensitive details out of the local memory file when possible and review or delete ~/hongkong/memory.md when the trip is complete.

Risk: The skill may ask whether it should proactively help whenever Hong Kong is mentioned.

Mitigation: Decline or limit proactive assistance if the skill should only be used for direct travel-planning requests.

Risk: Travel recommendations can become outdated as venues, transport options, prices, weather alerts, and opening hours change.

Mitigation: Verify time-sensitive plans against current official or local sources before booking, traveling, hiking, or responding to emergencies.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/wingchiu/skills/hongkong)
- [Skill homepage](https://clawic.com/skills/hongkong)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown travel-planning guidance with local memory setup notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain user-provided Hong Kong trip preferences in ~/hongkong/memory.md when enabled.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
