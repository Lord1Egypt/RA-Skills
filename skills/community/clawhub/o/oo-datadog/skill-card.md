## Description:

Datadog (datadoghq.com). Use this skill for ANY Datadog request — searching and reading data. Whenever a task involves Datadog, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to search and read Datadog metric metadata, monitors, and time-series data through a user's OOMOL-connected Datadog account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI's remote installer payloads are unverified and may execute code during setup.

Mitigation: Install a reviewed, version-pinned CLI yourself before enabling the skill.

Risk: CLI setup may make broader agent changes that are not disclosed by the skill.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 before CLI use, as documented in the oo CLI command reference.

Risk: The connected Datadog credentials are mediated by OOMOL and could have broader access than needed.

Mitigation: Use narrowly scoped Datadog credentials and account for OOMOL's role in access.

## Reference(s):

- [Datadog API documentation](https://docs.datadoghq.com/api/latest/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference: environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [Datadog skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-datadog)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON action requests and responses with concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available data and fields depend on the selected Datadog action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
