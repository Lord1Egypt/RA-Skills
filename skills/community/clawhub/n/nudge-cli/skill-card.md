## Description:

How to use the nudge CLI: commands, flags, setup, onboarding, task creation, secrets, status checks, punishment configuration, and exact command syntax.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neilsanghrajka](https://clawhub.ai/user/neilsanghrajka)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents use this skill to install and operate the Nudge CLI, create accountability tasks, manage secrets and punishment actions, and check task status with exact command syntax.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides use of an accountability CLI that can store embarrassing secrets and automatically send them to contacts.

Mitigation: Prefer non-sensitive punishment messages or local notifications unless recipient confirmation, secure secret entry, deletion controls, and clear storage protections are confirmed.

Risk: The shell-script installation path executes a remote installer.

Mitigation: Prefer the Homebrew or Go installation path, or review the installer before running it.

Risk: Tokens and sensitive secrets entered directly in command lines can be exposed through shell history or process metadata.

Mitigation: Avoid entering real tokens or sensitive secrets directly in command lines; use secure input and storage mechanisms when available.

## Reference(s):

- [Nudge CLI Reference](references/cli-reference.md)
- [ClawHub skill page](https://clawhub.ai/neilsanghrajka/skills/nudge-cli)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command examples may include JSON output flags and configuration values.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
