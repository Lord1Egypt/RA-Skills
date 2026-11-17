## Description:

Use when drying laundry on a rack indoors (or outdoors): computes hours-to-dry from vapor-pressure-deficit evaporation physics and spin-speed residual moisture, the kg of water the load dumps into your air, the room RH rise (condensation risk), and the cheapest drying method comparison (rack vs dehumidifier vs heated airer vs tumble dryer kWh).

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Households and other laundry handlers can estimate indoor or outdoor drying time, residual water, room humidity and condensation risk, and compare drying-method energy costs. Use the estimates to plan when to hang a load and choose a drying method suited to the room and weather.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Drying-time, humidity, and cost results are estimates, and the documentation and script use differing model coefficients.

Mitigation: Treat results as estimates; check the assumptions and verify them against observed conditions before relying on them for drying, ventilation, or cost decisions.

## Reference(s):

- [Drying physics reference](references/drying-physics.md)
- [ClawHub release](https://clawhub.ai/voronindenis5/skills/laundry-dry-forecaster)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON]

**Output Format:** [Plain-text drying estimates and cost comparison, or JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Estimates depend on user-supplied load, spin, room, airflow, ventilation, weather, and energy-price assumptions.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
