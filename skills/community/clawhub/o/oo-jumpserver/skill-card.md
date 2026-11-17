## Description:

Use the JumpServer connector through the oo CLI to search and read data in a connected JumpServer account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect managed accounts, assets, asset nodes, permissions, terminal sessions, and users in a connected JumpServer instance through OOMOL's oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can run a remote installer; the installer and connector implementation were not inspected.

Mitigation: Review the installer and its integrity before approving setup, and check the CLI's skill synchronization behavior before enabling it.

Risk: Queries can expose records available to the connected JumpServer account, and OOMOL's handling of requested records is unclear from the available evidence.

Mitigation: Use narrowly scoped, read-only JumpServer credentials and review OOMOL's handling of the records requested.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [JumpServer](https://www.jumpserver.org)
- [JumpServer API documentation](https://docs.jumpserver.org/zh/v4/dev/rest_api/)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON connector requests and results with concise text summaries and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only queries; returned data depends on the connected account's permissions.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
