## Description:

Diagnoses Huawei Cloud CCE network connectivity, DNS/CoreDNS, Ingress, NetworkPolicy, ELB backend, EIP, NAT, and VPC failures and produces Markdown diagnosis reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pintudeyudi](https://clawhub.ai/user/pintudeyudi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to investigate Huawei Cloud CCE Service reachability, DNS, Ingress, NetworkPolicy, ELB, EIP, NAT, and VPC network failures. It gathers read-only diagnostic evidence and returns structured findings with a Markdown report, confidence levels, recommendations, and verification criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server security review reports that the skill describes read-only network diagnosis while its shipped dispatcher can run broad cloud administration actions.

Mitigation: Review before installing and restrict execution to the documented read-only network diagnostic actions before use with real Huawei Cloud or Kubernetes credentials.

Risk: Server security review reports potential exposure of Kubernetes secrets.

Mitigation: Avoid production or write-capable credentials until the publisher removes Secret data access; if real credentials were already used, rotate exposed credentials and review agent logs for secret output.

Risk: Server security review calls out dependency pinning and certificate/TLS handling concerns.

Mitigation: Pin dependencies and fix certificate/TLS handling before deployment in production environments.

## Reference(s):

- [Skill page](https://clawhub.ai/pintudeyudi/skills/huawei-cloud-cce-network-failure-diagnoser)
- [Workflow](references/workflow.md)
- [Risk Rules](references/risk-rules.md)
- [Output Schema](references/output-schema.md)
- [IAM Policies](references/iam-policies.md)
- [Verification Method](references/verification-method.md)
- [Common Pitfalls](references/common-pitfalls.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Structured JSON with embedded Markdown diagnosis report and read-only verification guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include findings, snapshots, top causes, confidence values, recommendations, and verification criteria.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
