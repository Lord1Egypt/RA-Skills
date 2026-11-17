## Description:

Use Ambee to geocode places and retrieve air-quality observations, forecasts, and history through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can geocode locations and retrieve Ambee air-quality observations, forecasts, and historical readings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automatic setup workflow can run downloaded CLI installer code without a separate approval step.

Mitigation: Review and approve CLI setup separately, prefer a reviewed and pinned release, and check whether it installs or updates other agent skills.

Risk: Place names and coordinates pass through OOMOL to Ambee.

Mitigation: Submit only locations the user intends to share.

## Reference(s):

- [Ambee homepage](https://www.getambee.com)
- [Ambee API documentation](https://docs.ambeedata.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON requests and responses with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the oo CLI and an active Ambee connection; location names and coordinates are sent to Ambee through OOMOL.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
