## Description:

A macOS terminal setup skill for configuring, migrating, theming, diagnosing, and removing a shell and terminal environment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huiyonghkw](https://clawhub.ai/user/huiyonghkw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using macOS terminals can use it to configure or migrate iTerm2 and zsh, apply themes, diagnose setup, sync settings to another machine, and uninstall or restore its changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags the installer path and configuration, cleanup, and rollback behavior as meaningful risks, and the scan was incomplete.

Mitigation: Review the installer and cleanup behavior before running scripts, then inspect planned changes with --dry-run and keep the scripts' confirmation prompts enabled.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huiyonghkw/skills/hekouwang-terminal-lite-skill)
- [Project home (English)](https://huiyonghkw.github.io/hekouwang-terminal-lite-skill/index.html?lang=en)
- [Project guide (English)](https://huiyonghkw.github.io/hekouwang-terminal-lite-skill/guide/index.html?lang=en)
- [First-run guide](references/first-run.md)
- [English manual](docs/manual.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration files, Configuration instructions, Guidance]

**Output Format:** [Shell commands with configuration changes and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions target macOS terminal and shell settings; installation needs network access and scripts can modify local preferences and configuration.]

## Skill Version(s):

3.0.6 (source: SKILL.md frontmatter, VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
