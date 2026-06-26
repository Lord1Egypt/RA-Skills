## Description: <br>
Safe Linux firewall hardening with backend detection, idempotent atomic rules, rollback protection, and AI-executable state-machine workflows. Covers ufw, firewalld, nftables, iptables, Docker, Kubernetes CNI awareness, and fail2ban with compliance mapping to CIS/PCI-DSS/SOC2. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[discovery219](https://clawhub.ai/user/discovery219) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and operations teams use this skill to audit, plan, apply, and verify Linux host firewall hardening across common backends. It is intended for controlled server administration workflows that require dry-run planning, rollback preparation, and post-change verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Verification can have side effects, including canceling scheduled rollback or unrelated jobs. <br>
Mitigation: Treat firewall-verify.sh as a mutating finalize step; run it only with console access, a tested second SSH session, backups, and a known rollback timer. <br>
Risk: Firewall changes can lock out SSH or disrupt host networking if applied to the wrong environment or port. <br>
Mitigation: Run the audit and dry-run plan first, confirm the real SSH port, require the approval token before apply, and keep rollback and recovery access available. <br>
Risk: Manual host firewall changes can conflict with Kubernetes, container, cloud firewall, or infrastructure-as-code ownership. <br>
Mitigation: Use audit-only behavior or the documented alternative control plane when the environment is Kubernetes-managed, containerized, cloud-firewall-only, or IaC-managed. <br>


## Reference(s): <br>
- [Backend: UFW](references/backend-ufw.md) <br>
- [Backend: firewalld](references/backend-firewalld.md) <br>
- [Backend: nftables](references/backend-nftables.md) <br>
- [Backend: iptables](references/backend-iptables.md) <br>
- [Security Profiles](references/security-profiles.md) <br>
- [Declarative Firewall Policy](references/declarative-policy.md) <br>
- [Declarative Policy JSON Schema](references/policy-schema.json) <br>
- [Docker Firewall Hardening](references/docker-hardening.md) <br>
- [Kubernetes Node Firewall Policy](references/k8s-policy.md) <br>
- [Special Environments](references/special-environments.md) <br>
- [Recovery Procedures](references/recovery.md) <br>
- [Observability and Performance](references/observability.md) <br>
- [Compliance Mapping](references/compliance.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Bash commands and JSON/YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes machine-readable audit and plan JSON, policy YAML schema, approval tokens, exit code handling, and rollback/verification guidance.] <br>

## Skill Version(s): <br>
2.5.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
