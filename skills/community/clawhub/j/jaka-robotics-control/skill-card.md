## Description:

Control JAKA Zu20, Zu12, Zu7, and MiniCobo collaborative robots through Python and command-line workflows for state inspection, joint motion, linear motion, and tool I/O.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qujingyang28](https://clawhub.ai/user/qujingyang28)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, robotics engineers, and trained robot operators use this skill to connect to JAKA collaborative robots, inspect robot state, and issue motion or I/O commands from Python scripts or a CLI. It is intended for controlled robot environments where vendor safety controls and operator procedures are active.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can issue direct physical robot motion commands.

Mitigation: Use it only in a controlled robot environment with trained operators, a clear workcell, a reachable emergency stop, reduced-speed testing, and vendor safety controls active.

Risk: Motion targets, speeds, and command confirmations have weak safety checks.

Mitigation: Review or add bounds checks, confirmations, finite-value validation, speed limits, and failure handling before use on a live robot.

Risk: Runtime behavior depends on the external JAKA SDK and local installer files.

Mitigation: Use pinned, verified SDK and installer versions and test installation in a non-production setup before robot operation.

## Reference(s):

- [JAKA Python SDK Documentation](https://www.jaka.com/docs/guide/SDK/Python.html)
- [JAKA SDK Introduction and Download](https://www.jaka.com/docs/guide/SDK/introduction.html)
- [RobotQu Community](https://robotqu.com)
- [ClawHub Skill Page](https://clawhub.ai/qujingyang28/skills/jaka-robotics-control)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include robot IP addresses, motion targets, speed values, setup steps, and safety pre-check guidance.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
