## Description:

Sorftime (sorftime.com). Use this skill for ANY Sorftime request — searching and reading data. Whenever a task involves Sorftime, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Sorftime market and product data to research Amazon and Walmart products, keywords, rankings, and sales through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions can execute downloaded CLI installation code without prior user approval.

Mitigation: Require separate approval before CLI installation, use a pinned and verified release, and check whether the CLI installs or synchronizes other agent skills.

## Reference(s):

- [Sorftime homepage](https://www.sorftime.com/)
- [Sorftime CLI API documentation](https://github.com/sorftime/sorftime-cli/blob/master/README.md)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Sorftime on ClawHub](https://clawhub.ai/oomol/skills/oo-sorftime)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Analysis]

**Output Format:** [Sorftime query results returned as JSON through the oo CLI, with findings summarized as text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only product, keyword, category, ranking, sales, review, and credit data; request costs vary by action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
