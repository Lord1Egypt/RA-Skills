## Description:

Query and filter a Huawei Cloud Anti-DDoS protected-IP inventory, including protection status, bound policies, packages, and regions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and developers use this skill to inventory protected IPs in a Huawei Cloud account and check their blocking status, policy, package, and region.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release requires or installs a separate quality telemetry tool for a read-only inventory task, and the security scan reports incomplete coverage.

Mitigation: Avoid installation until the quality tool is optional or removed and its download is independently authenticated; review the component that was only partially inspected.

## Reference(s):

- [Huawei Cloud KooCLI Installation Guide](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [CLI Installation Guide](artifact/references/cli-installation-guide.md)
- [IAM Policies](artifact/references/iam-policies.md)
- [Verification Method](artifact/references/verification-method.md)
- [Acceptance Criteria](artifact/references/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Concise text, a detail table, or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports region, IP, policy, package, and tag filters, with automatic paging.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
