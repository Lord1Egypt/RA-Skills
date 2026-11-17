## Description:

Estimates per-pot watering amounts and check intervals from the pot, substrate, plant, and indoor conditions, and helps interpret moisture checks and watering symptoms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Houseplant owners and caregivers use this skill to estimate watering doses and moisture-check timing for individual pots, assess wet-versus-dry symptoms, and plan self-watering reservoirs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Estimated watering amounts or intervals may not match the needs of a particular plant or pot.

Mitigation: Check actual soil moisture before watering and adjust advice for the plant and conditions.

Risk: A dish-soap suggestion for hydrophobic substrate may be unsuitable for plant care.

Mitigation: Prefer repeated plain-water soaking or a horticultural wetting agent.

## Reference(s):

- [Water Balance Physics](references/water-balance.md)
- [Symptom Router](references/symptom-router.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, Shell commands, JSON]

**Output Format:** [Markdown guidance with optional JSON estimates from an offline Python helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Estimates are starting points to check against actual soil moisture; no automatic scheduling or complete care-card system.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
