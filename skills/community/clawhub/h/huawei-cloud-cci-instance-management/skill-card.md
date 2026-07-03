## Description: <br>
Huawei Cloud CCI (Cloud Container Instance) full lifecycle management using hcloud CLI for namespaces, networks, deployments, stateful sets, pods, EIPPools, logs, and metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to plan and run Huawei Cloud CCI lifecycle tasks through hcloud CLI commands and the bundled network helper. It supports creating, inspecting, updating, scaling, logging, and deleting CCI namespaces, networks, workloads, pods, and EIPPools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide high-impact Huawei Cloud CCI administration, including destructive deletes and broader operations than its stated lifecycle purpose. <br>
Mitigation: Use a least-privilege Huawei Cloud profile in a non-critical or tightly scoped project, and require explicit two-step confirmation before any delete action. <br>
Risk: The bundled Python helper performs direct CCI API calls for network create, delete, and status operations and has command-safety concerns noted by the security evidence. <br>
Mitigation: Review the helper before running it, avoid untrusted region values, and independently confirm delete targets before using the helper delete action. <br>
Risk: Logs, events, and secret-related operations can expose sensitive operational data. <br>
Mitigation: Treat status, event, log, and credential-adjacent outputs as sensitive; do not expose Huawei Cloud AK/SK values in prompts, commands, or responses. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pintudeyudi/huawei-cloud-cci-instance-management) <br>
- [CCI Common Workflows](references/common-workflows.md) <br>
- [CCI Operation Catalog](references/cci-operation-catalog.md) <br>
- [IAM Permission Policies for CCI Operations](references/iam-policies.md) <br>
- [CCI Parameter Format Rules](references/parameter-format.md) <br>
- [Step-by-Step Verification Process for CCI Skill Functionality](references/verification-method.md) <br>
- [Troubleshooting Guide for CCI hcloud CLI Issues](references/troubleshooting.md) <br>
- [Huawei Cloud CCI Network API Documentation](https://support.huaweicloud.com/api-cci/createNetworkingCciIoV1beta1NamespacedNetwork.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include hcloud CLI commands, JSON output recommendations, confirmation steps for destructive operations, and Python helper usage.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
