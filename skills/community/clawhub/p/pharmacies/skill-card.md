## Description:

Find nearby pharmacies. Invoke when user asks for drugstores near me.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeclaw007](https://clawhub.ai/user/mikeclaw007)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill through an agent or application to find nearby pharmacies or drugstores after sharing an authorized location. The skill supports standardized nearby-place responses with optional filters such as distance, 24-hour availability, and prescription-drug availability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on precise location data.

Mitigation: Request location authorization before use, use location only for nearby-pharmacy lookup, and avoid retaining exact coordinates unless necessary.

Risk: Provider failures, rate limits, invalid locations, or excessive radius requests can prevent complete pharmacy results.

Mitigation: Return clear error states such as invalid location, radius too large, provider unavailable, or rate limited instead of presenting missing results as complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikeclaw007/skills/pharmacies)

## Skill Output:

**Output Type(s):** [text, guidance, configuration]

**Output Format:** [Markdown guidance with JSON-shaped examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authorized user location and supports radius, limit, and optional pharmacy filters.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
