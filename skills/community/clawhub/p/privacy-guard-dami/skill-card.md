## Description:

Privacy Guard scans OpenClaw logs locally for sensitive data patterns, classifies findings by risk level, and supports review, reporting, and whitelist updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cq2000419](https://clawhub.ai/user/cq2000419)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to scan OpenClaw log files for possible API keys, passwords, personal identifiers, financial data, and other sensitive data before sharing or retaining logs. It also lets users triage suspicious findings and maintain local whitelist state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The published package bundles private runtime logs containing a token-like secret.

Mitigation: Do not install the package as-is; remove bundled logs, rotate the exposed token-like secret, and republish a clean release.

Risk: Generated reports and JSON state can retain unredacted sensitive log snippets.

Mitigation: Store outputs locally with restricted access, review them before sharing, and redact secrets before writing reports or state files.

Risk: Alerting integrations can move detection metadata outside the local machine when configured.

Mitigation: Keep outbound notification webhooks disabled unless approved and verify that outgoing alerts exclude sensitive log content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cq2000419/skills/privacy-guard-dami)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, console text, JSON state files, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local scan reports and suspicious or whitelist state; report snippets may contain sensitive log content unless redacted upstream.]

## Skill Version(s):

0.3.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
