## Description:

Advanced desktop automation with mouse, keyboard, screen capture, window management, clipboard operations, and optional autonomous task execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyafeichina](https://clawhub.ai/user/liyafeichina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to let an agent operate a desktop session through mouse movement, keyboard input, screenshots, window focus changes, clipboard access, and simple autonomous workflows. It is suited to local UI automation where the operator can supervise sensitive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadly control the active desktop through mouse, keyboard, window, and application actions.

Mitigation: Run it only in supervised sessions, keep failsafe enabled, prefer explicit approval for actions, and avoid financial, administrative, or otherwise sensitive workflows.

Risk: Screenshots, clipboard contents, and action logs may contain sensitive information.

Mitigation: Close private windows before use, avoid credentials and private messages, and handle saved screenshots and logs as sensitive data.

Risk: Autonomous workflows may execute unintended clicks, keystrokes, or app launches.

Mitigation: Start with low-risk tasks, set bounded step limits, and review behavior in a disposable or non-sensitive desktop session before broader use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liyafeichina/skills/mac-desktop-automation)
- [Publisher profile](https://clawhub.ai/user/liyafeichina)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python code examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce desktop actions, screenshots, clipboard reads or writes, and execution status dictionaries when used by an agent.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
