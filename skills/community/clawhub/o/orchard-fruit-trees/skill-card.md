## Description:

Guides agents in helping users plant and manage fruit trees and berry bushes for food production, including site assessment, variety selection, pruning, pest management, and realistic harvest timelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External gardeners, homesteaders, and property owners use this skill through an agent to plan and maintain fruit trees or berry plantings. It helps the agent assess site conditions, choose climate-appropriate varieties, explain rootstock and pruning decisions, and suggest practical pest and disease management next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unverified installation commands can expose users to supply-chain or privilege-escalation risk.

Mitigation: Use a pinned or otherwise verified clawhub installer and install without elevated privileges.

Risk: Filesystem-backed notes, schedules, or reminders may retain location, property, or orchard-management details.

Mitigation: Confirm where any state is stored, avoid sensitive personal details when possible, and ensure stored notes or reminders can be disabled or removed.

Risk: Fruit variety, pest, disease, and spray guidance can be wrong when climate, region, or local regulations differ.

Mitigation: Ask for the user's location, hardiness zone or equivalent, chill hours, and local constraints, then prefer local extension or agricultural advisory sources for region-specific recommendations.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/howtousehumans/skills/orchard-fruit-trees)
- [USDA Plant Hardiness Zone Map](https://planthardiness.ars.usda.gov/)
- [USDA Web Soil Survey](https://websoilsurvey.nrcs.usda.gov/)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown]

**Output Format:** [Markdown or plain text with checklists, recommendations, and seasonal management steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask for location, site, soil, drainage, and planting-goal details before giving variety-specific guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
