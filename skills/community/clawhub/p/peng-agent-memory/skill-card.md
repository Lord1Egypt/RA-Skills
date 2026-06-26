## Description: <br>
Provides persistent memory for AI agents to remember facts, learn from experience, and track entities across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[penglovemeng](https://clawhub.ai/user/penglovemeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add durable local memory to LLM-powered agents, including fact recall, lesson tracking, entity context, and JSON export across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally stores durable local memory, which can include sensitive facts, entity attributes, or personal preferences if an agent records them. <br>
Mitigation: Avoid storing secrets, credentials, regulated data, or sensitive personal details unless consent and controls are in place; periodically review or delete ~/.agent-memory/memory.db. <br>
Risk: Exported memory data can expose stored facts, lessons, and entity details to other tools or prompts. <br>
Mitigation: Treat export_json output as sensitive data and share it only with trusted tools or workflows. <br>
Risk: The default database path is under the user's home directory and persists across sessions. <br>
Mitigation: Use a protected custom database path for operational use or :memory: for tests and temporary sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/penglovemeng/peng-agent-memory) <br>
- [Publisher profile](https://clawhub.ai/user/penglovemeng) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; runtime APIs return Python objects and JSON-compatible dictionaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores facts, lessons, and entities in a local SQLite database and can export memory contents as JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
