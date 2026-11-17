## Description:

Local mouse control via ydotool wrapper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oguzhaslak](https://clawhub.ai/user/oguzhaslak)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent move and click a local Linux desktop mouse through the molt-mouse wrapper when they explicitly request pointer actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper has environment-variable escape hatches that could run unintended local code.

Mitigation: Install only in trusted local environments and prefer a version that pins /usr/bin/ydotool and validates numeric environment settings.

Risk: Agent-controlled clicks, holds, and drags can affect the user's desktop state.

Mitigation: Require explicit user direction before clicks, holds, or drags, and ask for clarification when coordinates or durations are missing or ambiguous.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oguzhaslak/skills/molt-mouse)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Text with shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local desktop input commands for the molt-mouse wrapper and asks for missing or ambiguous coordinates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
