## Description: <br>
Mark AI Memory Protocol provides persistent, searchable session memory for AI agents using local SQLite storage with no external dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rokkiezeng](https://clawhub.ai/user/rokkiezeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use MAMP to persist, search, and recall conversation history across sessions when an agent needs durable memory beyond the current context window. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Passive auto-recording can capture conversation content without each memory write being explicit. <br>
Mitigation: Prefer explicit add_turn() calls, disable or tightly constrain auto_record, and document when passive capture is enabled. <br>
Risk: Conversation history is persisted locally in plaintext SQLite storage. <br>
Mitigation: Use a dedicated db_path or MARK_MEMORY_DB location with restrictive filesystem permissions and avoid storing secrets, credentials, or regulated data. <br>
Risk: The security evidence says current code contradicts parts of its safety documentation. <br>
Mitigation: Review the published source before deployment and verify claims about cwd-only storage and removal of platform_info persistence. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/rokkiezeng/mamp-memory) <br>
- [Publisher profile](https://clawhub.ai/user/rokkiezeng) <br>
- [MAMP GitHub repository](https://github.com/rokkiezeng/MAMP.git) <br>
- [README.md](artifact/README.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>
- [iteration_guide.md](artifact/iteration_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local SQLite memory operations and agent-facing recall/search guidance; no external API calls are required by the documented workflow.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata, SKILL.md frontmatter, CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
