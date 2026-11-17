## Description:

Foursquare (foursquare.com). Use this skill for ANY Foursquare request — searching and reading data. Whenever a task involves Foursquare, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected Foursquare account can search for nearby places and retrieve place details, photos, and tips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs unverified downloaded code, and the installer's approval scope is unclear.

Mitigation: Review the oo CLI installer and downloaded release before running it; check bundled-skill synchronization settings and local changes before enabling the skill.

Risk: Location and search details are shared through OOMOL with Foursquare when actions run.

Mitigation: Use only location and search information you intend to share through OOMOL with Foursquare.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Foursquare API documentation](https://docs.foursquare.com/developer/reference)
- [Foursquare](https://foursquare.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON responses from Foursquare read actions, with natural-language summaries as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Place search and retrieval; requires the oo CLI and a connected Foursquare account.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
