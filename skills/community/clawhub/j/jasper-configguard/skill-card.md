## Description: <br>
Safe config changes for OpenClaw with automatic rollback, backups before patching, health checks after restart, and commands for patching, restoring, listing, diffing, validating, and doctor checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emberDesire](https://clawhub.ai/user/emberDesire) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to safely modify OpenClaw gateway configuration from an agent, CLI, or JavaScript API while keeping backups and rollback paths available. It is intended for local OpenClaw configuration management tasks such as model changes, plugin enablement, validation, backup restore, and gateway health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit OpenClaw configuration and signal a gateway restart, so an incorrect patch can disrupt the local gateway. <br>
Mitigation: Use --dry-run first, review the generated patch or diff before applying it, and use --no-restart when service signaling is not desired. <br>
Risk: Configuration backups may contain tokens or private provider settings when openclaw.json includes sensitive values. <br>
Mitigation: Protect access to ~/.openclaw/config-backups and apply the same local file-permission controls used for the primary OpenClaw configuration. <br>
Risk: Array values are replaced rather than merged, which can remove existing entries if a patch omits them. <br>
Mitigation: When patching arrays, include the full intended array contents and inspect the dry-run diff before applying. <br>


## Reference(s): <br>
- [Jasper ConfigGuard ClawHub Page](https://clawhub.ai/emberDesire/jasper-configguard) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Product Homepage](https://exohaven.online/products/jasper-configguard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command guidance, JSON configuration patch examples, diff previews, backup and restore instructions, validation results, and local health-check status.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
