## Description:

Creates and manages isolated OpenClaw rescue Gateway instances with automatic port allocation and macOS LaunchAgent setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangkai258](https://clawhub.ai/user/yangkai258)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create, batch-create, check, and remove isolated OpenClaw Gateway rescue instances for fallback operation, environment separation, and multi-configuration testing on macOS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates macOS user-level background services that auto-start and restart.

Mitigation: Require explicit user opt-in for persistence, review generated LaunchAgent plist files before loading them, and unload services that are no longer needed.

Risk: Unsafe instance input or deletion handling could affect unrelated user files.

Mitigation: Validate instance names and ports strictly, resolve canonical paths before file operations, and require confirmation before deleting rescue directories or service files.

Risk: Copied OpenClaw configuration files may include sensitive or environment-specific settings.

Mitigation: Generate minimal non-secret rescue configuration where possible, review copied configuration before startup, and keep credentials isolated per instance.

## Reference(s):

- [Quick Reference](artifact/references/quick-reference.md)
- [Multiple Gateways](/gateway/multiple-gateways)
- [Gateway Configuration](/gateway/configuration)
- [CLI Gateway](/cli/gateway)
- [ClawHub Skill Page](https://clawhub.ai/yangkai258/skills/openclaw-rescue-instances)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When scripts are executed, they create OpenClaw rescue directories, LaunchAgent plist files, logs, and copied configuration files.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
