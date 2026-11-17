## Description:

Search and read Codegen data through the user's OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to search Codegen organizations, repositories, users, and agent runs, and to retrieve run status and results through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-time setup path can execute a remote installer whose contents and exact dependency behavior are unverified.

Mitigation: Review the setup path, require approval before running the installer, and use a reviewed, verified CLI release.

Risk: Setup may introduce lasting changes through automatic skill synchronization.

Mitigation: Review synchronization behavior and disable unwanted synchronization using the oo CLI command reference.

Risk: Use of the connected Codegen account through OOMOL may incur usage charges.

Mitigation: Review applicable account and usage terms and monitor charges.

## Reference(s):

- [Codegen API documentation](https://docs.codegen.com/api-reference/overview)
- [Codegen](https://codegen.com)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON data and text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Codegen results depend on the connected account and its available data.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
