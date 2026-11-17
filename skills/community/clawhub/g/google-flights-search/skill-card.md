## Description:

Searches live Google Flights prices and schedules through SearchAPI.io and returns structured flight options for comparison, booking-link lookup, and price monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galdayan](https://clawhub.ai/user/galdayan)

### License/Terms of Use:


## Use Case:

External users and travel-focused agents use this skill to search flight options, compare prices and schedules, retrieve booking links, and prepare price monitoring for requested trips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic price monitoring can store travel plans or contact identifiers without clear consent.

Mitigation: Require explicit user consent before saving monitoring data, and define retention and deletion rules for saved travel plans.

Risk: Raw flight API responses and booking or departure tokens may be written to logs.

Mitigation: Restrict or disable raw logs, redact booking/departure tokens and contact identifiers, and audit log access before deployment.

Risk: The skill depends on a live SearchAPI.io credential.

Mitigation: Use a limited SearchAPI.io key stored in environment secrets, and monitor quota, errors, and unexpected use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/galdayan/skills/google-flights-search)
- [SearchAPI.io signup](https://www.searchapi.io/users/sign_up)
- [SearchAPI.io Google Flights API endpoint](https://www.searchapi.io/api/v1/search)

## Skill Output:

**Output Type(s):** [json, shell commands, configuration, guidance]

**Output Format:** [JSON from the helper script, with concise text or markdown flight recommendations after scoring and formatting.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SEARCHAPI_KEY; uses live SearchAPI.io calls and can include booking tokens, prices, schedules, layovers, and booking URLs.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact _meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
