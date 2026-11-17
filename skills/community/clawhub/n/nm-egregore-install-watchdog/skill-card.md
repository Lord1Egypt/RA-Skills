## Description:

Installs egregore watchdog daemon via launchd or systemd for autonomous relaunching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill after initializing an egregore project or while setting up a new machine to install and verify a user-level watchdog that relaunches sessions every five minutes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment rates the skill suspicious with medium confidence: its stated watchdog purpose does not match reported status checks, and its setup persists across sessions. The referenced install scripts were missing from the scan, so their behavior remains unassessed.

Mitigation: Before installing, review or obtain the install scripts and confirm that you want a watchdog configured to relaunch every five minutes and persist across sessions.

## Reference(s):

- [Egregore project page](https://github.com/athola/claude-night-market/tree/master/plugins/egregore)
- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-egregore-install-watchdog)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
