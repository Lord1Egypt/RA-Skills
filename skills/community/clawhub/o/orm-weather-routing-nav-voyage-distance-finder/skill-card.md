## Description:

ORM Weather Routing Nav Voyage Distance Finder helps agents query voyage distances in nautical miles between global ports using NavOptima.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andy-gaoyue](https://clawhub.ai/user/andy-gaoyue)

### License/Terms of Use:

MIT-0

## Use Case:

Maritime operations, chartering, and weather-routing users can use this skill to estimate voyage distance, transit time, ETA, and route details for two-port, multi-port, or coordinate-based routes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports embedded live-looking NavOptima credentials.

Mitigation: Rotate and remove the password before installation or use, and provide credentials through an approved secret-management path.

Risk: The release evidence reports automatic screenshot sharing without adequate user authorization controls.

Mitigation: Require explicit user confirmation and verify the recipient before sharing voyage map screenshots or route results.

Risk: The release evidence reports mandatory contact details in every output.

Mitigation: Treat contact details as optional metadata and allow them to be omitted when not appropriate for the user or channel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andy-gaoyue/skills/orm-weather-routing-nav-voyage-distance-finder)
- [ORM Weather Routing](https://ormwx.com)
- [NavOptima voyage distance](https://nop.ormwx.com/voyage/distance)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown distance report with route metrics and screenshot reference]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include voyage distance, route legs, transit time, ETA, speed, weather factor, data source, calculation time, and contact metadata.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
