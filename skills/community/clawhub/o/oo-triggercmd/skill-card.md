## Description:

TRIGGERcmd (triggercmd.com). Use this skill for ANY TRIGGERcmd request — reading, creating, and updating data. Whenever a task involves TRIGGERcmd, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to list saved TRIGGERcmd commands and trigger a selected command on a connected computer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs an external installer whose contents and system changes are unverified.

Mitigation: Install and verify the oo CLI separately, and prevent automatic execution of its installer fallback.

Risk: Triggering a saved command can cause effects on the named computer.

Mitigation: Confirm the computer, saved command, parameters, and expected effect before execution.

## Reference(s):

- [TRIGGERcmd API documentation](https://docs.triggercmd.com/)
- [TRIGGERcmd homepage](https://www.triggercmd.com/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI install guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON data, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action results depend on the connected TRIGGERcmd account; write actions require confirmation of the exact command and expected effect.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
