## Description: <br>
AI-driven Java/Kotlin security audit skill that guides agents through a staged workflow for code metrics, project reconnaissance, full audit, coverage gating, vulnerability validation, Semgrep rule generation, and standardized reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AuroraProudmoore](https://clawhub.ai/user/AuroraProudmoore) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and audit teams use this skill to examine Java and Kotlin codebases for security vulnerabilities, prioritize findings, and produce structured audit reports. It is intended for codebases the user is authorized to scan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads project source code and writes audit reports that may include sensitive code snippets, secrets, or vulnerability details. <br>
Mitigation: Run it only in a controlled workspace for codebases you are authorized to scan, and review generated audit-output files before sharing or storing them outside the project environment. <br>
Risk: The workflow may look up dependency versions online, which can expose private dependency names or versions if used with private projects. <br>
Mitigation: Disable or avoid online dependency lookups for private projects unless that disclosure is acceptable. <br>
Risk: Generated findings and remediation guidance may be incomplete or incorrect, including the specific XStream remediation guidance called out by the security evidence. <br>
Mitigation: Double-check vulnerability evidence and remediation steps before applying fixes, and keep uncertain findings marked for human verification. <br>


## Reference(s): <br>
- [DKTSS scoring system](references/dktss-scoring.md) <br>
- [Vulnerability confirmation conditions](references/vulnerability-conditions.md) <br>
- [Java web security audit checklist](references/security-checklist.md) <br>
- [Standardized report template](references/report-template.md) <br>
- [ClawHub skill page](https://clawhub.ai/AuroraProudmoore/java-audit-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, Semgrep YAML rules, JSON metrics, shell commands, and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write audit-output files such as metrics, tier classification, raw findings, verified findings, and final audit reports.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
