## Description:

Lists Huawei Cloud CBR backup vaults in a selected region and presents filtered results as a table, JSON, or a compact name-and-ID inventory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and operations engineers use it to inventory Huawei Cloud CBR backup vaults by region and review vault status, capacity, and charging mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the release suspicious with medium confidence; its partial scan reports automatic quality telemetry collection.

Mitigation: Review the telemetry behavior before use; set SKILL_QUALITY_REPORT=0 to disable telemetry reporting.

Risk: ClawScan reports installation of a separate skill-quality-cli as behavior outside the vault-listing task.

Mitigation: Review the installer and CLI behavior before installing; avoid running the installer until that review is complete.

## Reference(s):

- [KooCLI installation and credential guide](references/cli-installation-guide.md)
- [Read-only CBR IAM policy](references/iam-policies.md)
- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Aligned text table, JSON array, or compact vault name-and-ID list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can be filtered by region, name, status, object type, protection type, enterprise project, or vault ID.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
