## Description: <br>
Audit and validate Prisma Access configurations against best practices and security standards. Use when reviewing security policies, checking for misconfigurations, or validating compliance with PAN-OS best practices and CIS benchmarks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leesandao](https://clawhub.ai/user/leesandao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security engineers, network engineers, and compliance reviewers use this skill to audit Prisma Access configuration scope or JSON for policy weaknesses, object hygiene issues, and compliance alignment. It returns prioritized findings with risk and remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security audit recommendations may be incomplete or incorrect if the supplied Prisma Access configuration is partial, stale, or lacks operational context. <br>
Mitigation: Review findings with a qualified Prisma Access administrator and confirm changes against current PAN-OS and CIS guidance before applying them. <br>
Risk: Configuration excerpts can contain sensitive network, policy, or identity details. <br>
Mitigation: Provide only the minimum configuration needed for the audit and redact secrets or sensitive identifiers before sharing outside trusted environments. <br>
Risk: The available ClawScan evidence reports clean scan signals but still advises review before installation. <br>
Mitigation: Review the skill listing, requested permissions, and release evidence before deployment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/leesandao/prisma-audit) <br>
- [Project homepage](https://github.com/leesandao/prismaaccess-skill) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown audit report with severity-tagged findings, a summary score, finding counts, top priorities, and quick wins.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings include description, location, risk, recommendation, and reference fields when supported by the provided configuration.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
