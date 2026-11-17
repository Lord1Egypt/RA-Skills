## Description:

Search Google Maps and retrieve place, address, and route information through the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users with a connected Google Maps account can search for places, retrieve place details, geocode addresses, and calculate routes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified remote code or add additional agent skills through automatic synchronization.

Mitigation: Review the CLI installer and selected version before setup; disable automatic skill synchronization when only Maps support is needed.

Risk: Location queries pass through OOMOL to Google and may incur charges.

Mitigation: Avoid sending unnecessary location details and check applicable account billing before repeated or large queries.

## Reference(s):

- [Google Maps Platform](https://mapsplatform.google.com/)
- [Google Maps API documentation](https://developers.google.com/maps/get-started#create-project-account-key)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance]

**Output Format:** [JSON responses and text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may contain place, address, route, and location information.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
