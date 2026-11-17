## Description:

Searches and reads Circle community data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Use it to retrieve Circle community, member, post, space-group, and space-membership data from an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup recommends an unverified remote CLI installer without clearly requiring approval.

Mitigation: Install a reviewed CLI version yourself and require approval before installing it or changing other agent skills.

Risk: The live connector implementation has not been verified, and Circle data is handled through OOMOL.

Mitigation: Review setup before enabling the skill and confirm that OOMOL may handle your Circle data.

## Reference(s):

- [Circle](https://circle.so)
- [Circle Admin API Quick Start](https://api.circle.so/apis/admin-api/quick-start)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI install guide](https://cli.oomol.com/install-guide.md)
- [OOMOL Circle connection setup](https://console.oomol.com/connections/circle)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured Circle data with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only results for the available Circle community, member, post, and space actions.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
