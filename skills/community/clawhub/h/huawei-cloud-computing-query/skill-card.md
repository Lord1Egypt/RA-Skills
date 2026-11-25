## Description:

Queries Huawei Cloud ECS, BMS, IMS, Auto Scaling, and CCE resources using read-only operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and developers use this skill to inspect Huawei Cloud compute inventories, resource details, available specifications, and quotas. It supports read-only queries across ECS, BMS, IMS, Auto Scaling, and CCE.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reported TLS and package-source weaknesses could expose cloud credentials or returned data.

Mitigation: Pause before installation; review the connection and package-source security, and use least-privilege credentials if proceeding.

Risk: Password retrieval and IAM user listing extend beyond the advertised read-only computing query scope.

Mitigation: Review the relevant commands and permissions before use, and avoid password retrieval or IAM user listing unless explicitly required and authorized.

Risk: Scanner coverage was partial for two environment-check scripts, leaving evidence incomplete.

Mitigation: Review those scripts before installation; the scan does not establish malicious intent or a confirmed package compromise.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-computing-query)
- [ECS Query Guide](artifact/references/ecs/guide.md)
- [BMS Query Guide](artifact/references/bms/guide.md)
- [IMS Query Guide](artifact/references/ims/guide.md)
- [Auto Scaling Query Guide](artifact/references/as/guide.md)
- [CCE Query Guide](artifact/references/cce/guide.md)
- [IAM Policies](artifact/references/iam-policies.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown tables, concise field summaries, or JSON query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only cloud resource inventory and query guidance]

## Skill Version(s):

1.0.9 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
