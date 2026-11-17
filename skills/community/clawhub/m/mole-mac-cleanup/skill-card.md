## Description:

Mac cleanup & optimization tool combining CleanMyMac, AppCleaner, DaisyDisk features. Deep cleaning, smart uninstaller, disk insights, and project artifact purge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bjesuiter](https://clawhub.ai/user/bjesuiter)

### License/Terms of Use:


## Use Case:

Developers and macOS users use this skill to have an agent guide Mole commands for previewing and running cleanup, optimization, installer cleanup, and project artifact purge workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup, purge, installer, and optimization commands can remove files or alter system state.

Mitigation: Review Mole dry-run output and exact target paths before allowing non-dry-run execution.

Risk: Broad deletion commands can affect unchecked directories or important project files.

Mitigation: Keep backups for important projects and avoid running broad deletion commands on directories that have not been reviewed.

Risk: Sudo or Touch ID configuration changes can affect local authentication behavior.

Mitigation: Only run sudo or Touch ID setup commands after explicitly confirming the requested system change.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bjesuiter/skills/mole-mac-cleanup)
- [Mole GitHub Repository](https://github.com/tw93/Mole)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [macOS-only guidance for the `mo` command; dry-run review is recommended before cleanup or optimization execution.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
