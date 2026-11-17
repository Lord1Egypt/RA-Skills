## Description:

Use Geocodio for address geocoding and coordinate reverse geocoding through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can geocode addresses and reverse geocode coordinates, one at a time or in batches, through their connected Geocodio service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes downloaded code that was not verified.

Mitigation: Review and approve CLI installation separately, using a verified release.

Risk: The publisher documents broader changes to installed agent skills.

Mitigation: Consider enabling OO_SKILLS_SYNC_DISABLED before use.

Risk: Addresses and coordinates are processed by OOMOL and Geocodio, and service charges may apply.

Mitigation: Submit only data authorized for both services and check service charges.

## Reference(s):

- [Geocodio API documentation](https://www.geocod.io/docs/)
- [Geocodio](https://www.geocod.io)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON API responses with shell command examples and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single and batch address geocoding or coordinate reverse geocoding]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
