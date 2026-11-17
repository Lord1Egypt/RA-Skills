## Description:

Operate a connected MailBluster account to read, create, update, and delete leads and list custom fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to manage MailBluster leads and inspect custom fields through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run an external installer that has not been inspected and may make broader changes to the agent environment.

Mitigation: Review and approve CLI installation separately, check any additional skills it installs, and use OO_SKILLS_SYNC_DISABLED to prevent startup skill synchronization when appropriate.

Risk: Creating, updating, or deleting leads changes account data.

Mitigation: Confirm the exact write payload and effect before running a write, and confirm the target before deleting a lead.

## Reference(s):

- [oo CLI command documentation](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [MailBluster API documentation](https://app.mailbluster.com/api-doc/getting-started)
- [MailBluster homepage](https://mailbluster.com)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Shell commands]

**Output Format:** [JSON API results and concise Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MailBluster lead data or custom-field information returned by requested actions.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
