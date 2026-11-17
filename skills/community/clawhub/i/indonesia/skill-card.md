## Description:

Plan Indonesia trips with island-routing logic, verified entry guidance, weather-aware logistics, and practical local execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and planning assistants use this skill to build realistic Indonesia itineraries, choose island clusters, check entry assumptions, and account for weather, transport, budget, safety, mobility, and local logistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can keep local trip-planning notes that may include travel preferences, budget assumptions, mobility constraints, and itinerary details.

Mitigation: Use or install it only when local note persistence is acceptable, and review or delete ~/indonesia/ when those details should not remain on disk.

Risk: Fast-changing entry, visa, weather, sea, volcano, park, and transport conditions can make stale travel guidance unsafe or costly.

Mitigation: Re-check current official sources before bookings, border decisions, boat crossings, volcano starts, and park visits.

Risk: Indonesia routes can involve scooters, boats, heat, rough roads, stairs, remote areas, and weaker medical backup.

Mitigation: Prefer conservative transport plans, explicit mobility and safety checks, weather or sea-condition fallbacks, and realistic buffers for risky route segments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/indonesia)
- [Skill homepage](https://clawic.com/skills/indonesia)
- [Official source map](artifact/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown travel-planning guidance with concise checklists, route logic, and operational notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local trip-planning notes under ~/indonesia/ when continuity is helpful and the user is planning beyond a one-off answer.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
