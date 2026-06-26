## Description: <br>
Interact with a MongoDB database for persistent document storage, including CRUD operations, aggregation pipelines, collection management, and index creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JithinM](https://clawhub.ai/user/JithinM) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to connect to MongoDB, persist structured documents, query records, run aggregations, and manage collections or indexes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, write, and persist MongoDB records. <br>
Mitigation: Use a dedicated least-privilege MongoDB user scoped to the intended database and collections. <br>
Risk: Bulk updates, upserts, schema or index changes, deletes, and collection drops can significantly alter stored data. <br>
Mitigation: Require explicit review before these operations and only pass confirmation flags after the user has approved the action. <br>
Risk: Database content may include secrets, personal data, or regulated records. <br>
Mitigation: Avoid storing sensitive or regulated data unless retention, access control, and deletion requirements are already defined. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JithinM/mongo-db) <br>
- [Publisher profile](https://clawhub.ai/user/JithinM) <br>
- [MongoDB Ubuntu installation notes](INSTALL-UBUNTU.md) <br>
- [MongoDB Community Server package repository](https://repo.mongodb.org/apt/ubuntu) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown instructions with JSON payloads, shell commands, and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The MongoDB client returns JSON success or error objects and serializes ObjectId fields as strings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
