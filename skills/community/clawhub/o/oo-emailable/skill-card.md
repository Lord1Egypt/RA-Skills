## Description:

Emailable (emailable.com). Use this skill for ANY Emailable request — reading, creating, and updating data. Whenever a task involves Emailable, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to verify individual email addresses, submit batch verification jobs, inspect batch status, and check account information through Emailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions use a remote installer, and the installer contents and installed CLI version are not verified in the release evidence.

Mitigation: Review and approve a verified, pinned CLI installation before setup, and verify the installed version.

Risk: The CLI may make changes to other agent skills during use.

Mitigation: Consider setting OO_SKILLS_SYNC_DISABLED=1 before using the CLI.

Risk: Email addresses are sent to Emailable for verification, and verification can consume account credits.

Mitigation: Only verify addresses you are authorized to send through OOMOL to Emailable, and check applicable credit costs.

## Reference(s):

- [Emailable website](https://emailable.com/)
- [Emailable API documentation](https://emailable.com/docs/api#authentication)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions, shell commands with JSON payloads, and JSON action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action and payload depend on the selected account, single-address, or batch-verification operation.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
