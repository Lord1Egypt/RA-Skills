## Description:

Lists Huawei Cloud VPN gateways and IPSec connection states by region, with filters and compact, tabular, or JSON results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud network operators and engineers use this skill to inventory Huawei Cloud VPN gateways, find IPSec connections that are not UP, and inspect results by region, name, status, or gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an additional telemetry tool that can access authenticated commands and raw VPN results; its downloaded code is not bundled.

Mitigation: Review the telemetry tool and its data policy, require a verified release, and use VPN read-only credentials.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/wlc-dev/skills/huawei-cloud-vpn-connection-list)
- [IAM Policies (least privilege, read-only)](artifact/references/iam-policies.md)
- [KooCLI Installation, Credentials & quality CLI](artifact/references/cli-installation-guide.md)
- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Compact text, tables, or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Gateway and connection inventory with filters and a separate view of connections not UP.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
