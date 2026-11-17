## Description:

Back up and restore Hermes Agent data, including configs, secrets, skills, sessions, memories, cron, and profiles, as portable tar.gz archives with SQLite snapshots, JSON manifests, and integrity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyjohn](https://clawhub.ai/user/anyjohn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Hermes Agent users use this skill to create portable backups, restore Hermes data, and migrate Hermes installations between machines. It is intended for operational backup and recovery of local Hermes configuration, state, profiles, and related user data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backup archives can contain API keys, auth tokens, sessions, memories, profiles, skills, hooks, plugins, and other private Hermes data.

Mitigation: Store archives like credentials, avoid shared locations, prefer encrypted transfer, and restore only archives you created and trust.

Risk: Restore can overwrite persistent Hermes behavior and configuration with files from unvalidated archives.

Mitigation: Use --dry-run first, inspect archives before restoring, and be cautious with --force and custom target options.

Risk: Restoring while Hermes is running can corrupt SQLite databases.

Mitigation: Stop Hermes before restoring or use the documented force flow, then verify database integrity before starting Hermes.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/anyJohn/hermes-backup-restore/tree/main/skills/hermes-backup-restore)
- [Source repository](https://github.com/anyJohn/hermes-backup-restore)
- [Hermes Agent documentation](https://hermes-agent.nousresearch.com)
- [ClawHub skill page](https://clawhub.ai/anyjohn/skills/hermes-backup-restore)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Files, Configuration]

**Output Format:** [Markdown guidance with bash command examples; scripts produce tar.gz backup archives and JSON manifests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run previews are supported; generated backup archives can contain secrets and behavior-changing Hermes data.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
