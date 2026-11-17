## Description:

Knock (knock.app). Use this skill for ANY Knock request — reading, creating, updating, and deleting data. Whenever a task involves Knock, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Knock through an OOMOL-connected account can retrieve or update users, trigger workflows, and delete users through the oo CLI. State changes require approval, and permanent deletion requires explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI can install other agent skills without this skill explaining or controlling those changes.

Mitigation: Review the CLI's automatic skill installation before use; set OO_SKILLS_SYNC_DISABLED=1 before any oo invocation if those changes are unwanted, and use a separately reviewed CLI version.

Risk: The remote installers and hosted connector implementation were not verified.

Mitigation: Verify the installer and select a reviewed CLI version separately.

## Reference(s):

- [ClawHub Knock release](https://clawhub.ai/oomol/skills/oo-knock)
- [Knock API documentation](https://docs.knock.app/api-reference/overview)
- [Knock homepage](https://knock.app/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON API responses and shell commands with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that change Knock state require approval; permanent deletion requires explicit confirmation.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
