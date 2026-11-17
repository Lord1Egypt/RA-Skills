## Description:

Queries Huawei Cloud network resources across VPC, EIP, ELB, NAT, VPN, and DNS using read-only local Python scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inventory Huawei Cloud network resources, inspect topology and configuration, and retrieve reusable identifiers for verification or automation planning. It is limited to queries and does not create, modify, or delete cloud resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mandatory setup may run local code and install dependencies before queries are performed.

Mitigation: Review the skill before installing, use an isolated environment, and make dependency installation explicit and user-controlled.

Risk: HTTPS handling and credential traffic are flagged as review-worthy by the security evidence.

Mitigation: Use least-privilege, read-only Huawei Cloud credentials and avoid running setup until TLS verification is restored.

Risk: Credential-bearing environment variables are required for Huawei Cloud queries.

Mitigation: Use temporary or scoped credentials where possible and do not expose access keys, secret keys, or security tokens in outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-network-query)
- [DNS Python Script Usage Guide](references/dns/guide.md)
- [EIP Python Script Usage Guide](references/eip/guide.md)
- [ELB Python Script Usage Guide](references/elb/guide.md)
- [NAT Gateway Python Script Usage Guide](references/nat/guide.md)
- [VPC Python Script Usage Guide](references/vpc/guide.md)
- [VPN Python Script Usage Guide](references/vpn/guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with script commands and JSON query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query results commonly include total counts and item lists with resource IDs, names, statuses, and service-specific fields.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
