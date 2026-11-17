## Description:

Persistent IRC presence using ii (minimalist file-based IRC client) with event-driven mention detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[destructatron](https://clawhub.ai/user/destructatron)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to set up a persistent IRC bridge with ii, monitor channel mentions, send IRC messages, and trigger OpenClaw events from IRC activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted IRC messages can trigger immediate OpenClaw events.

Mitigation: Use a low-privilege account, restrict server and channel access, avoid sensitive channels, and review who can send messages before enabling the bridge.

Risk: The setup script includes unsafe argument serialization for generated scripts.

Mitigation: Fix the setup script's argument serialization before using untrusted or automated configuration values.

Risk: The bridge creates persistent IRC presence and auto-start behavior when configured with systemd.

Mitigation: Disable auto-start when persistent connectivity is not needed and review the generated service files before deployment.

## Reference(s):

- [ii tools documentation](https://tools.suckless.org/ii/)
- [ii source repository](https://git.suckless.org/ii)
- [ClawHub skill page](https://clawhub.ai/destructatron/skills/ii-irc)
- [ClawHub publisher profile](https://clawhub.ai/user/destructatron)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and generated shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Linux-focused setup guidance and scripts for ii, systemd user services, IRC message sending, and mention monitoring.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
