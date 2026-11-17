## Description:

Sync GOG game library, save files, and custom configs across devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use GOG Sync to automate syncing a GOG library, save files, and selected game configuration files across devices and remote backup storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Save files and selected configuration files can be sent to the configured rsync destination.

Mitigation: Set GOG_CONFIG_REMOTE only to a trusted host and review the destination before running sync or sync-config.

Risk: sync-config can copy files from an unintended local directory if GOG_CONFIG_DIR is set incorrectly.

Mitigation: Review GOG_CONFIG_DIR before execution and keep it scoped to the intended GOG configuration directory.

Risk: The evidence notes a mismatch between gogrepo and gogrepoc dependency names.

Mitigation: Verify which dependency is intended before installation or library sync use.

## Reference(s):

- [GOG Sync ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/gog-sync)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Plain text with shell command invocations, terminal status text, and environment variable settings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires rsync; optional library sync depends on the intended GOG repository tool being available.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
