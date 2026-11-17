## Description:

Manage operations with mandatory user confirmation, permission checks, explicit method adherence, and clear choices before execution on sensitive system tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangwud1](https://clawhub.ai/user/zhangwud1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when an agent is asked to perform sensitive system work such as elevated commands, file deletion or modification, package installation, service management, user management, or configuration changes. It helps the agent verify resources, present clear options, wait for explicit confirmation, and report failures without silently switching methods.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runnable examples include broad sudo command execution and destructive file deletion patterns.

Mitigation: Review each proposed command before execution, prefer least-privilege or reversible options, confirm target paths, and create backups before changing system files.

Risk: The included shell template accepts sudo passwords as arguments or prompt input.

Mitigation: Do not provide sudo passwords through chat, command-line arguments, or skill prompts; authenticate manually in a trusted terminal when elevated access is required.

Risk: The skill can guide changes to system services, packages, user accounts, databases, and configuration files.

Mitigation: Require explicit user confirmation, inspect the exact command or edit plan, use dry-run or show-only options when available, and verify results after execution.

## Reference(s):

- [Detailed Scenarios for Optional Strict Instructions](references/scenarios.md)
- [ClawHub skill page](https://clawhub.ai/zhangwud1/skills/optional-strict-instructions)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation for sensitive actions; included shell scripts are templates/examples that should be reviewed before execution.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
