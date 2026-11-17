## Description:

Huawei Cloud ModelArts platform integration with modular resource management, OBS notebook storage support, environment-variable authentication, pool plugin management, and node configuration template queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modelarts-agent](https://clawhub.ai/user/modelarts-agent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to manage Huawei Cloud ModelArts resources, including notebooks, resource pools, node pools, training jobs, inference services, workspaces, VPC resources, KMS keypairs, SWR image repositories, and LiteServer instances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad Huawei ModelArts administration authority.

Mitigation: Install it only in a Huawei Cloud project where agent-driven ModelArts administration is acceptable, and use narrowly scoped cloud permissions.

Risk: Authentication tokens or exec login data may be exposed by token-returning helpers despite credential-hiding claims.

Mitigation: Avoid production credentials until token-returning exec and authentication helpers are removed, disabled, or redacted.

Risk: The skill can perform destructive cloud operations such as deleting services, jobs, pools, notebooks, buckets, and LiteServer resources.

Mitigation: Require narrow resource IDs and explicit confirmation before destructive actions.

## Reference(s):

- [Huawei Cloud ModelArts Skill on ClawHub](https://clawhub.ai/modelarts-agent/skills/huawei-cloud-modelarts-skill)
- [Common Module Reference](artifact/references/common.md)
- [Notebook Module Reference](artifact/references/notebook.md)
- [Resource Pool Module Reference](artifact/references/pool.md)
- [Node Pool Module Reference](artifact/references/node_pool.md)
- [Training Module Reference](artifact/references/train.md)
- [Inference V1 Module Reference](artifact/references/infer_v1.md)
- [Inference V2 Module Reference](artifact/references/infer_v2.md)
- [Management Module Reference](artifact/references/management.md)
- [SWR Module Reference](artifact/references/swr.md)
- [VPC Module Reference](artifact/references/vpc.md)
- [KMS Module Reference](artifact/references/kms.md)
- [LiteServer Module Reference](artifact/references/liteserver.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and structured cloud API result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include resource IDs, status details, and masked cloud API responses.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
