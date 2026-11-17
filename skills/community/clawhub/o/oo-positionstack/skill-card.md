## Description:

Search Positionstack through a connected account for forward and reverse geocoding results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn addresses or place queries into geocoding results, and to look up locations from coordinates or IP addresses through Positionstack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions offer installers that download and execute software whose contents and hosted implementation are unverified.

Mitigation: Review and install a fixed CLI release yourself before enabling this skill.

Risk: OO CLI startup synchronization may introduce additional agent skills without clearly disclosing those changes.

Mitigation: Review the CLI synchronization behavior and set OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization if desired.

Risk: Location queries may disclose addresses, coordinates, or IP addresses to OOMOL and Positionstack.

Mitigation: Share only location information you intend those services to receive.

## Reference(s):

- [Positionstack API documentation](https://docs.apilayer.com/positionstack/docs/api-documentation)
- [Positionstack](https://positionstack.com)
- [OO CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request and response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Positionstack account and requested lookup.]

## Skill Version(s):

1.0.5 (source: frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
