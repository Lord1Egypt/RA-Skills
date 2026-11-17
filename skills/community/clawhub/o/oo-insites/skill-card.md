## Description:

Use the oo CLI to read Insites audit results and start new website audits through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Insites audit results and start SEO and AEO website audits through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI installation flow can execute remote code whose behavior has not been verified.

Mitigation: Review and approve the installer separately before running setup.

Risk: Automatic agent-skill synchronization can make broader agent changes.

Mitigation: Review synchronization effects and disable them with OO_SKILLS_SYNC_DISABLED if unwanted.

Risk: Starting an audit creates a new Insites audit.

Mitigation: Keep the skill's confirmation requirement before running start_audit.

## Reference(s):

- [Insites](https://insites.com)
- [Insites Audit API documentation](https://help.insites.com/en/articles/7994946-audit-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Insites skill release](https://clawhub.ai/oomol/skills/oo-insites)
- [Publisher profile](https://clawhub.ai/user/oomol)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON audit data and Markdown instructions with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions retrieve audit data; starting an audit changes Insites state and requires confirmation.]

## Skill Version(s):

1.0.4 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
