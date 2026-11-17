## Description:

Use Geokeo to search geocoding data and retrieve forward or reverse geocoding results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve geocoding results from Geokeo for place queries or coordinates through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI installation and binaries have not been verified.

Mitigation: Review and approve installation separately, preferably using a verified fixed version.

Risk: Startup skill synchronization may make changes to agent skills that have not been reviewed.

Mitigation: Disable startup synchronization with OO_SKILLS_SYNC_DISABLED=1 unless those changes are intended.

Risk: Addresses and coordinates pass through OOMOL to Geokeo.

Mitigation: Submit only location information you intend to share with those services.

## Reference(s):

- [Geokeo API Documentation](https://geokeo.com/documentation.php)
- [Geokeo](https://geokeo.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Configuration instructions]

**Output Format:** [Geocoding results as JSON, with inline shell commands and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected Geokeo action and its live input schema.]

## Skill Version(s):

1.0.6 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
