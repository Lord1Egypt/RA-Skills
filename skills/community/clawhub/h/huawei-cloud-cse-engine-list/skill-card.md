## Description:

Lists Huawei Cloud CSE microservice engines in a selected region and returns concise, table, or JSON inventory results using KooCLI or the official Python SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud developers and operators can inventory CSE, Nacos, and MicroGateway engines in a Huawei Cloud region and review their versions, statuses, and capacity. They can filter by type or name and use the results for operational audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags environment-controlled command settings that could run arbitrary programs with the process's cloud credentials.

Mitigation: Avoid installation or use until command overrides are addressed. If approved for use, run with isolated, least-privilege credentials scoped to cse:engine:list.

Risk: The security assessment flags a pagination flaw that may produce an incomplete engine inventory.

Mitigation: Do not treat results as complete until pagination behavior is corrected and verified; cross-check inventory totals against Huawei Cloud.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wlc-dev/skills/huawei-cloud-cse-engine-list)
- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Verification method and API details](artifact/references/verification-method.md)
- [Least-privilege IAM policy](artifact/references/iam-policies.md)
- [CLI installation and credential guide](artifact/references/cli-installation-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain-text inventory, full-field table, or normalized JSON array]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Region-scoped engine records with name, ID, type, version, status, flavor, instance counts, creation time, and region; supports type and name filters.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
