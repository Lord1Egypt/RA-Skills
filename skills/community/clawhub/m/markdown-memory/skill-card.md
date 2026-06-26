## Description: <br>
Markdown Memory helps AI assistants maintain local Markdown and SQLite-based memories with daily records, long-term notes, session notes, and Ollama embedding search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kk-kingkong](https://clawhub.ai/user/Kk-kingkong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and AI assistants use this skill to keep local, human-readable memory across sessions and retrieve it with local vector search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory can retain private or sensitive user data across sessions. <br>
Mitigation: Avoid storing passwords, tokens, financial details, or other secrets, and periodically review or delete MEMORY.md, USER.md, daily memory files, and any SQLite memory database. <br>


## Reference(s): <br>
- [Markdown Memory on ClawHub](https://clawhub.ai/Kk-kingkong/markdown-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide the agent to create or update local Markdown memory files and SQLite-backed memory data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
