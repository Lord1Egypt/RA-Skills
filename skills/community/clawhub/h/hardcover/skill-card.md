## Description:

Query reading lists and book data from Hardcover.app via GraphQL API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asaphko](https://clawhub.ai/user/asaphko)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent query their Hardcover reading library, check book progress and goals, search books, authors, and series, and prepare reading data for workflows such as Obsidian sync.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Hardcover API token and can query personal reading-library data.

Mitigation: Install it only when you want the agent to use Hardcover, keep HARDCOVER_API_TOKEN in the environment, and avoid invoking the skill for unrelated book questions.

Risk: Queries may return personal reading progress, library status, or followed-user data available through the Hardcover account.

Mitigation: Review prompts and outputs for sensitive reading data before sharing results outside the intended workflow.

## Reference(s):

- [Hardcover Entity Reference](references/entities.md)
- [Hardcover](https://hardcover.app)
- [Hardcover API Endpoint](https://api.hardcover.app/v1/graphql)
- [Hardcover API Token Settings](https://hardcover.app/settings)
- [ClawHub Hardcover Skill Page](https://clawhub.ai/asaphko/skills/hardcover)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with GraphQL and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HARDCOVER_API_TOKEN; queries are read-only and subject to Hardcover rate limits.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
