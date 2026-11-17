## Description:

Lists and filters Huawei Cloud MapReduce Service clusters through KooCLI, returning a full-field table, JSON array, or compact cluster-name list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud developers and operators use this skill to inspect MRS cluster inventory by region and optional name or state filters. It can support routine inventory checks and provide cluster identifiers for follow-on work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command overrides can exceed the advertised read-only scope.

Mitigation: Leave both MRS_LIST_HCLOUD_* overrides unset, use a trusted KooCLI executable, and configure a dedicated read-only cloud identity outside chat.

Risk: The installer source needs verification.

Mitigation: Obtain KooCLI through Huawei's official instructions and verify its checksum.

Risk: Cluster details appear in agent output.

Mitigation: Use the skill only where the resulting cluster inventory is appropriate to display.

## Reference(s):

- [Acceptance Criteria](artifact/references/acceptance-criteria.md)
- [KooCLI Installation and Credential Guide](artifact/references/cli-installation-guide.md)
- [Huawei Cloud KooCLI Quick Start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Least-Privilege IAM Policy](artifact/references/iam-policies.md)
- [Data Flow Diagram](artifact/references/dataflow-diagram.md)
- [Verification Method](artifact/references/verification-method.md)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Full-field text table, JSON array, or cluster-name list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports region, cluster state, and cluster name filters; paginates results.]

## Skill Version(s):

1.0.5 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
