## Description:

Connects to CrateDB Cloud to search and read account data through OOMOL's oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use the skill to inspect CrateDB Cloud organizations, projects, clusters, products, and regions through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup instructs users to run downloaded CLI installers without verification.

Mitigation: Review and approve installation separately, preferably using a verified, pinned release.

Risk: The connected service has access to the account connection and query results, and the CLI installation can add agent skills.

Mitigation: Use read-only CrateDB credentials and consider OOMOL's access to the connection and results before connecting.

## Reference(s):

- [CrateDB Cloud](https://cratedb.com/database/cloud)
- [CrateDB Cloud API documentation](https://cratedb.com/docs/cloud/en/latest/organization/api.html)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill listing](https://clawhub.ai/oomol/skills/oo-cratedb-cloud)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Text summaries and structured data from CrateDB Cloud read actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only account and resource information; CLI actions use JSON payloads.]

## Skill Version(s):

1.0.4 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
