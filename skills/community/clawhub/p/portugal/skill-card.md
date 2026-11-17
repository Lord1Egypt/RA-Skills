## Description:

Discover Portugal like a local with specific restaurants, hidden gems, wine regions, and tips beyond the tourist traps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External travelers use this skill to plan Portugal trips with practical local guidance on regions, itineraries, food, wine, beaches, transport, safety, and trip style tradeoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and reuses a local plaintext trip memory that can include sensitive booking, family, dietary, mobility, and itinerary details.

Mitigation: Review the skill before installation, avoid storing passport, payment, booking confirmation, exact home-away dates, or sensitive family/accessibility details, and use owner-only permissions for ~/portugal/memory.md.

Risk: Stored trip preferences may persist longer than intended on the local filesystem.

Mitigation: Periodically review, edit, or delete ~/portugal/memory.md when trip planning is complete or preferences no longer need to be retained.

Risk: Travel recommendations, prices, opening hours, and safety context may become stale.

Mitigation: Verify time-sensitive travel, booking, health, transport, and safety details with current official or provider sources before acting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/portugal)
- [Skill Homepage](https://clawic.com/skills/portugal)
- [Skill Definition](artifact/SKILL.md)
- [Setup Guide](artifact/setup.md)
- [Memory Template](artifact/memory-template.md)
- [Portugal Regions Overview](artifact/regions.md)
- [Lisbon Guide](artifact/lisbon.md)
- [Porto Guide](artifact/porto.md)
- [Food Guide](artifact/food-guide.md)
- [Transport Guide](artifact/transport.md)
- [Emergencies and Safety Guide](artifact/emergencies.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with occasional shell commands and local configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and reuse a local plaintext trip memory at ~/portugal/memory.md.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
