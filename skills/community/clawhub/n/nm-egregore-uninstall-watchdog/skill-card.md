## Description:

Removes the egregore watchdog daemon and its associated files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when they want to stop automatic egregore session relaunching or remove the watchdog before removing the egregore plugin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Linux cleanup may remove the watchdog unit files while leaving an already running service active; the scan was also partial because a referenced path was missing.

Mitigation: Review the Linux cleanup sequence, confirm both the timer and service are stopped before removing their unit files, and verify the watchdog is inactive afterward. Treat the partial scan as incomplete assurance.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/athola/skills/nm-egregore-uninstall-watchdog)
- [Homepage listed in skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/egregore)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Platform-specific macOS and Linux cleanup and verification steps.]

## Skill Version(s):

1.10.4 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
