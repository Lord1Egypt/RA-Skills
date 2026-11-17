## Description:

Ambivo (ambivo.com). Use this skill for ANY Ambivo request — reading, creating, updating, and deleting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill through their connected OOMOL account to read Ambivo CRM contacts, leads, and tasks, and to create or update records. It can also delete tasks when the user confirms the target and effect.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup can run a downloaded CLI installer before its contents and deployed version have been verified.

Mitigation: Review the installer, verify the CLI version, and approve CLI installation separately before running it.

Risk: CLI startup may change agent skill directories, and the scope of those changes is unclear.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 before startup if those changes are not intended, and review the provider's CLI controls.

Risk: Create, update, and delete actions can change Ambivo CRM records.

Mitigation: Inspect the live action schema and confirm the exact payload and effect before writes; confirm the target before deleting a task.

## Reference(s):

- [Ambivo website](https://www.ambivo.com/)
- [Ambivo API documentation](https://docs.ambivo.com/ambivo-openapi/getting-started)
- [oo CLI controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-ambivo)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON action responses with concise natural-language summaries as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response fields vary by Ambivo action and requested data.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
