## Description:

Homebrew package manager for macOS. Search, install, manage, and troubleshoot packages and casks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesethrose](https://clawhub.ai/user/thesethrose)

### License/Terms of Use:


## Use Case:

Developers and macOS users use this skill to have an agent propose Homebrew commands for searching, installing, upgrading, uninstalling, and troubleshooting packages and casks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Homebrew install, upgrade, and uninstall commands can make real changes to the local macOS environment.

Mitigation: Confirm the exact formula or cask names and intended operation before executing generated commands.

Risk: Troubleshooting commands such as brew config can expose local environment details.

Mitigation: Review command output before sharing it externally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thesethrose/skills/homebrew)
- [Official Homebrew Documentation](https://docs.brew.sh)
- [Homebrew Core](https://github.com/Homebrew/homebrew-core)
- [Homebrew Cask](https://github.com/Homebrew/homebrew-cask)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may perform local package installation, upgrade, removal, or troubleshooting actions when executed.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
