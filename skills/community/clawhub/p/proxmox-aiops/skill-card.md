## Description:

Manage and diagnose Proxmox VE virtual machines, containers, storage, and cluster health with audited operations and recovery support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Proxmox administrators and infrastructure engineers use this skill to inspect cluster and guest health, manage VM and container lifecycles, work with snapshots and backups, and review storage and cluster resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proxmox credentials and audit data are kept in local configuration and state files.

Mitigation: Protect the per-target secret file and local audit data with restrictive permissions, and use a least-privilege Proxmox token for each target.

Risk: VM, container, snapshot, and backup operations can change or remove workload state.

Mitigation: Check the target and preview supported changes with dry-run; take a snapshot or backup before significant changes where appropriate.

Risk: Disabling TLS verification for a Proxmox target weakens server identity checks.

Mitigation: Keep TLS verification enabled except when connecting to a self-signed lab endpoint.

## Reference(s):

- [Setup guide](artifact/references/setup-guide.md)
- [CLI reference](artifact/references/cli-reference.md)
- [Capabilities](artifact/references/capabilities.md)
- [Agent guardrails](artifact/references/agent-guardrails.md)
- [Project homepage](https://github.com/AIops-tools/Proxmox-AIops)

## Skill Output:

**Output Type(s):** [Text, API Calls, Analysis, Shell commands, Configuration instructions]

**Output Format:** [Structured tool results and concise text, with CLI commands and configuration examples in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include Proxmox task identifiers and diagnostic findings with measured values.]

## Skill Version(s):

0.16.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
