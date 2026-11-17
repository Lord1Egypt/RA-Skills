## Description:

Search and read HotspotSystem account data through the OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External HotspotSystem operators use the skill to retrieve information about their account, locations, customers, and subscribers through the connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions include an unverified remote installer that could execute code on the user's machine.

Mitigation: Review and install a known CLI version yourself, and require approval before an agent downloads or runs an installer.

Risk: The connected CLI can access HotspotSystem account and location data.

Mitigation: Check the CLI's automatic skill installation behavior and connect only the account and locations you intend to expose.

## Reference(s):

- [HotspotSystem API documentation](https://www.hotspotsystem.com/apidocs/api/reference)
- [HotspotSystem](https://www.hotspotsystem.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured connector results with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only account data retrieval]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
