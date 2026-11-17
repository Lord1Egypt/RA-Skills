## Description:

Audit OpenClaw configuration for security risks and generate a remediation report using the user's configured LLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muhammad-waleed381](https://clawhub.ai/user/muhammad-waleed381)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw developers and operators use this skill to audit an OpenClaw configuration file for common security risks and receive a prioritized remediation report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the user's OpenClaw configuration file, which may contain sensitive settings.

Mitigation: Confirm that reading the selected config file is acceptable before installation, and review generated findings without exposing secret values.

Risk: If the user's configured OpenClaw LLM is a hosted provider, redacted findings may still be processed by that provider through the normal OpenClaw setup.

Mitigation: Use a local model or an approved hosted-provider data path for sensitive deployments, and review what metadata is sent for analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/muhammad-waleed381/skills/openclaw-security-auditor)
- [README](README.md)
- [Security Checks](docs/SECURITY-CHECKS.md)
- [Usage](docs/USAGE.md)
- [Installation](docs/INSTALLATION.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown report with a risk score, severity buckets, findings, fix guidance, example configuration, and remediation roadmap]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a default OpenClaw config path of ~/.openclaw/openclaw.json unless the user provides another path; requires cat and jq.]

## Skill Version(s):

1.0.0 (source: server release metadata, changelog, README badge)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
