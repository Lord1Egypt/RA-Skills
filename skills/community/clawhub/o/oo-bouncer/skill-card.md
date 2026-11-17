## Description:

Bouncer (usebouncer.com). Use this skill for ANY Bouncer request — reading, creating, updating, and deleting data. Whenever a task involves Bouncer, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to verify email addresses and domains, submit and manage batch or toxicity checks, and retrieve status and results through a connected Bouncer account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup runs remote installation code that is not pinned to a reviewed version.

Mitigation: Review the CLI installation separately and use a reviewed release before running the skill.

Risk: Startup skill synchronization may make broader persistent changes to agent skills whose exact behavior was not inspected.

Mitigation: Consider setting OO_SKILLS_SYNC_DISABLED=1 before running the CLI, and review skill changes before accepting them.

Risk: Email verification submits email addresses to OOMOL and Bouncer.

Mitigation: Only submit email addresses you are authorized to share with those services.

## Reference(s):

- [Bouncer API documentation](https://docs.usebouncer.com/)
- [Bouncer homepage](https://www.usebouncer.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI command and environment controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use action names and JSON inputs; inspect the live action schema before submitting a payload.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
