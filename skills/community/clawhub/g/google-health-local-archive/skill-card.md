## Description:

Read a local ghcli archive of Google Health API data for Fitbit/Google health accounts. Uses read-only local JSON queries and never calls Google Health directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fdsouvenir](https://clawhub.ai/user/fdsouvenir)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query locally archived Google Health and Fitbit history through ghcli while keeping routine health queries read-only and date-bounded.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive local health and Fitbit archive data when queried.

Mitigation: Install only when this access is intended, keep queries date-bounded, and avoid broad archive dumps.

Risk: Setup, login, sync, and export actions have broader effects than read-only archive queries.

Mitigation: Run only read-only ghcli diagnostics and queries by default, and require an explicit user request before setup, login, sync, or export.

Risk: Health archive contents may be stale or incomplete.

Mitigation: Mention data freshness when it affects an answer and ask the user before running any sync action.

## Reference(s):

- [Google Health Local Archive on ClawHub](https://clawhub.ai/fdsouvenir/skills/google-health-local-archive)
- [ghcli GitHub repository](https://github.com/fdsouvenir/ghcli)
- [ghcli Go install module](https://github.com/fdsouvenir/ghcli/tree/v1.0.4)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash commands and JSON-oriented command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are scoped to local ghcli archive queries and should use --json --read-only unless the user explicitly asks for setup, login, sync, or export.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
