## Description:

Guides engineers through preparing, running, and analyzing a Huawei Cloud CCE availability-zone outage drill by stopping and restarting cluster nodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to prepare controlled Huawei Cloud CCE availability-zone fault drills, observe workload failover, restore nodes, and review impact reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Executing the drill stops CCE nodes in an availability zone and may disrupt workloads.

Mitigation: Use a controlled target, confirm cluster and availability zone with a human, run a dry run first, and require explicit approval before live execution.

Risk: The execution path does not enforce the documented confirmation and compatibility gates.

Mitigation: Manually verify that validation.json is current and all_compatible=true before any non-dry-run execution; keep recovery steps ready.

Risk: Broad cloud credentials or a shared kubeconfig can expand the impact of the drill.

Mitigation: Use least-privilege Huawei credentials and a temporary KUBECONFIG rather than /root/.kube/config.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cce-chaos-experiment)
- [CCE validation rules](references/cce-validation-rules.md)
- [Experiment execution workflow](references/execution-workflow.md)
- [Huawei Cloud KooCLI installation guide](https://support.huaweicloud.com/developer-hcli/hcli_02_0001.html)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Markdown]

**Output Format:** [Text guidance and commands; JSON experiment files and logs; Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can prepare local experiment files, run an outage drill, and produce execution and impact reports.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
