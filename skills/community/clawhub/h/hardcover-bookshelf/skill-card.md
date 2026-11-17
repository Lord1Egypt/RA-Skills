## Description:

Talk to a user's Hardcover bookshelf via the Hardcover GraphQL API to manage reading activity in natural language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diwakergupta](https://clawhub.ai/user/diwakergupta)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users and agents use this skill to inspect and update a user's Hardcover reading account, including Want to Read items, Currently Reading status, Read status, and previous-year reading counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Hardcover API token and can change account reading status.

Mitigation: Require the user to provide HARDCOVER_TOKEN intentionally, confirm start and finish actions before execution, and avoid mutating when title resolution is ambiguous.

Risk: Runtime commands use npx-based dependencies that may be downloaded or resolved at execution time.

Mitigation: Prefer a lockfile-pinned install and run the packaged local CLI from installed dependencies instead of allowing ad hoc runtime downloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diwakergupta/skills/hardcover-bookshelf)
- [Hardcover API settings](https://hardcover.app/account/api)
- [Hardcover GraphQL endpoint](https://api.hardcover.app/v1/graphql)
- [Hardcover GraphQL Patterns](references/graphql-patterns.md)
- [Hardcover schema quirks](references/schema-quirks.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text responses, with optional JSON from CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HARDCOVER_TOKEN and may execute local TypeScript CLI commands that call the Hardcover GraphQL API.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
