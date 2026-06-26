## Description: <br>
Ollama Memory helps an agent maintain local Markdown and SQLite memory with Ollama embeddings for semantic search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kk-kingkong](https://clawhub.ai/user/Kk-kingkong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to keep durable local assistant notes, long-term memory, user preferences, and daily session records searchable through a local Ollama embedding workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Assistant memory persists on the user's machine and may retain sensitive personal data if the user saves it. <br>
Mitigation: Avoid saving passwords, account tokens, or sensitive personal data unless retention is intentional; periodically review or delete USER.md, MEMORY.md, SOUL.md, daily notes, and any SQLite memory database. <br>
Risk: The artifact references Python memory scripts that are not bundled with the skill. <br>
Mitigation: Review any local memory scripts before running initialization, add, or search commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Kk-kingkong/ollama-memory) <br>
- [Publisher profile](https://clawhub.ai/user/Kk-kingkong) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes local files under ~/.openclaw/workspace and requires python3, sqlite3, and ollama.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
