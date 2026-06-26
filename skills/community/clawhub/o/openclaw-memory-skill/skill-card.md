## Description: <br>
MongoDB-backed long-term semantic memory for recalling, storing, searching, and managing facts, decisions, and user preferences across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrlynn](https://clawhub.ai/user/mrlynn) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to persist, search, retrieve, list, and delete long-term memories across sessions. It supports semantic recall of facts, decisions, preferences, and project context through a MongoDB-backed memory service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically save and re-use conversation details across sessions through an external memory service. <br>
Mitigation: Install only when long-term memory is intended, avoid storing secrets or regulated personal data, review or delete stored memories periodically, and disable hooks when memory should be saved only by explicit user action. <br>
Risk: Stored memories may reside in local or cloud-hosted MongoDB depending on deployment configuration. <br>
Mitigation: Confirm where MongoDB is hosted before use and verify the external plugin and daemon source before relying on the memory service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrlynn/openclaw-memory-skill) <br>
- [Publisher profile](https://clawhub.ai/user/mrlynn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON, TypeScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent guidance for memory search, storage, retrieval, deletion, listing, status checks, hook behavior, configuration, installation, and troubleshooting.] <br>

## Skill Version(s): <br>
0.2.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
