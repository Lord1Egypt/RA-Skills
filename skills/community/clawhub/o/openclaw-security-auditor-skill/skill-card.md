## Description:

OpenClaw Security Auditor (OSA) audits OpenClaw deployments by scanning configuration, scoring security risk, generating Chinese/English reports, and suggesting remediation steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albertlsy588](https://clawhub.ai/user/albertlsy588)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to assess OpenClaw configuration posture, identify security issues, and receive remediation guidance before deployment or during routine audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner depends on external Python code that the release evidence identifies as unreviewed and not pinned.

Mitigation: Pin and verify the external `osa` dependency before using scan results for security decisions.

Risk: The configuration fixer can persistently edit OpenClaw configuration files.

Mitigation: Use dry-run behavior first, review intended changes, keep backups, and apply edits only with explicit user approval.

Risk: The aggressive security profile disables authentication and expands permissions for testing.

Mitigation: Use the aggressive profile only in disposable isolated environments and never with sensitive data or untrusted networks.

## Reference(s):

- [OpenClaw Security Configuration Guide](artifact/references/config-guide.md)
- [OpenClaw Security Modes](artifact/references/security-modes.md)
- [ClawHub skill page](https://clawhub.ai/albertlsy588/skills/openclaw-security-auditor-skill)
- [Publisher profile](https://clawhub.ai/user/albertlsy588)

## Skill Output:

**Output Type(s):** [text, markdown, json, html, shell commands, configuration, guidance]

**Output Format:** [Markdown, bilingual Markdown, JSON, or HTML reports with risk scores, issue details, fix commands, and configuration recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include severity levels, passed and failed check counts, current and recommended values, and mode-specific security guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
