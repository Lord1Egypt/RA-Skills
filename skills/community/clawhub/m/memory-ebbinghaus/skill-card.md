## Description: <br>
Ebbinghaus forgetting curve memory lifecycle manager for AI agents that calculates memory strength decay and supports review reinforcement, archiving, and deletion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subcoldzhang](https://clawhub.ai/user/subcoldzhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to manage local agent memory records, identify fading memories, and decide whether to review, archive, or delete them. It is useful for lightweight spaced-repetition workflows over project, technical, personal, event, and general memory items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores memory content in a local JSON database and may append archived memories to a Markdown file, so sensitive information could persist if added as a memory. <br>
Mitigation: Set EBBINGHAUS_DB and EBBINGHAUS_ARCHIVE deliberately and avoid storing secrets or sensitive data as memories. <br>
Risk: The forget and archive commands remove items from the active memory list based on an item ID. <br>
Mitigation: Review status output and confirm the intended item ID before running forget or archive. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/subcoldzhang/memory-ebbinghaus) <br>
- [Publisher profile](https://clawhub.ai/user/subcoldzhang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local JSON memory database and can append archived memories to a Markdown file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
