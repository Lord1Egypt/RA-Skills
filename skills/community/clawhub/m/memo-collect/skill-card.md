## Description: <br>
This is a simple skill for note-taking, used to quickly record user notes, and provide users with query, delete, and other capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bondli](https://clawhub.ai/user/bondli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to add, list, and delete lightweight local memo notes during normal assistant workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memos are stored in a local file that may contain user-provided sensitive information. <br>
Mitigation: Avoid storing secrets or hard-to-recreate information in memos and review local storage expectations before installing. <br>
Risk: Deleting a numbered memo removes it immediately and no recovery step is documented. <br>
Mitigation: List memos before deletion and confirm the intended item number before invoking delete_memo. <br>


## Reference(s): <br>
- [README.md](README.md) <br>
- [ClawHub release page](https://clawhub.ai/bondli/memo-collect) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text command output and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates a local JSON memo file; delete actions remove memos immediately by number.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
