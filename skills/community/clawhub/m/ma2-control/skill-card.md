## Description:

Ma2 Control helps an agent control a physical grandMA2 lighting console over Telnet for fixture selection, dimming, cue storage, playback, and status queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[y1035211-cloud](https://clawhub.ai/user/y1035211-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

External lighting operators and technicians use this skill to have an agent prepare and send grandMA2 console commands through a local bridge for programming, playback, and diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands can change a real lighting console, live equipment state, and show files.

Mitigation: Use the skill only when MA2 control is intended, test in an offline or rehearsal environment first, and require explicit operator confirmation for Store, Assign, Go, Goto, overwrite, /noconfirm, Move, Copy, and Delete commands.

Risk: The skill depends on local bridge scripts to send Telnet commands to the console.

Mitigation: Review the bridge scripts before use, keep them in a protected location, and verify the bridge health before sending commands.

Risk: Incorrect console IP, port, or Remote settings can cause failed or misdirected control attempts.

Mitigation: Confirm the console IP, Telnet port, network segment, and Remote setting before operation.

## Reference(s):

- [MA2 command syntax](references/MA2_COMMAND_SYNTAX.md)
- [MA2 command templates](references/MA2_TEMPLATES.md)
- [MA2 troubleshooting guide](references/MA2_TROUBLESHOOTING.md)
- [ClawHub skill page](https://clawhub.ai/y1035211-cloud/skills/ma2-control)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON command templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include commands intended for a local grandMA2 bridge script.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
