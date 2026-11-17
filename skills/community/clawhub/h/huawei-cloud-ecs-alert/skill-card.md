## Description:

Automates batch creation and management of Huawei Cloud CES alarm rules for ECS instances using hcloud CLI v7.2.2+.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to configure ECS monitoring alarms, manage SMN notification subscriptions, and query CES metrics across Huawei Cloud ECS instances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make Huawei Cloud changes, including creating CES alarms, updating alarm notifications, and deleting SMN subscriptions, and the security evidence reports no enforced confirmation gate.

Mitigation: Require manual review of target resources and operation details before running any create, update, or delete script; use dry-run mode where available and verify results after execution.

Risk: Production Huawei Cloud credentials may be exposed or overused if pasted into chat, stored in command history, or granted broad permissions.

Mitigation: Use hcloud configure or approved per-call credential handling, do not paste AK/SK into chat or shell history, and prefer least-privilege IAM policies over broad FullAccess where possible.

Risk: Deleting an SMN subscription can interrupt alarm notifications.

Mitigation: Treat SMN subscription deletion as a high-impact operation, confirm the subscription URN and notification dependency before execution, and verify active subscriptions afterward.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-ecs-alert)
- [CLI installation guide](references/cli-installation-guide.md)
- [IAM policies](references/iam-policies.md)
- [Related APIs](references/related-apis.md)
- [SMN subscription guide](references/smn-subscription-guide.md)
- [Troubleshooting](references/troubleshooting.md)
- [CES API reference](https://support.huaweicloud.com/api-ces/ces_03_0001.html)
- [SMN API reference](https://support.huaweicloud.com/api-smn/smn-api-170301001.html)
- [ECS API reference](https://support.huaweicloud.com/api-ecs/ecs_01_0100.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON or table command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dry-run guidance and verification steps for Huawei Cloud CLI operations.]

## Skill Version(s):

1.0.4 (source: server release evidence; artifact frontmatter is 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
