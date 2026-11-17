## Description:

Guides developers through deploying open-source language models with vLLM-Ascend as online inference services on Huawei Cloud ModelArts.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to prepare model weights and images, select a deployment topology, configure ModelArts online services, and verify OpenAI-compatible inference on Ascend NPUs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports serious transport and credential-handling risks.

Mitigation: Before considering use, have a qualified reviewer examine the network and credential-handling behavior.

Risk: The security guidance calls out proxy access controls and host-level changes for review.

Mitigation: Have a qualified reviewer examine proxy access controls and host-impacting behavior before use.

Risk: The security guidance calls out model-code settings and the bundled wheel’s provenance for review.

Mitigation: Have a qualified reviewer inspect model-code settings and verify the bundled wheel’s provenance before considering use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-modelarts-vllm-ascend-model-deploy)
- [vLLM-Ascend model deployment documentation](https://docs.vllm.ai/projects/ascend/zh-cn/latest/tutorials/models/)
- [Huawei Cloud ModelArts deployment best practice](https://support.huaweicloud.com/intl/zh-cn/bestpractice-modelarts/modelarts_10_3121.html)
- [Huawei Cloud CreateInferService API](https://support.huaweicloud.com/api-modelarts/CreateInferService.html)
- [vLLM-Ascend image repository](https://quay.io/repository/ascend/vllm-ascend)
- [Deployment form decision guide](references/deployment-form-decision.md)
- [IAM policies and token guidance](references/iam-policies.md)
- [Verification method](references/verification-method.md)
- [Troubleshooting guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with shell commands, Python examples, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance and templates cover single-node, multi-node, and prefill/decode disaggregated deployments.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
