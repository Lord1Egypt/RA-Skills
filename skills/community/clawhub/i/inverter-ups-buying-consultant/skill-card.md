## Description:

Help first-time inverter UPS buyers calculate load, battery Ah, and VA rating based on their appliances, usage hours, and power situation - region-aware, brand-neutral.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arbazex](https://clawhub.ai/user/arbazex)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to guide inverter UPS buyers through appliance load, backup duration, grid quality, location, and battery preference questions. The agent then produces sizing calculations, spec priorities, and region-aware buying guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product availability, ratings, and regional certifications may change after a recommendation is generated.

Mitigation: Verify current product specifications, warranty terms, and required certifications with the seller or manufacturer before purchasing.

Risk: The consultation asks for location, appliance, outage, and power-quality details that may reveal household or office usage patterns.

Mitigation: Share only the country, city, and level of electrical detail needed to size the UPS and identify relevant standards.

Risk: Incorrect or incomplete load inputs can produce undersized or oversized inverter and battery recommendations.

Mitigation: Review appliance wattages, backup-hour assumptions, motor-startup loads, and final installation constraints before acting on the recommendation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arbazex/skills/inverter-ups-buying-consultant)
- [Skill homepage](https://github.com/arbazex/power-energy-buying-consultants/tree/master/inverter-ups-buying-consultant)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style consultation, calculations, specification recommendations, and product suggestion summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external APIs, environment variables, or runtime dependencies are required.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
