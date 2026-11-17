## Description:

Capture and automate macOS UI with the Peekaboo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonydesign1999](https://clawhub.ai/user/tonydesign1999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture, inspect, and automate macOS UI workflows with Peekaboo, including screenshots, element targeting, app and window management, clipboard actions, and scripted input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screen capture and clipboard commands can expose sensitive windows, chats, credentials, files, or images.

Mitigation: Grant Screen Recording and Accessibility permissions deliberately, avoid sensitive apps and windows, and confirm clipboard reads, writes, screenshots, and scripted runs before execution.

Risk: UI automation can click, type, drag, close windows, change apps, or run scripts with unintended effects.

Mitigation: Review target app, window, element, and coordinate selections before execution, and require confirmation for destructive or high-impact UI actions.

Risk: Installation uses a third-party Homebrew tap and requires the Peekaboo binary.

Mitigation: Install only when the publisher and Homebrew tap are trusted, and verify that the expected peekaboo binary is present before using the skill.

## Reference(s):

- [Peekaboo homepage](https://peekaboo.boo)
- [ClawHub skill page](https://clawhub.ai/tonydesign1999/skills/peekaboo-1)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may emit JSON when Peekaboo is invoked with --json or -j.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
