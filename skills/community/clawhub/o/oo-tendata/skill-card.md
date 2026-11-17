## Description:

Search Tendata and retrieve trade, company, and contact data through the connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and business users can use this skill to search Tendata trade and company records and retrieve account or contact information through their OOMOL connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow may install the oo CLI and may synchronize skills across agents; the remote installer was unavailable for inspection.

Mitigation: Review setup instructions before installing, use a verified CLI build, and decide whether cross-agent synchronization is acceptable. The oo CLI documents OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization.

Risk: Tendata queries may consume account points or request quota.

Mitigation: Use count or analysis actions to check matching records before retrieving trade details, and review the account's points and quota constraints before running retrievals.

## Reference(s):

- [Tendata homepage](https://www.tendata.cn/)
- [Tendata API integration guide](https://open-api.tendata.cn/integration-guide.html)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment variable documentation](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, JSON]

**Output Format:** [JSON results with textual trade, company, and contact data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some queries are paginated; trade retrieval may consume account points or request quota.]

## Skill Version(s):

1.0.2 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
