## Description: <br>
Huawei Cloud CCE Network Failure Diagnoser helps agents diagnose Huawei Cloud CCE Service, DNS/CoreDNS, Ingress, NetworkPolicy, ELB, EIP, NAT, VPC, subnet, security group, and ACL network failures using the bundled Python SDK dispatcher. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to investigate Huawei Cloud CCE network incidents, collect read-only Kubernetes and cloud-side evidence, and produce a Markdown diagnosis report with findings, confidence, recommendations, and verification criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled dispatcher exposes powerful cluster administration and sensitive-data actions beyond the advertised read-only network troubleshooting purpose. <br>
Mitigation: Review and restrict the bundled dispatcher before use; permit only the diagnosis actions needed for the incident workflow. <br>
Risk: The skill requires sensitive Huawei Cloud and Kubernetes credentials. <br>
Mitigation: Use least-privilege read-only Huawei Cloud and Kubernetes credentials, avoid passing AK/SK values on the command line, and tightly control log, secret, and kubeconfig-returning actions. <br>
Risk: Mutating actions may be available through bundled scripts even though the documented network diagnosis workflow is read-only. <br>
Mitigation: Do not run mutating actions unless they have been intentionally audited and approved; keep network changes as reviewed recommendations with rollback and verification criteria. <br>


## Reference(s): <br>
- [Diagnosis workflow](references/workflow.md) <br>
- [Risk rules](references/risk-rules.md) <br>
- [Output schema](references/output-schema.md) <br>
- [Verification method](references/verification-method.md) <br>
- [IAM policies](references/iam-policies.md) <br>
- [Common pitfalls](references/common-pitfalls.md) <br>
- [ClawHub skill page](https://clawhub.ai/pintudeyudi/huawei-cloud-cce-network-failure-diagnoser) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Structured JSON with embedded Markdown diagnosis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include investigation process, evidence matrix, conclusions, confidence levels, recommendations, and verification criteria.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
