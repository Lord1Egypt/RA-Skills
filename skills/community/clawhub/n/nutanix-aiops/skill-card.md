## Description:

Helps agents inspect and operate Nutanix Prism Central v4 estates, including clusters, virtual machines, storage, disaster recovery, alerts, upgrades, and capacity diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Infrastructure operators and developers use this skill to investigate Nutanix estate health and alerts, manage virtual machines and storage, and carry out Prism Central maintenance and disaster recovery tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Destructive actions can affect production infrastructure without an in-skill approval gate or read-only mode.

Mitigation: Start with a read-only Prism account, separate test and production targets, and require human approval before granting credentials for delete, restore, failover, migration, or updates.

Risk: A master password used for non-interactive access could be exposed through logs or CI output.

Mitigation: Keep NUTANIX_AIOPS_MASTER_PASSWORD out of logs and CI output.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zw008/skills/nutanix-aiops)
- [Project homepage (skill metadata; import provenance unavailable)](https://github.com/AIops-tools/Nutanix-AIops)
- [Capabilities and tool reference](artifact/references/capabilities.md)
- [Setup and security guide](artifact/references/setup-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Text or Markdown with command examples and structured tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes estate findings, operational guidance, and action summaries.]

## Skill Version(s):

0.13.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
