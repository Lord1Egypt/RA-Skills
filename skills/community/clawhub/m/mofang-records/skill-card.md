## Description: <br>
Mofang Records helps agents use a bundled Node.js CLI to manage Magicflu/Mofang web-table records and BPM workflow tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[magicscape](https://clawhub.ai/user/magicscape) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operations teams, and agents use this skill to list spaces and forms, inspect field definitions, query or change records, and act on BPM tasks in Magicflu/Mofang environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, delete, complete, delegate, claim, jump, and transact on records or BPM tasks. <br>
Mitigation: Require explicit review of record IDs, task IDs, targets, and consequences before write, delete, BPM, or transaction operations. <br>
Risk: The skill needs Magicflu/Mofang server credentials. <br>
Mitigation: Use a dedicated least-privilege account and keep passwords in a secure environment or secret store rather than a shared .env file. <br>
Risk: Ambiguous space or form names can target the wrong data. <br>
Mitigation: Prefer read-only discovery first, pass spaceHint when available, and inspect field definitions before create or update operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/magicscape/mofang-records) <br>
- [Publisher profile](https://clawhub.ai/user/magicscape) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI commands return JSON with success, message, and data fields; write, delete, and BPM actions require explicit review.] <br>

## Skill Version(s): <br>
3.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
