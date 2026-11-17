## Description:

PassSlot (passslot.com). Use this skill for ANY PassSlot request — reading, creating, updating, and deleting data. Whenever a task involves PassSlot, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other PassSlot users can use the skill to inspect templates and passes, retrieve pass details and installation URLs, and create, update, or delete Wallet passes through their connected PassSlot account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded installer code whose exact effects were unavailable for inspection.

Mitigation: Review setup before use and install a verified oo CLI release yourself.

Risk: Automatic skill-file synchronization may introduce persistent agent changes without clear user control.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 and keep approval requirements for write and deletion actions.

## Reference(s):

- [PassSlot](https://www.passslot.com)
- [PassSlot API documentation](https://www.passslot.com/developer/api/start)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference: environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and PassSlot action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action results vary by the selected PassSlot operation.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
