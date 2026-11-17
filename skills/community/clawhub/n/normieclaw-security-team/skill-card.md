## Description:

Automates security, platform, and memory audits for OpenClaw environments and reports findings that need attention.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use Security Team to run local audits of OpenClaw environments, check service health, track accepted risks, and receive concise remediation guidance for security, platform, and memory findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security review says the main scanner scripts are broken.

Mitigation: Review before installing and do not rely on the skill for monitoring until syntax checks and a baseline run succeed.

Risk: The server security review says privacy claims are overstated, and npm audit can disclose dependency metadata to the configured npm registry.

Mitigation: Configure narrow scan directories and review npm registry disclosure expectations before running dependency audits.

Risk: The artifact includes promotional cross-sell instructions that can appear in security reports.

Mitigation: Remove or ignore cross-sell instructions when reports must remain limited to security findings and remediation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nollio/skills/normieclaw-security-team)
- [README](README.md)
- [Security guarantees](SECURITY.md)
- [Security Team operating manual](SKILL.md)
- [Security configuration](config/security-config.json)
- [Dashboard companion spec](dashboard-kit/DASHBOARD-SPEC.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown or plain-text audit reports, JSON scanner output, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are intended to redact raw secrets and prioritize critical findings first.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
