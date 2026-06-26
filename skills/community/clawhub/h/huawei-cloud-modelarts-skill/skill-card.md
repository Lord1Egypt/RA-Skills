## Description: <br>
Huawei Cloud ModelArts platform integration for administering notebooks, pools, node pools, training jobs, inference services, management resources, SWR, VPC, KMS, and Lite Server resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modelarts-agent](https://clawhub.ai/user/modelarts-agent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to let an agent inspect and administer Huawei Cloud ModelArts resources, including notebooks, training jobs, inference services, resource pools, workspace settings, container images, networks, keys, and Lite Server instances. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or delete Huawei Cloud resources. <br>
Mitigation: Use least-privilege, non-production credentials first and require explicit human confirmation before delete, batch delete, reinstall OS, change OS, workspace, quota, and authorization actions. <br>
Risk: Resource mutations may target the wrong project or region. <br>
Mitigation: Verify the project and region before mutating calls and inspect planned changes before execution. <br>
Risk: Exec login results and cluster tokens may contain sensitive access material. <br>
Mitigation: Treat exec login results and cluster tokens as secrets and avoid exposing them in logs, prompts, or shared outputs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/modelarts-agent/huawei-cloud-modelarts-skill) <br>
- [Common Module Reference](references/common.md) <br>
- [Notebook Module Reference](references/notebook.md) <br>
- [Pool Module Reference](references/pool.md) <br>
- [Node Pool Module Reference](references/node_pool.md) <br>
- [Train Module Reference](references/train.md) <br>
- [Infer V1 Module Reference](references/infer_v1.md) <br>
- [Infer V2 Module Reference](references/infer_v2.md) <br>
- [Management Module Reference](references/management.md) <br>
- [SWR Module Reference](references/swr.md) <br>
- [VPC Module Reference](references/vpc.md) <br>
- [KMS Module Reference](references/kms.md) <br>
- [Lite Server Module Reference](references/liteserver.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown, JSON-like API results, Python function calls, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform cloud resource reads, mutations, lifecycle operations, and authenticated Huawei Cloud API calls when invoked by an agent.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
