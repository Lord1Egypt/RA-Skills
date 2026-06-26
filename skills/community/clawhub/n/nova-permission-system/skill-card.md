## Description: <br>
Nova权限系统 provides a local permission and identity workflow for AI assistants, including role-based permission checks, identity verification, approval handling, account binding, and audit logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rancho718](https://clawhub.ai/user/rancho718) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add a local access-control layer around an AI assistant, so non-conversational operations can be checked against configured roles and identities before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authorization checks can fail open or skip checks when configuration, identity fields, or runtime imports are missing. <br>
Mitigation: Change authorization paths to fail closed before relying on the skill for real access control, and test missing-identity, disabled-config, and exception paths. <br>
Risk: The skill stores local identity/profile data, approval data, memories, audit logs, and verification codes. <br>
Mitigation: Hash or remove plaintext codes, avoid echoing secrets in approval messages, and define retention and deletion controls for logs and memory data. <br>
Risk: The installation guidance asks users to add broad workspace-level permission rules. <br>
Mitigation: Narrow the AGENTS.md rules to the specific operations and channels that require this gate, and review them after installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rancho718/nova-permission-system) <br>
- [Installation and system overview](artifact/SKILL.md) <br>
- [Permission check documentation](artifact/permission-check/SKILL.md) <br>
- [Permission gate documentation](artifact/permission-gate/SKILL.md) <br>
- [Identity management documentation](artifact/identity-management/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python snippets, JSON configuration templates, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The installed skill uses local JSON files for users, accounts, permissions, approvals, memories, and audit records.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
