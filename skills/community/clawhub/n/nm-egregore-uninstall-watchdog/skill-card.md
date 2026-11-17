## Description:

Removes the egregore watchdog daemon and its associated files

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project maintainers use this skill when removing the egregore watchdog or ending automatic session relaunching. It guides them through platform-specific service cleanup and verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review rates this release suspicious: the uninstall guidance may leave the watchdog running, and scan coverage is partial with disagreement about whether the removal commands match the described behavior.

Mitigation: Review the cleanup steps against the installed service before use, then verify removal with the documented launchd or systemd checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-egregore-uninstall-watchdog)
- [Project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/egregore)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and platform-specific cleanup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [macOS launchd and Linux systemd cleanup steps with verification commands]

## Skill Version(s):

1.10.3 (source: artifact frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
