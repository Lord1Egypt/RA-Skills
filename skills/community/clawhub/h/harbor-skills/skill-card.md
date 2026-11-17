## Description:

Harbor Skills helps agents manage Harbor container registries, including projects, images, vulnerability scanning, retention policies, CI/CD and GitOps integration, replication, storage, backup and recovery, webhooks, and compliance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiutoo](https://clawhub.ai/user/qiutoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, and registry administrators use this skill to operate Harbor registries and generate commands, checks, and configuration guidance for routine maintenance, security scanning, cleanup, automation, and recovery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact registry, Kubernetes, credential, and recovery actions could affect production Harbor availability or integrity.

Mitigation: Require operator approval gates before deletion, garbage collection, restore, replication, or account-rotation actions.

Risk: Broad or long-lived credentials could expose Harbor projects or images if mishandled.

Mitigation: Use narrowly scoped robot credentials, avoid logging tokens, and rotate credentials on a defined schedule.

Risk: Unverified hosts, certificates, manifests, or images could route automation to unsafe infrastructure.

Mitigation: Require HTTPS and approved Harbor hosts, verify TLS certificates, and pin Kubernetes manifests and images.

## Reference(s):

- [Harbor API v2.0 Reference](references/harbor-api.md)
- [Image Cleanup Policy](references/cleanup-policy.md)
- [Webhook Event Guide](references/webhook.md)
- [Backup and Recovery](references/backup-recovery.md)
- [GitOps and Harbor Integration](references/gitops.md)
- [Compliance Checks](references/compliance.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, Python, JSON, and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate high-impact Harbor administration commands that require operator review before execution.]

## Skill Version(s):

1.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
