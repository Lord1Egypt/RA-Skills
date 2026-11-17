## Description:

Use Campaign Cleaner to read, create, update, and delete campaign data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Campaign Cleaner users use this skill to manage campaigns, check processing status and credits, and retrieve analysis reports through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute unverified CLI installation software.

Mitigation: Review and approve CLI installation separately, prefer a verified release, and consider disabling automatic skill synchronization where supported.

Risk: Campaign actions can access connected account data, submit campaigns, or delete saved campaigns.

Mitigation: Connect only the intended account and retain the skill's required confirmation for write and destructive actions.

## Reference(s):

- [Campaign Cleaner](https://campaigncleaner.com)
- [Campaign Cleaner API documentation](https://docs.campaigncleaner.com/api-reference/introduction)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [OOMOL synchronization controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [CLI commands with JSON input and structured API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read campaign data, submit campaigns, or delete saved campaigns.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
