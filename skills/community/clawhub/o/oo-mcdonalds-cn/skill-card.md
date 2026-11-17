## Description:

Search McDonald's China restaurants, menus, products, and store business details through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to find McDonald's China locations and retrieve menu, product, and store business information.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Setup may execute an installer without clear user approval.

Mitigation: Install a verified CLI release yourself and require approval before running installer commands.

Risk: The CLI may synchronize managed skills.

Mitigation: Review its synchronization behavior; publisher documentation identifies OO_SKILLS_SYNC_DISABLED=1 to disable it.

Risk: Queries and connected-account access are mediated by OOMOL.

Mitigation: Review the data access and connected-account scope before use.

## Reference(s):

- [McDonald's China homepage](https://open.mcd.cn)
- [McDonald's China API documentation](https://open.mcd.cn/docs/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured connector response data (JSON) and text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response fields vary by action.]

## Skill Version(s):

1.0.4 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
