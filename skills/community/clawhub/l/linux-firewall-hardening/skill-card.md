## Description:

Safe Linux firewall hardening with backend detection, idempotent atomic rules, rollback protection, and AI-executable state-machine workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[discovery219](https://clawhub.ai/user/discovery219)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, system administrators, and security engineers use this skill to audit Linux firewall posture, plan safe rule changes, and produce confirmed firewall hardening steps for supported Linux firewall backends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rollback and verification scripts can make broad privileged firewall changes that are not safely scoped.

Mitigation: Treat the release as a Review install, inspect scripts before running them, use a maintenance window, and avoid apply/verify automation on production hosts until rollback cancellation and plan-state handling are tightened.

Risk: Firewall changes can lock out remote SSH access.

Mitigation: Use only systems with console access, keep a second tested SSH session open, require explicit plan-token confirmation before apply, and complete verification before cancelling rollback protection.

Risk: Emergency fallback commands can expose the host by accepting all input traffic and flushing firewall rules.

Mitigation: Do not let an agent execute the emergency rollback fallback automatically; reserve it for a human operator using serial console access and re-harden immediately afterward.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/discovery219/skills/linux-firewall-hardening)
- [UFW Backend Guide](references/backend-ufw.md)
- [firewalld Backend Guide](references/backend-firewalld.md)
- [nftables Backend Guide](references/backend-nftables.md)
- [iptables Backend Guide](references/backend-iptables.md)
- [Declarative Firewall Policy](references/declarative-policy.md)
- [Docker Firewall Hardening](references/docker-hardening.md)
- [Kubernetes Node Firewall Policy](references/k8s-policy.md)
- [firewall-apply.sh](references/firewall-apply.md)
- [Recovery Procedures](references/recovery.md)
- [Security Profiles](references/security-profiles.md)
- [Special Environments](references/special-environments.md)
- [Compliance Mapping](references/compliance.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON/YAML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires human confirmation before firewall changes and separate verification before committing changes.]

## Skill Version(s):

2.7.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
