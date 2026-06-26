## Description: <br>
Stores memory locally with AES-256 encryption and scheduled encrypted backups to reduce leakage and data-loss risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liujw0214](https://clawhub.ai/user/liujw0214) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and enterprise teams use this skill when asking an agent to encrypt local memory, maintain encrypted backups, and restore prior memory backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to manage sensitive memory encryption and scheduled backups without enough implementation detail or user control. <br>
Mitigation: Review before installing and do not rely on it for sensitive memory unless the publisher provides auditable encryption details and clear controls for enabling, disabling, restoring, and deleting backups. <br>
Risk: The local key file is stored separately from encrypted memory but is not itself described as encrypted. <br>
Mitigation: Protect and back up the local key file separately from the backups; loss can make memory unrecoverable and exposure can compromise encrypted memories. <br>
Risk: Scheduled backups can preserve sensitive memory copies beyond the active memory file. <br>
Mitigation: Confirm the backup directory, retention policy, restore flow, and deletion process before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liujw0214/memory-encrypted) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include backup-retention, restore, key-management, and local-path guidance.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
