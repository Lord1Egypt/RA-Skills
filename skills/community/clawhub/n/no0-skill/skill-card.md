## Description:

Monitors and protects AI agent identity and sensitive data by detecting tampering and enforcing access control with rollback and audit capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanghaoyu-xiaolu](https://clawhub.ai/user/wanghaoyu-xiaolu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use No.0-skill to monitor AI agent cognitive files, review or roll back tampering, and optionally add local data access controls, authorization, MFA, and audit logging for sensitive environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approval controls are weak according to the security summary.

Mitigation: Use only in test or isolated environments until the approval service, MFA flow, and interceptor fail-open behavior are fixed.

Risk: Testing code can alter protected cognitive files.

Mitigation: Do not run the tamper simulator against real cognitive files; test only with disposable files or isolated workspaces.

Risk: Backup and cleanup behavior can affect local No.0 runtime state.

Mitigation: Back up ~/.openclaw/no0 before running cleanup or uninstall commands.

Risk: DLC dependencies are not pinned to exact versions.

Mitigation: Review and pin dependency versions in a controlled environment before deployment.

## Reference(s):

- [No.0-skill ClawHub page](https://clawhub.ai/wanghaoyu-xiaolu/skills/no0-skill)
- [Publisher profile](https://clawhub.ai/user/wanghaoyu-xiaolu)
- [Project site](https://skill.lawgenesis.cn)
- [Installation Guide](INSTALL.md)
- [Quickstart](QUICKSTART.md)
- [No.0 Event Schema](docs/event_schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, CLI examples, and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local operational guidance for installing, running, auditing, and rolling back No.0 Core and optional DLC controls.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
