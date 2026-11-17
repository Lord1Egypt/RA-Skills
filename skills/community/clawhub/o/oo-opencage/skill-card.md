## Description:

OpenCage (opencagedata.com). Use this skill for ANY OpenCage request — searching and reading data. Whenever a task involves OpenCage, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users use this skill to run forward geocoding, GeoJSON geocoding, and reverse geocoding through an OpenCage connection managed by OOMOL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The missing-command fallback can run an online installer that was not verified.

Mitigation: Review the installer separately, use a reviewed version-pinned installation, and check which agent skills it installs or updates.

Risk: Addresses and coordinates submitted through the skill go through OOMOL to OpenCage and may consume service credit.

Mitigation: Submit only location data appropriate for these services and account for the associated service credit.

## Reference(s):

- [OpenCage API Documentation](https://opencagedata.com/api)
- [OpenCage](https://opencagedata.com)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill listing](https://clawhub.ai/oomol/skills/oo-opencage)

## Skill Output:

**Output Type(s):** [API Calls, JSON, GeoJSON, Text]

**Output Format:** [Geocoding results as JSON or GeoJSON, presented to the agent as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected geocoding action.]

## Skill Version(s):

1.0.6 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
