## Description:

Evaluates thermostat setbacks by estimating energy and cost savings, recovery effects, and comfort tradeoffs across heating systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Homeowners and HVAC practitioners use the skill to compare thermostat setback schedules, estimate seasonal heating costs, and understand recovery and comfort tradeoffs for their heating system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Savings, cost estimates, and suggested temperatures may not match actual home conditions.

Mitigation: Treat results as rough estimates, independently verify heat-pump results, and set safe temperature limits before applying schedules.

Risk: Overly low indoor temperatures can contribute to frozen pipes.

Mitigation: Set safe temperature limits and consult the linked Red Cross freeze-protection guidance before applying a schedule.

## Reference(s):

- [Setback Physics & System Handbook](references/setback-physics.md)
- [Red Cross frozen-pipe guidance](https://www.redcross.org/get-help/how-to-prepare-for-emergencies/types-of-emergencies/winter-storm/frozen-pipes.html)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Guidance]

**Output Format:** [Plain-text comparison tables and system verdicts; JSON when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rough, decision-support estimates; not exact billing predictions.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
