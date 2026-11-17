## Description:

Protect OpenClaw installations from prompt injection, data exfiltration, malicious skills, and workspace tampering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylejfrost](https://clawhub.ai/user/kylejfrost)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to audit OpenClaw skill files, monitor installed skill integrity, check outbound data-flow patterns, and apply basic workspace hardening controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local hardening tools may be mistaken for a complete security boundary.

Mitigation: Treat the outputs as advisory and keep manual review in the approval process for skills, workspace changes, and outbound access.

Risk: The authoritative security scan reports bypass flaws in the install guard and URL whitelist that can make unsafe skills appear clean.

Mitigation: Do not rely on install-guard.sh as the sole approval gate until those bypass issues are fixed and retested.

Risk: Workspace hardening actions can modify file permissions, .gitignore entries, and local security directories.

Mitigation: Review reported changes before running fix modes, and run check-only modes first in shared or sensitive workspaces.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/kylejfrost/skills/openclaw-security-hardening)
- [Security rules template](assets/security-rules-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and local shell report output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local hash baselines, whitelist entries, permission changes, .gitignore updates, and incident-log directories when users run the provided scripts with write-oriented options.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
