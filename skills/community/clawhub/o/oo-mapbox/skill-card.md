## Description:

Mapbox (mapbox.com). Use this skill for ANY Mapbox request — searching and reading data. Whenever a task involves Mapbox, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can use the skill to search Mapbox geographic data, geocode places and coordinates, and request directions or travel matrices through their OOMOL-connected Mapbox account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup may run downloaded code whose contents and exact changes have not been verified, without a clear approval step.

Mitigation: Review and approve the CLI installation separately, including its automatic agent-skill synchronization; prefer a verified, versioned installation before enabling the skill.

Risk: Addresses and coordinates submitted through the skill pass through OOMOL to Mapbox.

Mitigation: Avoid submitting sensitive location data and disclose this data path before sending location details.

## Reference(s):

- [Mapbox API documentation](https://docs.mapbox.com/api/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-mapbox)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Mapbox action results returned as JSON and task responses as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The available actions cover geocoding, directions, and travel matrices.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
