## Description: <br>
Kubernetes manifest security auditor that scans YAML and JSON manifests for privileged containers, risky host access, RBAC over-permission, plaintext secrets, missing network policy, and related CIS Kubernetes Benchmark and Pod Security Standards issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform engineers, and security teams use this skill to audit Kubernetes manifests in local repositories or CI before deployment. It helps identify container, RBAC, service account, network policy, and service exposure findings with remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit reports may reveal deployment structure, file paths, Kubernetes resource names, and secret-like variable names. <br>
Mitigation: Treat generated reports and CI logs as sensitive and review them before sharing outside the intended team. <br>
Risk: The skill runs local Python code and reads repository directories selected for audit. <br>
Mitigation: Install and run it only in repositories or directories you intend to scan, and install PyYAML from a trusted source. <br>


## Reference(s): <br>
- [Canlah AI](https://canlah.ai) <br>
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes) <br>
- [ClawHub release page](https://clawhub.ai/PHY041/phy-k8s-security-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal audit report or JSON findings, with Markdown guidance and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings include severity, affected resource, check identifier, details, remediation, and CIS or PSS references when available.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
