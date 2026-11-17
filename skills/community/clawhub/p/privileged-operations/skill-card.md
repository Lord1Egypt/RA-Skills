## Description:

Safely perform Linux tasks that may require root privileges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pinguy](https://clawhub.ai/user/pinguy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent operators use this skill to keep Linux work unprivileged by default and elevate only the specific operation that genuinely needs root. It helps make privileged actions, authentication prompts, and rollback considerations visible before system-level changes are attempted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A proposed privileged command could modify protected system state more broadly than intended.

Mitigation: Review the exact command and reason before approving the visible authentication prompt, and elevate only the narrow protected operation.

Risk: Hidden credential handling or password automation could expose user credentials.

Mitigation: Never ask for, capture, pipe, cache, or automate passwords; use only authentication prompts the user can see and control.

Risk: Destructive privileged operations can be difficult to recover from if the target or rollback path is unclear.

Mitigation: Identify the exact target, validate inputs, create backups or rollback points where practical, and stop when the target cannot be established confidently.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/pinguy/Skills/tree/main/skills/privileged-operations)
- [ClawHub skill listing](https://clawhub.ai/pinguy/skills/privileged-operations)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on visible, narrowly scoped privilege elevation and user-controlled authentication.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
