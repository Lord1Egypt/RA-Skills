## Description: <br>
Helps an agent read, search, create, update, delete, merge, back up, and restore entries in the local macOS Contacts address book. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leocdchina](https://clawhub.ai/user/leocdchina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent needs to inspect or manage a user's native macOS Contacts records, including search, duplicate checks, precise identifier-based edits, and backup-backed maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify, delete, merge, back up, and restore macOS Contacts. <br>
Mitigation: Use it only when the user intentionally wants Contacts maintenance, and require explicit confirmation of contact identifiers and fields before mutating operations. <br>
Risk: Restore operations can overwrite the current address book, and backups contain private contact data. <br>
Mitigation: Treat restore as high risk, confirm the backup path and expected result before use, and store or dispose of backups according to the user's privacy requirements. <br>
Risk: Broad dedupe or merge requests can remove or combine the wrong contact records. <br>
Mitigation: Plan duplicate changes first, inspect keep and drop identifiers, and wrap applied merge or delete operations with the transaction helper. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leocdchina/openclaw-macos-contacts) <br>
- [Production notes](artifact/references/production-notes.md) <br>
- [Schema notes](artifact/references/schema-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return structured contact records, operation status, backup paths, and rollback results.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
