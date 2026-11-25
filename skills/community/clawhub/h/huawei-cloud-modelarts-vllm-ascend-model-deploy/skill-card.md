## Description:

Guides developers through deploying open-source language models on Huawei Cloud ModelArts with vLLM-Ascend on Ascend NPUs, from deployment planning through service verification.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to prepare model weights and container images, choose a supported deployment form, configure a ModelArts online inference service, and verify its OpenAI-compatible API. The source describes the workflow for validation and prototyping and advises against direct production use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports TLS and credential exposure risks.

Mitigation: Review and decide whether to accept the reported transport and credential risks before installing; keep credentials out of chat and logs.

Risk: The security guidance reports public inference access and root-level host changes as deployment concerns.

Mitigation: Review access controls and host changes before deployment.

Risk: The security guidance identifies deployment image and installer trust risks.

Mitigation: Review and establish trust in the selected image and installer sources before installing.

Risk: Security inspection was incomplete: 67 of 68 components were covered, one was partially inspected, and a static analyzer was degraded.

Mitigation: Treat the scan evidence as incomplete and review the affected components before installation.

## Reference(s):

- [Huawei Cloud ModelArts vLLM-Ascend deployment best practice](https://support.huaweicloud.com/intl/zh-cn/bestpractice-modelarts/modelarts_10_3121.html)
- [Huawei Cloud CreateInferService API](https://support.huaweicloud.com/api-modelarts/CreateInferService.html)
- [vLLM-Ascend model documentation](https://docs.vllm.ai/projects/ascend/zh-cn/latest/tutorials/models/)
- [Deployment form decision guide](artifact/references/deployment-form-decision.md)
- [IAM policies guide](artifact/references/iam-policies.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown guidance with shell scripts, Python examples, and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Model-specific; depends on the confirmed hardware, deployment form, and model documentation.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
