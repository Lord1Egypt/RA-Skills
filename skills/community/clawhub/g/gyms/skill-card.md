## Description:

Find nearby gyms. Invoke when user asks for fitness centers near me.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeclaw007](https://clawhub.ai/user/mikeclaw007)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to request nearby fitness centers from an agent, with location, radius, limit, and optional amenity or rating filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on user-authorized location data.

Mitigation: Request location only for nearby-gym lookup and avoid retaining precise coordinates; use coarse grid handling when retention is necessary.

Risk: The skill references a local STANDARD_RESPONSE.md file that is not bundled with the release.

Mitigation: Clarify the response schema with the publisher or provide an equivalent bundled schema before relying on exact output formatting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikeclaw007/skills/gyms)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or structured text describing nearby gym results and possible lookup errors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected result fields are described by a referenced standard response file that is not bundled with this release.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
