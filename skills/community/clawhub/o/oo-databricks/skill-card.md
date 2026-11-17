## Description:

Use the oo CLI to read and manage Databricks jobs, clusters, secrets, and workspace objects through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data platform operators use this skill to inspect and manage Databricks jobs, clusters, secrets, and workspace content through an OOMOL-connected account. The skill requires the oo CLI and an existing Databricks connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute unchecked downloads and add persistent skills to other agent applications.

Mitigation: Review and install a verified CLI version; set OO_SKILLS_SYNC_DISABLED=1 before invoking it when only the Databricks integration is needed.

Risk: Connected-account actions can change or delete Databricks resources.

Mitigation: Limit connected-account permissions and retain the documented approval steps for write and destructive actions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Databricks Workspace API documentation](https://docs.databricks.com/api/workspace/introduction)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown instructions with oo CLI commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use live connector schemas; write and destructive actions require confirmation as documented in the skill.]

## Skill Version(s):

1.0.6 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
