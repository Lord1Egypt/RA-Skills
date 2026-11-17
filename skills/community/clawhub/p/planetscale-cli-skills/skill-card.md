## Description:

Provides PlanetScale CLI command guidance and workflows for managing databases, branches, schema changes, monitoring, access, billing, backups, and related services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vince-winkintel](https://clawhub.ai/user/vince-winkintel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to inspect and manage PlanetScale organizations and databases with the `pscale` CLI. It provides focused command references and workflows for routine administration and higher impact changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database, access, billing, and destructive operations can have production or service impact.

Mitigation: Use credentials limited to the intended resources, pass `--org` explicitly, inspect the exact target, obtain approval for the specific high impact change, and verify the result.

Risk: The deployment helper deploys immediately when `--deploy` is supplied.

Mitigation: Review the exact schema change and obtain approval before invoking the helper with `--deploy`.

Risk: Credentials, database dumps, and query output may contain sensitive information.

Mitigation: Keep credentials, dumps, and query output private.

## Reference(s):

- [PlanetScale CLI documentation](https://planetscale.com/docs/reference/planetscale-cli)
- [PlanetScale CLI Skills release page](https://clawhub.ai/vince-winkintel/skills/planetscale-cli-skills)

## Skill Output:

**Output Type(s):** [Guidance, Text, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown guidance with shell command examples and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command workflows require the PlanetScale CLI and suitable authentication; examples include approval and verification steps for high impact operations.]

## Skill Version(s):

1.0.39 (source: artifact/VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
