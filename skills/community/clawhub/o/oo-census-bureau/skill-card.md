## Description:

Census Bureau (census.gov). Use this skill for ANY Census Bureau request — searching and reading data. Whenever a task involves Census Bureau, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use the skill to search Census Bureau datasets, inspect variable groups and variables, and query Census data through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs the agent to execute a remote CLI installer that the release security review did not verify.

Mitigation: Review and approve CLI installation separately, preferably using a pinned, verified release, and check the CLI's automatic skill synchronization before running it.

Risk: Census requests through OOMOL may incur charges.

Mitigation: Check applicable OOMOL billing and usage before making Census requests.

## Reference(s):

- [Census Bureau](https://www.census.gov)
- [Census Data API User Guide](https://www.census.gov/data/developers/guidance/api-user-guide.html)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON Census data with natural language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected Census dataset, variables, geography, and filters.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
