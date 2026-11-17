## Description:

Enterprise-grade security framework for LobsterAI with audit logging, RBAC, input validation, output sanitization, code scanning, and dependency vulnerability detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stoneyhoo](https://clawhub.ai/user/stoneyhoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add security controls to LobsterAI workflows, including audit logging, role-based access control, input validation, output sanitization, and code or dependency scanning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit integration helper can modify other installed skills.

Mitigation: Do not run scripts/integrate_audit.py unless the exact target skills have been reviewed, backups exist, and broad integration is intentional.

Risk: Audit logs can persist sensitive inputs, outputs, or private documents.

Mitigation: Restrict audit log permissions, avoid logging raw secrets, and configure LOBSTERAI_AUDIT_SECRET when tamper-evident signatures are needed.

Risk: All-skill scanning can read code and dependencies across a LobsterAI installation.

Mitigation: Prefer explicit per-skill scanning unless full-installation review is required and the operator trusts the skill source.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/stoneyhoo/skills/lobsterai-security)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [SECURITY.md](artifact/SECURITY.md)
- [TECHNICAL_DOCUMENTATION.md](artifact/TECHNICAL_DOCUMENTATION.md)
- [DEPLOYMENT.md](artifact/DEPLOYMENT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, Python code snippets, shell commands, configuration values, and JSON or JSONL audit and scan data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local audit logs, RBAC configuration, and code or dependency scan reports when invoked.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
