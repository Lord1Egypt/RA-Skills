## Description:

Tinybird (tinybird.co). Use this skill for ANY Tinybird request — searching and reading data. Whenever a task involves Tinybird, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data teams use this skill to inspect Tinybird data sources, query published Pipe endpoints, and run SQL queries through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may run a remote CLI installer whose contents were not verified.

Mitigation: Review and approve CLI installation separately, prefer a pinned and verified release, and check whether setup adds or updates other agent skills.

Risk: Requests pass through OOMOL and use the connected Tinybird account.

Mitigation: Connect Tinybird with only the read permissions needed and account for requests passing through OOMOL.

## Reference(s):

- [Tinybird API documentation](https://www.tinybird.co/docs/md/api-reference)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Tinybird ClawHub release](https://clawhub.ai/oomol/skills/oo-tinybird)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON query results with concise text summaries and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-oriented data source metadata, Pipe endpoint results, or SQL query results]

## Skill Version(s):

1.0.4 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
