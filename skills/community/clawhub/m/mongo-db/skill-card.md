## Description:

Mongo Db Client Tool lets agents use a Python CLI to store, query, update, aggregate, and manage documents in MongoDB.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jithinm](https://clawhub.ai/user/jithinm)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to persist structured data in MongoDB, query collections, run aggregation pipelines, and manage collections or indexes across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access data and perform writes allowed by the configured MongoDB account.

Mitigation: Use a dedicated least-privilege MongoDB user and review operations before enabling write or destructive access.

Risk: Database credentials may be placed in local configuration files.

Mitigation: Prefer environment variables or a secret manager over config.json and keep local configuration files out of version control.

Risk: The Ubuntu setup guidance can enable MongoDB as a persistent system service.

Mitigation: Enable mongod at boot only when needed after checking local binding, authentication, and firewall settings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jithinm/skills/mongo-db)
- [INSTALL-UBUNTU.md](INSTALL-UBUNTU.md)
- [MongoDB Ubuntu APT repository](https://repo.mongodb.org/apt/ubuntu)

## Skill Output:

**Output Type(s):** [JSON, shell commands, configuration, guidance]

**Output Format:** [JSON results and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Destructive database operations require explicit confirmation in the JSON payload.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
