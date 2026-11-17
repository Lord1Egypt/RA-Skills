## Description:

Search cheap flights via the MoltFlights API. Find deals, compare prices, track routes, and set up price alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhalmari](https://clawhub.ai/user/jhalmari)

### License/Terms of Use:


## Use Case:

External users and travel-planning agents use this skill to search flight options, compare prices, resolve airport codes, and monitor selected routes for price changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flight searches send route, date, and passenger-count details to MoltFlights.

Mitigation: Share only travel details appropriate for the external MoltFlights service.

Risk: Booking links may direct users to third-party travel sites.

Mitigation: Review destination sites and fare details before entering personal or payment information.

Risk: The optional price-alert pattern can create recurring local network checks.

Mitigation: Create scheduled alerts only for intended routes and review or remove the schedule when monitoring is no longer needed.

## Reference(s):

- [MoltFlights ClawHub skill page](https://clawhub.ai/jhalmari/skills/moltflights)
- [MoltFlights API documentation](https://moltflights.com/agents)
- [MoltFlights homepage](https://moltflights.com)

## Skill Output:

**Output Type(s):** [guidance, shell commands, API calls, configuration]

**Output Format:** [Markdown with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight search API responses include structured JSON with prices, route details, and booking links.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
