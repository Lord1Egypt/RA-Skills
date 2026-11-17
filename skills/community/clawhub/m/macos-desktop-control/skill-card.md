## Description:

Automates macOS desktop interactions by capturing screenshots and executing precise mouse movements, clicks, and keyboard inputs via cliclick.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emptyopen](https://clawhub.ai/user/emptyopen)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to let an agent inspect a live macOS desktop, identify UI element positions, and issue mouse or keyboard actions during GUI automation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent live screen capture plus mouse and keyboard control in a macOS desktop session.

Mitigation: Use only in a trusted session, keep sensitive windows and credentials out of view, and review proposed actions before allowing desktop control.

Risk: Screenshots are written to a fixed temporary path without documented cleanup.

Mitigation: Harden screenshot storage with a private randomized temporary path, restrictive permissions, exit-status checks, and cleanup after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/emptyopen/skills/macos-desktop-control)
- [Publisher profile](https://clawhub.ai/user/emptyopen)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The screenshot wrapper writes a PNG file to /tmp/claw_view.png, and desktop actions affect the live macOS session.]

## Skill Version(s):

1.0.0 (source: evidence release metadata and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
