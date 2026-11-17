## Description:

Bright Data (brightdata.com). Use this skill for ANY Bright Data request — searching and reading data. Whenever a task involves Bright Data, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to read account status and discover Bright Data marketplace datasets, dataset views, snapshot metadata, and ready snapshot parts through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes downloaded CLI installers without a fixed release; the publisher notes that broader changes to agent skills may occur, and external installers and hosted connector code were not verified.

Mitigation: Review and approve CLI installation separately using a fixed, independently verified release. If automatic agent-skill changes are unwanted, set OO_SKILLS_SYNC_DISABLED=1.

## Reference(s):

- [Bright Data](https://brightdata.com)
- [Bright Data API authentication documentation](https://docs.brightdata.com/api-reference/authentication)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API calls, JSON, Guidance]

**Output Format:** [JSON action responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only account and marketplace lookups.]

## Skill Version(s):

1.0.4 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
