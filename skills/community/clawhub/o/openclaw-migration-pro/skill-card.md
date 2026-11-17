## Description:

OpenClaw Migration Pro helps users analyze, package, transfer, and restore OpenClaw skills, memory, configuration, and cron jobs when moving an environment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yankj](https://clawhub.ai/user/yankj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to migrate an OpenClaw environment between machines by analyzing local assets, packaging skills, memory, configuration, and cron jobs, transferring the package, and restoring it in a target environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Migration bundles can contain broad private OpenClaw data and may be automatically sent to the current channel.

Mitigation: Review the archive contents and destination before transfer, and use --no-send or another controlled transfer method for private backups.

Risk: Artifact documentation is inconsistent about whether credentials and API keys are excluded or packed.

Mitigation: Do not include credentials or API keys in migration bundles; reconfigure secrets separately after restore.

Risk: Installation examples include pipe-to-bash and unpinned npx commands.

Mitigation: Review installation sources before execution, avoid pipe-to-bash, and pin package versions where possible.

Risk: Restoring configuration and cron jobs into an active environment can change scheduled behavior or overwrite local state.

Mitigation: Restore only into a controlled environment after inspecting MANIFEST.json, configuration files, and cron job definitions.

## Reference(s):

- [Openclaw Migration Pro ClawHub Page](https://clawhub.ai/yankj/skills/openclaw-migration-pro)
- [Skill Definition](artifact/SKILL.md)
- [README](artifact/README.md)
- [Migration Guide](artifact/MIGRATION-GUIDE.md)
- [Capability Report](artifact/CAPABILITY-REPORT.md)
- [Compression Complete Report](artifact/COMPRESSION-COMPLETE-REPORT.md)
- [Exclude Strategy](artifact/EXCLUDE-STRATEGY.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Files]

**Output Format:** [Markdown guidance with bash command examples and generated migration files such as MANIFEST.json and backup archives]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or restore local archives, configuration files, memory files, skills, and cron job definitions.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
