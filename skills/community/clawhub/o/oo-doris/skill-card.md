## Description:

Apache Doris (doris.apache.org). Use this skill for ANY Apache Doris request — searching and reading data. Whenever a task involves Apache Doris, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data teams use this skill to inspect Apache Doris databases, tables, and schemas and to run read-only queries through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified remote code.

Mitigation: Verify installer and connector sources before setup; the bundled instructions alone do not verify them.

Risk: Setup may make broader changes to other agents' skills.

Mitigation: Review skill synchronization behavior and consider setting OO_SKILLS_SYNC_DISABLED.

Risk: Requested database data may be processed by OOMOL.

Mitigation: Use a read-only Doris account and assess whether OOMOL may process the requested data.

## Reference(s):

- [Apache Doris](https://doris.apache.org)
- [Apache Doris statement execution documentation](https://doris.apache.org/docs/dev/admin-manual/open-api/fe-http/statement-execution-action/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Analysis]

**Output Format:** [JSON connector results and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query responses are capped at 8 MiB.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
