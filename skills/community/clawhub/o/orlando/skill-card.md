## Description:

Navigate Orlando as visitor, resident, remote worker, or family with theme parks, neighborhoods, transit, costs, and local strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for practical Orlando travel, relocation, family, neighborhood, transit, cost, career, and local-life guidance. It helps agents tailor answers by visitor, resident, remote worker, student, founder, or family context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional persistent memory may retain sensitive personal details in plaintext.

Mitigation: Use the skill statelessly when possible. If ~/orlando/memory.md is enabled, keep it to lightweight planning preferences and avoid passport numbers, payment details, insurance IDs, ticket or reservation access codes, and exact home addresses.

Risk: Local memory can accumulate more detail than the user intended over time.

Mitigation: Periodically inspect ~/orlando/memory.md and delete unnecessary or sensitive details.

Risk: Orlando prices, park policies, transit rules, school boundaries, and legal requirements can change.

Mitigation: Use the official listed sources for exact current rules, prices, schedules, and location-specific requirements before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/orlando)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)
- [Visit Orlando](https://www.visitorlando.com)
- [City of Orlando](https://www.orlando.gov)
- [LYNX](https://www.golynx.com)
- [SunRail](https://sunrail.com)
- [Walt Disney World](https://disneyworld.disney.go.com)
- [Universal Orlando Resort](https://www.universalorlando.com)
- [SeaWorld Orlando](https://seaworld.com/orlando)
- [Florida Sunbiz](https://www.sunbiz.org)
- [University of Central Florida](https://www.ucf.edu)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown or plain text guidance with occasional configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May optionally use local plaintext memory under ~/orlando/ when the user confirms continuity.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
