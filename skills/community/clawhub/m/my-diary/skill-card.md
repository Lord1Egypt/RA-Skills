## Description: <br>
A personal diary management skill for recording, viewing, searching, and deleting diary entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nancyzhong2024](https://clawhub.ai/user/nancyzhong2024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and assistants use this skill to record, browse, search, and delete personal diary entries stored locally in a JSON file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diary contents are stored in a local plaintext JSON file. <br>
Mitigation: Use a private storage path and protect the file with appropriate local permissions or encryption when entries may be sensitive. <br>
Risk: The skill can display or delete diary entries. <br>
Mitigation: Review prompts before showing entries and require confirmation before deleting an entry. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nancyzhong2024/my-diary) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/nancyzhong2024) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text responses describing diary entries and requested diary actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local plaintext JSON diary file; deletion requires confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
