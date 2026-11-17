## Description:

CATS (catsone.com). Use this skill for ANY CATS request — searching and reading data. Whenever a task involves CATS, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting teams and users with connected CATS accounts can search, list, and read candidate, company, job, and site records through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unchecked remote code or introduce broader agent changes without clear user control.

Mitigation: Review and install the CLI separately, limit CATS access to needed records, and review startup synchronization; set OO_SKILLS_SYNC_DISABLED to disable it.

## Reference(s):

- [CATS homepage](https://catsone.com/)
- [CATS API v3 documentation](https://docs.catsone.com/api/v3/)
- [oo CLI commands](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Text]

**Output Format:** [JSON records returned by CATS actions, with concise textual summaries and oo CLI commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only candidate, company, job, and site data; pagination is available for list and search actions.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
