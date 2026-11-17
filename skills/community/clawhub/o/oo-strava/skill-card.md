## Description:

Connects to Strava through an OOMOL-connected account to read fitness data and create or update supported activities and athlete information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Strava users can use the skill to inspect activities, routes, segments, clubs, and training information, and to create or update supported Strava data through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may run a remote oo CLI installer that has not been verified.

Mitigation: Verify the installer and approve its installation before running the setup fallback.

Risk: The connected service can access private fitness and location data, and supported actions can upload or edit Strava data.

Mitigation: Review OOMOL's data access and automatic skill synchronization, and confirm uploads and edits before they run.

## Reference(s):

- [Strava API Reference](https://developers.strava.com/docs/reference/)
- [Strava](https://www.strava.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON data with explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include fitness and location-related account data; confirm state-changing actions.]

## Skill Version(s):

1.0.6 (source: server-resolved release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
