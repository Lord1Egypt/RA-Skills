## Description:

Manage Apple Notes via the `memo` CLI on macOS, including creating, viewing, editing, deleting, searching, moving, and exporting notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohdalhashemi98-hue](https://clawhub.ai/user/mohdalhashemi98-hue)

### License/Terms of Use:


## Use Case:

External users and developers on macOS use this skill to ask an agent for Apple Notes operations performed through the `memo` CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a third-party `memo` CLI with Apple Notes access.

Mitigation: Install only if the user trusts the `memo` CLI source, and review the Homebrew tap or repository before installing.

Risk: Granting macOS Automation access can allow the CLI to view and change Apple Notes, including deletes through interactive commands.

Mitigation: Grant Automation access only after confirming the requested workflow, and require user confirmation before destructive note operations.

Risk: The artifact states that notes containing images or attachments cannot be edited and that interactive prompts may require terminal access.

Mitigation: Use view or export workflows for unsupported notes, and ask the user to complete terminal prompts when an operation cannot run noninteractively.

## Reference(s):

- [ClawHub Skill: MH apple-notes](https://clawhub.ai/mohdalhashemi98-hue/skills/mh-apple-notes)
- [memo CLI project](https://github.com/antoniorodr/memo)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [macOS-only; requires the third-party `memo` CLI and Apple Notes Automation access for note operations.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
