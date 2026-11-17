## Description:

AI-driven Java and Kotlin security audit skill that guides agents through systematic vulnerability discovery, coverage checks, verification, rule creation, and standardized reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auroraproudmoore](https://clawhub.ai/user/auroraproudmoore)

### License/Terms of Use:

MIT-0

## Use Case:

Security engineers and developers use this skill to audit Java and Kotlin repositories for vulnerabilities, prioritize findings, and produce reviewable security reports. It is suited to repository security assessments, pre-CI/CD vulnerability discovery, and audit methodology standardization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent must read the target Java or Kotlin repository and write audit outputs.

Mitigation: Install and run the skill only in workspaces where that repository access and report generation are intended.

Risk: Generated coverage numbers and final reports may be advisory rather than complete.

Mitigation: Manually verify important findings, call chains, and coverage before relying on the report.

Risk: Proprietary source code could be exposed if an external vector store or service is used during audit workflows.

Mitigation: Use isolated environments and approve any external data flow before sending code outside the local workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/auroraproudmoore/skills/java-audit-skill)
- [DKTSS scoring reference](references/dktss-scoring.md)
- [Vulnerability confirmation conditions](references/vulnerability-conditions.md)
- [Security audit checklist](references/security-checklist.md)
- [Standard report template](references/report-template.md)
- [Semgrep rules reference](rules/semgrep/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON metrics, Semgrep YAML rules, and shell/Python command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces advisory audit artifacts that should be reviewed before security or release decisions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
