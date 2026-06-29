## Description: <br>
Configure, deploy, and verify Huawei Cloud CCE to CCI 2.0 bursting for fast elastic capacity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud platform engineers use this skill to prepare Huawei Cloud CCE clusters for bursting workloads into CCI 2.0 capacity, including VPCEP dependencies, virtual-kubelet setup, smoke workload deployment, and readiness diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package exposes broader Huawei Cloud and Kubernetes authority than CCE-CCI bursting alone. <br>
Mitigation: Install only with a least-privilege IAM user and grant only the cloud and Kubernetes permissions required for the intended workflow. <br>
Risk: Sensitive Huawei Cloud AK/SK credentials may be exposed if passed directly in commands or persisted in files. <br>
Mitigation: Use environment variables or approved secret handling, avoid command-line AK/SK parameters where possible, and never write credentials to reports, debug files, shell history, or skill files. <br>
Risk: Infrastructure-changing actions can create billed endpoints, alter addons, resize node pools, or deploy workloads. <br>
Mitigation: Run preview commands first and apply only after reviewing the plan and giving explicit confirm=true approval. <br>
Risk: Incorrect subnet IDs or guessed OBS endpoint service names can break the bursting setup. <br>
Mitigation: Use precheck output to distinguish cci_subnet_id from vpcep_subnet_id and obtain the exact OBS endpoint service name through the Huawei Cloud service ticket. <br>


## Reference(s): <br>
- [CCE to CCI 2.0 Bursting Workflow](references/workflow.md) <br>
- [Risk Rules](references/risk-rules.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [CCI 2.0 environment configuration](https://support.huaweicloud.com/intl/zh-cn/usermanual-cci2/cci_01_0024.html) <br>
- [CCI 2.0 cloud bursting setup](https://support.huaweicloud.com/intl/zh-cn/usermanual-cci2/cci_01_0025.html) <br>
- [CCE cloud native hybrid deployment addon](https://support.huaweicloud.com/usermanual-cce/cce_10_0135.html) <br>
- [CCI image pulling FAQ](https://support.huaweicloud.com/intl/en-us/cci_faq/cci_faq_0095.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Analysis] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preview-first workflow; infrastructure-changing actions require explicit confirm=true approval.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
