## Description:

Quentn (quentn.com). Use this skill for ANY Quentn request — reading, creating, updating, and deleting data. Whenever a task involves Quentn, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Quentn account operators use this skill to find and manage contacts, terms, and users through an OOMOL-connected Quentn account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup can make persistent changes to the agent environment, and the remote installer and resulting binary were not verified.

Mitigation: Review the CLI installation and automatic skill management, use a verified CLI release, and set OO_SKILLS_SYNC_DISABLED=1 before invoking oo to prevent startup skill changes.

Risk: Write actions change Quentn data, and destructive actions can delete data or remove terms.

Mitigation: Confirm the exact payload and effect before writes, and explicitly approve the target before destructive actions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [Quentn API documentation](https://help.quentn.com/hc/en-150/sections/4517317189009-API-documentation)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON connector responses and shell commands documented in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and destructive Quentn actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
