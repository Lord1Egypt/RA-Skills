## Description: <br>
MemPalace provides local AI memory with semantic search over past conversations, a temporal knowledge graph, and palace-style organization for stored memories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanikua](https://clawhub.ai/user/wanikua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use MemPalace to connect an assistant to a local memory store, search prior conversations, manage temporal facts, and write session diary entries for continuity across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically persists and reuses conversation history, which can capture sensitive or unwanted personal context. <br>
Mitigation: Use it only when local long-term memory is intended; verify where data is stored, how diary writes can be disabled, and how saved memories can be reviewed or deleted. <br>
Risk: Stored memories may include credentials, regulated personal data, or confidential business content if users provide that content during conversations. <br>
Mitigation: Avoid using the skill with secrets, regulated personal data, or confidential business content unless appropriate controls, retention limits, and deletion workflows are confirmed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wanikua/mempalace) <br>
- [Publisher profile](https://clawhub.ai/user/wanikua) <br>
- [MemPalace homepage](https://github.com/milla-jovovich/mempalace) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include MCP tool usage instructions, memory search/write recommendations, and local setup commands.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
