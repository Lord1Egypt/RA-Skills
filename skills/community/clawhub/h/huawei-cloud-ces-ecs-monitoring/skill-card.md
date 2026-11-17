## Description:

Monitors Huawei Cloud ECS instances with Cloud Eye Service by querying current and historical CPU, memory, disk, network, and system metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use the skill to inspect ECS resource utilization, review metric history, and troubleshoot performance issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags permissions that extend to server control and account-user information, which exceed basic metric monitoring needs.

Mitigation: Use a dedicated, project-scoped role with only the minimum read-only monitoring permissions; authorize server actions and alarm or tag changes separately when needed.

Risk: The external CLI installer and image payloads mentioned in the guidance were not reviewed in the security evidence.

Mitigation: Verify installer and image provenance before use, and keep saved profiles and inventory caches private.

## Reference(s):

- [CES Metrics Reference](artifact/references/ces-metrics-reference.md)
- [IAM Policies](artifact/references/iam-policies.md)
- [KooCLI Command Reference](artifact/references/related-commands.md)
- [KooCLI Installation Guide](artifact/references/cli-installation-guide.md)
- [Monitoring Best Practices](artifact/references/best-practices.md)
- [Troubleshooting Guide](artifact/references/troubleshooting-guide.md)
- [Huawei Cloud ECS User Guide](https://support.huaweicloud.com/usermanual-ecs/ecs_03_1001.html)
- [Huawei Cloud KooCLI Documentation](https://support.huaweicloud.com/function-hcli/index.html)
- [ClawHub Skill Release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-ces-ecs-monitoring)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Guidance]

**Output Format:** [Markdown with metric summaries and inline hcloud command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected ECS instances, metrics, region, and time range.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
