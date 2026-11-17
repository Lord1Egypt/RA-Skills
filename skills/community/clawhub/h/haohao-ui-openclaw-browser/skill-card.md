## Description:

Use the OpenClaw-managed browser for real website interaction, page operations, snapshots, clicks, typing, waits, screenshots, and tab control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haohao-ui](https://clawhub.ai/user/haohao-ui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when a task needs controlled interaction with real websites, including navigation, snapshots, clicks, typing, waits, screenshots, tab control, and browser-profile selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using a live signed-in browser profile can allow an agent to act in the user's real account session.

Mitigation: Prefer isolated OpenClaw browser profiles for routine work; use the user profile only when the task requires it and the user is present to approve live-account actions.

Risk: Reusing another agent's profile or an unmanaged browser flow can mix session state across tasks.

Mitigation: Use an explicit, dedicated browser profile when available and keep actions within the OpenClaw browser tool or CLI surface.

## Reference(s):

- [OpenClaw Browser skill listing](https://clawhub.ai/haohao-ui/skills/haohao-ui-openclaw-browser)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance emphasizes explicit browser profiles, snapshot-based page actions, and using the OpenClaw browser tool or CLI surface.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
