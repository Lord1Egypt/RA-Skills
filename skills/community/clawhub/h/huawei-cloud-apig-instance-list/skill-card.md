## Description:

Lists Huawei Cloud APIG dedicated instances and, optionally, their APIs, with filters and compact, table, or JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inspect Huawei Cloud APIG dedicated instances and list the APIs belonging to a selected instance. It helps with read-only inventory checks across a chosen Huawei Cloud region.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer and external dependency contents have not been audited.

Mitigation: Obtain KooCLI through Huawei's documented downloads and verify its integrity before installation; review installer and dependency contents.

Risk: Executable and extra-argument environment overrides can change the command that runs.

Mitigation: Remove or restrict APIG_LIST_HCLOUD_BIN and APIG_LIST_HCLOUD_ARGS; keep both unset in trusted environments.

Risk: The SDK reads configured cloud credentials into memory.

Mitigation: Use read-only, least-privilege credentials configured outside chat, and do not share secrets in prompts.

## Reference(s):

- [KooCLI installation and credential guide](artifact/references/cli-installation-guide.md)
- [Read-only IAM policies](artifact/references/iam-policies.md)
- [Data flow diagram](artifact/references/dataflow-diagram.md)
- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Compact text, a fixed-column table, or JSON records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports region selection, filters, instance API drill-down, and result limits.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
