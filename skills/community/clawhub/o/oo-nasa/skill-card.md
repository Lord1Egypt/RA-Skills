## Description:

Search and read NASA data through an OOMOL-connected NASA service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can retrieve NASA information, including near-Earth object data, space-weather events, EPIC imagery metadata, and Astronomy Picture of the Day information, through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback setup pipes a remote installer into a shell, which may run unverified code with local permissions.

Mitigation: Review the installer and use a separately reviewed, version-pinned CLI installation; check automatic skill-install settings.

Risk: NASA requests pass through OOMOL and may require account credit.

Mitigation: Confirm the NASA connection and OOMOL account requirements before relying on the service.

## Reference(s):

- [NASA API Documentation](https://api.nasa.gov/)
- [NASA](https://www.nasa.gov)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON]

**Output Format:** [Structured JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses include returned data and execution metadata.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
