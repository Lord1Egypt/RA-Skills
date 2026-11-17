## Description:

Lists public NAT gateways in a Huawei Cloud tenant region through KooCLI, with an SDK fallback, filtering, paging, and table or JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud developers and operators use this skill to inspect and filter public NAT gateways in a Huawei Cloud region, including gateway IDs and associated VPCs, for inventory and operations checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found read-only safeguard bypasses and unchecked region values that could direct the credentialed SDK client outside Huawei Cloud. Real cloud execution and the downloaded installer remain unverified.

Mitigation: Remove or restrict production executable overrides, validate regions against trusted endpoints, use dedicated credentials limited to nat:natGateways:list, configure credentials outside chat, and install KooCLI from a verified vendor distribution.

## Reference(s):

- [Huawei Cloud KooCLI NAT command reference](https://support.huaweicloud.com/clir-natgateway/nat-cli.html)
- [Least-privilege IAM policy](artifact/references/iam-policies.md)
- [KooCLI installation and credential guide](artifact/references/cli-installation-guide.md)
- [ClawHub release page](https://clawhub.ai/wlc-dev/skills/huawei-cloud-nat-list)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Full-field table, raw JSON array, or compact list of gateway names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports region and gateway filters with automatic marker paging.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
