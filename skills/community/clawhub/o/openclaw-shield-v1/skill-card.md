## Description:

OpenClaw Shield is a cloud security guardrail for Codex and OpenClaw workflows that checks commands, file operations, network requests, and package installs before execution, classifies source trust, tracks taint, blocks metadata endpoints, and redacts sensitive output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eilaiwangwh](https://clawhub.ai/user/eilaiwangwh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to guide agent handling of shell commands, file operations, network requests, and package installation in cloud-server workflows. It is intended to support source-trust classification, sensitive-output redaction, metadata endpoint blocking, and audit expectations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release describes security enforcement behavior, but the authoritative security evidence says the promised shield.py implementation is absent and documented to fail open.

Mitigation: Treat the current package as documentation-only until an implementation is supplied, pinned, tested, and invoked through a safe non-shell interface.

Risk: The artifact asks users to append broad persistent agent rules to SOUL.md or AGENTS.md, which can change agent behavior across future sessions.

Mitigation: Review those persistent rules before installation and do not append them unless the enforcement script and rollback process have been verified.

## Reference(s):

- [OpenClaw Shield Skill Page](https://clawhub.ai/eilaiwangwh/skills/openclaw-shield-v1)
- [Permission Matrix](references/permission-matrix.md)
- [Detection and Redaction](references/detection-and-redaction.md)
- [Cloud Boundaries Config](references/cloud-boundaries-config.md)
- [Audit and Playbook](references/audit-and-playbook.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed pass, warn, confirm, or block decisions, redaction guidance, and audit checklist steps.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
