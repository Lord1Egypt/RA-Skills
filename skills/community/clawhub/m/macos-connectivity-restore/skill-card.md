## Description:

Restores Universal Control and AirDrop settings on a managed Mac by resetting the relevant managed preference files and setting AirDrop discoverability to Contacts Only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinntrance](https://clawhub.ai/user/jinntrance)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, IT administrators, and managed Mac support teams use this skill to restore Universal Control and AirDrop settings by applying root-level and user-level macOS preference changes. It can also propose startup jobs to reapply those settings after reboot or login.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The persistence workflow can install a root LaunchDaemon that runs a script from a user-writable skill path.

Mitigation: Avoid installing the persistence workflow unless the root script is copied to a root-owned, non-user-writable location and uninstall steps are available.

Risk: The skill modifies managed macOS preference files and may override organization-managed connectivity policy.

Mitigation: Use it only with appropriate administrative authorization and verify the restored preference values after execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinntrance/skills/macos-connectivity-restore)
- [Publisher profile](https://clawhub.ai/user/jinntrance)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include privileged macOS commands, preference-file changes, verification commands, and optional startup-job installation steps.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
