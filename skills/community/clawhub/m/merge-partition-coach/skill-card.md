## Description:

Merge Partitions Without Data Loss - Combine adjacent or non-adjacent partitions into one larger volume to consolidate space and simplify drive management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hezhaoyun](https://clawhub.ai/user/hezhaoyun)

### License/Terms of Use:

MIT-0

## Use Case:

External Windows users and support agents use this skill to plan and launch a partition merge workflow with EaseUS Partition Master, including pre-checks, command examples, and troubleshooting for adjacent and non-adjacent partition consolidation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead users to install and run disk-management software capable of modifying partitions.

Mitigation: Use it only with a verified backup and recovery plan, and confirm the operation preview before any write operation.

Risk: The bundled installer script downloads and silently runs third-party vendor software.

Mitigation: Prefer manual download from a trusted source with signature or hash verification before running elevated installation.

Risk: Partition merge guidance may be applied to unsupported disk layouts.

Mitigation: Confirm target partitions are on the same basic disk, use supported file systems, and avoid dynamic volumes for this workflow.

## Reference(s):

- [Merge Partition Coach on ClawHub](https://clawhub.ai/hezhaoyun/skills/merge-partition-coach)
- [EaseUS Partition Master](https://www.easeus.com/partition-manager/)
- [EaseUS Partition Master Free download](https://down.easeus.com/product/epm_free?source=skills&dest=merge-partition-coach)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with Windows command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes disk-partition pre-checks, installation guidance, launch commands, and troubleshooting notes.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
