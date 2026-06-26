## Description: <br>
管理对话上下文和记忆提取。根据关键词高效检索历史记忆。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaxint](https://clawhub.ai/user/jaxint) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to search local memory files by keyword and retrieve recent memory entries for conversation context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper searches local Markdown and JSON files under both memory and skills directories, which can expose sensitive local context if those folders contain secrets. <br>
Mitigation: Keep secrets out of searched folders or narrow SEARCH_DIRS to memory before use when only conversation-memory lookup is intended. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands] <br>
**Output Format:** [Python function return values and plain text CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Searches local Markdown and JSON files under configured memory and skills directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
