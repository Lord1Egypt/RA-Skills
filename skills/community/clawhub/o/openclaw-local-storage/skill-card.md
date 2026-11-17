## Description:

Openclaw Local Storage uses Node.js and a local JSON file to store records, infer fields from the first record, and handle Chinese-language CRUD commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anbangzhiguo](https://clawhub.ai/user/anbangzhiguo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to manage simple local datasets through Chinese-language add, query, update, and delete commands without connecting to an external database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored records are kept as plaintext in a local JSON file.

Mitigation: Use appropriate filesystem permissions and backups, and avoid storing secrets or sensitive personal data unless those controls are in place.

Risk: Update and delete commands modify the local data file without an undo mechanism.

Mitigation: Review commands before execution and keep a backup of important data before making bulk changes.

Risk: The package declares unnecessary fs and path npm dependencies.

Mitigation: Remove those dependencies before production use when possible, since Node.js already provides fs and path as built-in modules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anbangzhiguo/skills/openclaw-local-storage)
- [Publisher profile](https://clawhub.ai/user/anbangzhiguo)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Guidance]

**Output Format:** [Chinese text responses and JSON-formatted query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads and writes plaintext records in a local JSON file.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
