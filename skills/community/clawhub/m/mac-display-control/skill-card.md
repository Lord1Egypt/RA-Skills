## Description:

Step-by-step guide for controlling external display settings on macOS from the command line or keyboard shortcuts, including brightness, contrast, volume, input source, color temperature, power, and DDC/CI fallback guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oakland](https://clawhub.ai/user/oakland)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, IT staff, and macOS power users use this skill to set up command-line and keyboard-shortcut control of external monitor settings across Apple Silicon and Intel Macs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags an unverified remote Homebrew installer command.

Mitigation: Use official Homebrew installation instructions or inspect and verify the installer before running it.

Risk: Scheduled cron jobs and keyboard shortcuts can repeatedly change display settings after setup.

Mitigation: Create persistent automation only when desired, document each job or shortcut, and keep removal steps available.

Risk: Display commands for factory reset, input switching, power, and color gain can make disruptive or hard-to-reverse changes.

Mitigation: Test commands manually on the target display before binding them to shortcuts or schedules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oakland/skills/mac-display-control)
- [Brightness control reference](references/brightness.md)
- [Contrast control reference](references/contrast.md)
- [Volume control reference](references/volume.md)
- [Input source switching reference](references/input-source.md)
- [Color temperature reference](references/color-temperature.md)
- [Power and miscellaneous controls reference](references/pow-and-misc.md)
- [m1ddc](https://github.com/waydabber/m1ddc)
- [ddcctl](https://github.com/kfix/ddcctl)
- [MonitorControl README](https://github.com/MonitorControl/MonitorControl#readme)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and script snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup steps, control-specific command examples, automation guidance, and troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
