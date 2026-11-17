## Description:

Check database migrations for safety by identifying data loss risks, locking operations, backward compatibility issues, and deployment ordering problems across SQL and ORM migrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to review raw SQL and ORM migrations before deployment. It helps flag destructive schema changes, lock-heavy operations, compatibility breaks, and safer rollout patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Migration review may expose schema details or migration contents to the agent session.

Mitigation: Review only migration content that is appropriate for the active agent environment and avoid including unnecessary sensitive data.

Risk: Guidance about migration safety, lock duration, or compatibility can be incomplete without production schema and traffic context.

Mitigation: Validate recommendations against the target database version, table sizes, indexes, and deployment process before running migrations.

## Reference(s):

- [Migration Safety Checker on ClawHub](https://clawhub.ai/charlie-morrison/skills/migration-safety-checker)
- [charlie-morrison ClawHub profile](https://clawhub.ai/user/charlie-morrison)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with concise findings, risk levels, tables, and suggested migration fixes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include read-only discovery commands and database-specific safety recommendations.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
