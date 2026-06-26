## Description: <br>
NOVA Memory helps agents design and operate a three-layer long-term memory system using episodic, semantic, and rules-based memory files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ShaunLeeCN](https://clawhub.ai/user/ShaunLeeCN) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to add structured long-term memory to an AI assistant, including memory folders, an index file, identity records, maintenance routines, and integration notes for OpenClaw-style agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause an agent to persist long-term local memory about users, conversations, identity, and work context. <br>
Mitigation: Enable it only when persistent memory is intended, review stored memory files, and avoid recording secrets or sensitive personal data. <br>
Risk: The skill describes automatic maintenance, cron scheduling, and Git commits for memory updates. <br>
Mitigation: Disable cron jobs and automatic commits unless explicitly desired, and require review before memory maintenance changes are applied. <br>
Risk: The skill may require edits to AGENTS.md and references a helper script that is not included in the artifact. <br>
Mitigation: Review AGENTS.md changes before enabling them and inspect or provide the referenced helper script before running it. <br>


## Reference(s): <br>
- [NOVA Memory on ClawHub](https://clawhub.ai/ShaunLeeCN/nova-three-level-memory) <br>
- [ShaunLeeCN publisher profile](https://clawhub.ai/user/ShaunLeeCN) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with file tree examples, markdown snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent local memory files, scheduled maintenance, AGENTS.md updates, and Git commits.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
