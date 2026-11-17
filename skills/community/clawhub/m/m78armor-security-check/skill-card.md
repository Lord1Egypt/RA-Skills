## Description:

Read-only local OpenClaw security configuration check and hardening assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[move78ai](https://clawhub.ai/user/move78ai)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw operators and developers use this skill after install or upgrade to review local configuration baseline gaps, risky exposure, weak defaults, and drift indicators. It presents practical hardening guidance without claiming certification or host safety.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw configuration to produce security findings.

Mitigation: Install only when local configuration review is intended; do not provide secrets or unrelated files, and prefer a specific config path when scope matters.

Risk: Normal human-readable output includes paid upgrade messaging.

Mitigation: Use the documented --quiet mode for automated or ad-free reporting.

Risk: Findings are configuration checks, not proof that the host is secure.

Mitigation: Treat the results as hardening guidance and review any remediation manually before applying changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/move78ai/skills/m78armor-security-check)
- [Publisher profile](https://clawhub.ai/user/move78ai)
- [M78Armor homepage](https://www.m78armor.com)
- [ClawHub listing copy](references/clawhub-listing-copy.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with inline shell commands; optional JSON from the bundled CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual English/Chinese output, quiet mode for CI, and exit code 1 when high-risk findings are detected.]

## Skill Version(s):

1.0.0 (source: server release metadata and bundled script)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
