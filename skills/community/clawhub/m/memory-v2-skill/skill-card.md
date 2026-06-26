## Description: <br>
Memory Lucia is a local SQLite-based memory system for OpenClaw agents that tracks priorities, learning progress, decisions, skill evolution, local text search, and automatic database backups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wen521](https://clawhub.ai/user/wen521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add persistent local memory to OpenClaw agents, including priority tracking, learning status, decision records, skill usage history, search, and backup workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation-derived memory and backup files can contain sensitive local data. <br>
Mitigation: Keep the SQLite database and backups out of shared folders and apply local access controls appropriate for the data being stored. <br>
Risk: Local search activity may expose sensitive queries in local logs or retained memory. <br>
Mitigation: Avoid searching for secrets or credentials and review retained memory before using the skill in sensitive environments. <br>
Risk: The skill depends on npm packages for local SQLite access. <br>
Mitigation: Pin and audit dependencies before deployment in controlled or sensitive environments. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/wen521/memory-v2-skill) <br>
- [API Reference](references/API.md) <br>
- [npm Package](https://www.npmjs.com/package/memory-lucia) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation, JavaScript API calls, shell commands, and SQLite-backed text or JSON-like query results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores conversation-derived memory locally in SQLite and may retain backup copies.] <br>

## Skill Version(s): <br>
2.5.4 (source: server release evidence, SKILL.md frontmatter, package.json, README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
