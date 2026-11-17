## Description:

Google Routes lets agents compute routes and route matrices through an OOMOL-connected Google Routes account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to calculate routes between origins and destinations and compute route matrices for waypoint combinations via a connected Google Routes account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-time setup instructions include remote shell installer commands.

Mitigation: Review the oo CLI installation method before use and prefer a verified package or signed release when available.

Risk: Route origins, destinations, waypoints, and related metadata may be sensitive and are routed through OOMOL's connector service.

Mitigation: Use the skill only when sharing route request data with OOMOL's connector service is acceptable for the user's task and policy.

## Reference(s):

- [Google Routes documentation](https://developers.google.com/maps/documentation/routes)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)
- [Google Routes ClawHub skill page](https://clawhub.ai/oomol/skills/oo-google-routes)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses include connector data and an execution identifier when actions run successfully.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
