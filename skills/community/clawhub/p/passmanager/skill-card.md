## Description:

PassManager provides local encrypted credential storage and CLI-based password management for AI assistant teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isenlink](https://clawhub.ai/user/isenlink)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI assistant teams use this skill to manage local credentials, audit credential access, and perform backup or restore workflows without relying on a hosted password service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advertised role-based access controls may not be enforced for sensitive operations.

Mitigation: Review authorization behavior before use with real credentials, limit execution to trusted local users, and avoid restore, delete, and team-management operations until authorization checks are confirmed.

Risk: Master passwords and stored passwords can be exposed through command-line arguments, shell history, process listings, or explicit password display.

Mitigation: Use test secrets until secure prompting is added, avoid passing real secrets on the command line, clear shell history where needed, and avoid password display unless strictly required.

Risk: The local database, key file, backups, and audit logs are high-value files on disk.

Mitigation: Restrict permissions on ~/.passmanager, backups, key material, and logs to the local owner and store backups in a protected location.

## Reference(s):

- [ClawHub PassManager Skill Page](https://clawhub.ai/isenlink/skills/passmanager)
- [PassManager Skill Documentation](artifact/docs/passmanager_skill.md)
- [PassManager Training Manual](artifact/docs/passmanager_training.md)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [AES Encryption Standard](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and CLI text output with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command output can include stored credentials when password display is requested; local database, key, backup, and audit files are written under the configured PassManager directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
