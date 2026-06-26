## Description: <br>
Stores complete OpenClaw conversation history in a local SQLite database, supports search and recall, creates summaries, and syncs extracted decisions to MEMORY.md. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[louch84](https://clawhub.ai/user/louch84) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to retain, search, summarize, and recall local OpenClaw conversation context across sessions while keeping raw messages available in a local database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Complete conversations are retained locally and remain searchable later. <br>
Mitigation: Use only in sessions where local retention is intended, and avoid logging credentials, personal data, confidential business context, or regulated information. <br>
Risk: Extracted decisions may be appended automatically to MEMORY.md without a built-in review or redaction step. <br>
Mitigation: Review MEMORY.md updates regularly and add local redaction, deletion, or retention controls before using the skill with sensitive material. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/louch84/memory-lcm) <br>
- [Publisher profile](https://clawhub.ai/user/louch84) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples, CLI commands, local SQLite storage, and MEMORY.md updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores complete conversation content locally and may append extracted decisions to MEMORY.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
