## Description: <br>
Huawei Cloud Ascend model deployment and testing skill for large language models on Ascend DevServer (910B series). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaweiclouddev](https://clawhub.ai/user/huaweiclouddev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to deploy, test, and monitor LLM, vision-language, embedding, and rerank models on Huawei Cloud Ascend DevServer 910B systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated deployment commands download and run remote Huawei Cloud deployment scripts without integrity checks. <br>
Mitigation: Inspect or pin the downloaded scripts before execution, verify the script source, and require explicit user confirmation before running deployment commands. <br>
Risk: Deployment commands can start services and write under /home/modelarts-agent on the target DevServer. <br>
Mitigation: Use a least-privileged deployment account, confirm the target host and port, and define a stop or rollback process before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huaweiclouddev/huawei-cloud-ascend-models-deploy) <br>
- [Deployment task steps](references/task-deploy-model.md) <br>
- [Testing task steps](references/task-test-model.md) <br>
- [Model catalog](references/model-catalog.md) <br>
- [API parameter reference](references/api-parameters.md) <br>
- [Prerequisites checklist](references/prerequisites.md) <br>
- [Verification method](references/verification-method.md) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>
- [Model matching helper](scripts/deploy_helper.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates deployment commands, inference test requests, log checks, status checks, and prerequisite validation guidance.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
