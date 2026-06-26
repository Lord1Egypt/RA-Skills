## Description: <br>
Long-term memory management system for maintaining MEMORY.md, consolidating daily memories, and extracting key insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenmeng](https://clawhub.ai/user/shenmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain persistent local memory by consolidating daily notes into MEMORY.md, archiving older logs, extracting key facts, searching memory history, and checking memory health. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory may retain sensitive conversation, account, credential-related, financial, or personal information. <br>
Mitigation: Use the skill only when persistent local memory is intended, avoid storing secrets or unnecessary personal data, and review MEMORY.md and daily logs before consolidation, archiving, summary export, or vector sync. <br>
Risk: Mutating commands can rewrite MEMORY.md or move daily memory files into archives. <br>
Mitigation: Keep a backup before running consolidation or archive commands, and review proposed changes before relying on the updated memory files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shenmeng/longterm-memory-manager) <br>
- [Publisher profile](https://clawhub.ai/user/shenmeng) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline bash commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands read and write local memory files under ~/.openclaw/workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
