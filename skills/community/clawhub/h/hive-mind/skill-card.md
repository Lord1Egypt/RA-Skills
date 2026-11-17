## Description:

Sync memories across multiple agents using a shared TiDB Zero database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilyjazz](https://clawhub.ai/user/lilyjazz)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to persist small key-value preferences and recall them across agent sessions, devices, or team agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent user preferences and database credentials may be stored or reused with insufficient consent, scoping, or protection.

Mitigation: Use only non-sensitive preferences, provide tightly scoped TiDB credentials, restrict the database account, and avoid storing secrets, private identifiers, financial, health, or confidential work data.

Risk: Auto-provisioning can create a remote TiDB Zero database and cache the DSN locally.

Mitigation: Prefer bring-your-own TiDB credentials; if auto-provisioning is used, accept the remote service dependency and remove or protect ~/.openclaw_hive_mind_dsn.

Risk: Stored data may expire when using the temporary database fallback.

Mitigation: Use a persistent TiDB Cloud Serverless database for durable storage rather than relying on the documented 30-day temporary database behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lilyjazz/skills/hive-mind)
- [TiDB Zero instance API endpoint](https://zero.tidbapi.com/v1alpha1/instances)
- [PROTOCOL.md](artifact/PROTOCOL.md)
- [DESIGN.md](artifact/DESIGN.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores and retrieves preference keys and values through set, get, and list actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
