## Description:

Uses Peekaboo to inspect and automate native macOS desktop apps, including window focus, UI inspection, semantic actions, typing, clicking, and permission checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zimuoo](https://clawhub.ai/user/zimuoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and macOS power users use this skill to let an agent inspect and control native macOS apps for desktop workflow automation when browser DOM tools are not applicable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install a third-party desktop-control tool through Homebrew.

Mitigation: Require explicit approval for the exact Homebrew install command before installing Peekaboo.

Risk: Screen Recording and Accessibility permissions enable high-impact local app control.

Mitigation: Grant permissions only for specific desktop tasks the user initiated, inspect the target UI first, and verify state-changing actions with command evidence.

Risk: Native UI automation can affect user data or send content through local apps if the target is wrong.

Mitigation: Ask before destructive, irreversible, bulk, message-sending, or credential-related actions, and prefer semantic actions over coordinate clicks.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zimuoo/skills/peekaboo-macos-automation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and occasional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, Homebrew for automatic install, Peekaboo, and Screen Recording and Accessibility permissions for GUI automation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
