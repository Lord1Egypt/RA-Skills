## Description:

Hauscout automates collection and AI analysis of HouseSigma real estate listings, then stores structured listing data and price-history updates in Neon PostgreSQL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sonim1](https://clawhub.ai/user/sonim1)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run and verify a real estate listing collection pipeline, including targeted listing or profile collection, AI analysis, database updates, and post-run reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run unaudited local collection code that scrapes HouseSigma, calls AI services, and writes or updates persistent database records.

Mitigation: Inspect the collection script and dependencies, run with dry-run first, and use scoped database credentials before allowing persistent writes.

Risk: The skill's workflow can create local memory summaries and push repository changes after collection.

Mitigation: Review generated files, git status, and diffs before committing, and require explicit manual approval before any push.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sonim1/skills/hauscout)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown with inline shell and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to create dated local collection summaries and report new listings, price changes, errors, and database query results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
