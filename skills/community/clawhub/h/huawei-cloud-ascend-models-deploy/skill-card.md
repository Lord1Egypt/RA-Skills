## Description:

Deploys and tests large language, vision-language, embedding, and rerank models on Huawei Cloud Ascend DevServer 910B systems, including command generation, model catalog matching, inference testing, log viewing, and status monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan, generate, review, and run commands for deploying supported models on Huawei Cloud Ascend DevServer 910B infrastructure, then test inference endpoints and inspect deployment status or logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to run remote shell scripts downloaded from Huawei OBS on user servers.

Mitigation: Use the skill only when the OBS-hosted scripts are trusted or have been pre-staged and verified; review every generated command before execution.

Risk: Detached deployment jobs can keep running after the initiating session ends and may consume NPU, memory, disk, or network resources.

Mitigation: Maintain a stop and cleanup plan for background deployment processes, logs, and downloaded scripts before starting deployment.

Risk: SSH access to important servers increases impact if commands are wrong or over-privileged.

Mitigation: Run with the least-privileged practical account and confirm target host, port, model, card count, and deployment directory before execution.

## Reference(s):

- [Task: Deploy Model](references/task-deploy-model.md)
- [Task: Test Model](references/task-test-model.md)
- [Model Catalog](references/model-catalog.md)
- [API Parameters](references/api-parameters.md)
- [Prerequisites](references/prerequisites.md)
- [Verification Method](references/verification-method.md)
- [Troubleshooting](references/troubleshooting.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Model matching helper](scripts/deploy_helper.py)
- [Huawei Cloud OBS deployment scripts](https://documentation-samples-17.obs.cn-north-9.myhuaweicloud.com/solution-as-code-publicbucket/solution-as-code-module/quickly-deploy-llm-on-modelarts-lite-devserver/userdata)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash, JSON, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce SSH deployment commands, nohup background jobs, API test requests, model matching JSON, and deployment status summaries.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
