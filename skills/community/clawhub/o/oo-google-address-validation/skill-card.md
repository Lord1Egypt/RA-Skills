## Description:

Validates and standardizes postal addresses through Google Address Validation, returning a verdict, parsed address, and geocode details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to validate and standardize postal addresses through a connected Google Address Validation account, then review the returned verdict, parsed address, and geocode details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unchecked remote code and introduce undisclosed changes to other agent skills; the actual installers and released CLI binary are unverified.

Mitigation: Review setup before installing, use a verified fixed CLI release, and disable startup skill synchronization before its first invocation with OO_SKILLS_SYNC_DISABLED=1.

Risk: Addresses pass through OOMOL during validation.

Mitigation: Submit addresses only when processing them through OOMOL is acceptable for the user and their data-handling requirements.

## Reference(s):

- [Google Address Validation API documentation](https://developers.google.com/maps/documentation/address-validation/overview)
- [Google Address Validation](https://developers.google.com/maps/documentation/address-validation)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API results, JSON, Text, Shell commands, Guidance]

**Output Format:** [JSON API responses with concise text summaries; shell commands for schema inspection and action execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include validation verdict, parsed address, and geocode details when returned by the service.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
