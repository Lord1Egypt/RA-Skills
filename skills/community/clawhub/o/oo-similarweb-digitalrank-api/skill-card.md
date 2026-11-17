## Description:

Use Similarweb to search for and read digital-rank data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Similarweb digital-rank information, including top sites, rank-tracker campaign details, and connected subscription allowance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs a downloaded CLI installer that was not verified, and automatic skill synchronization may add other agent skills.

Mitigation: Review and approve the CLI installation separately. Disable automatic skill synchronization with OO_SKILLS_SYNC_DISABLED=1 if it is not wanted.

Risk: Actions use the connected Similarweb account and may incur usage charges.

Mitigation: Review the connected account's access and remaining usage allowance before use.

## Reference(s):

- [Similarweb API documentation](https://developers.similarweb.com/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Similarweb](https://www.similarweb.com)

## Skill Output:

**Output Type(s):** [API data, Text]

**Output Format:** [Structured JSON data and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the selected read action and connected Similarweb account.]

## Skill Version(s):

1.0.5 (source: frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
