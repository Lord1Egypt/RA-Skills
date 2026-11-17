## Description:

Plans Huawei Cloud CCE Kubernetes cluster upgrades by assessing upgrade paths, addon compatibility, pre-upgrade checks, version-specific risks, upgrade windows, and execution previews with two-step confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pintudeyudi](https://clawhub.ai/user/pintudeyudi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud platform engineers use this skill to plan Huawei Cloud CCE Kubernetes version upgrades, estimate maintenance windows, check compatibility, and generate reviewed hcloud command previews before changing clusters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Preview sections include live hcloud upgrade commands that could change production CCE clusters if executed.

Mitigation: Use read-only or least-privileged Huawei Cloud credentials for assessment and require explicit approval for the exact cluster, region, target version, and operation before running UpgradeCluster, CreateUpgradeWorkFlow, UpgradeNodePool, UpdateAddonInstance, pause, retry, continue, or cancellation commands.

Risk: Incorrect upgrade-path, pre-check, or addon compatibility guidance could lead to failed upgrades or service interruption.

Mitigation: Verify hcloud dry-run behavior and command help independently, run CCE pre-upgrade checks, follow supported version paths, and review rollback plus post-upgrade verification steps before execution.

## Reference(s):

- [Upgrade Workflow](references/upgrade-workflow.md)
- [Pre-Upgrade Checklist](references/pre-upgrade-checklist.md)
- [Addon Compatibility and Upgrade Order](references/addon-compatibility.md)
- [CCE Kubernetes Version Upgrade Path Matrix](references/k8s-version-matrix.md)
- [Upgrade Window Estimation](references/upgrade-window-estimation.md)
- [Risk Rules and Guardrails](references/risk-rules.md)
- [Output Schema](references/output-schema.md)
- [Huawei Cloud CCE Cluster Upgrade](https://support.huaweicloud.com/usermanual-cce/cce_10_0197.html)
- [Huawei Cloud CCE Pre-Upgrade Checks](https://support.huaweicloud.com/usermanual-cce/cce_10_0549.html)
- [Huawei Cloud CCE Version Lifecycle](https://support.huaweicloud.com/bulletin-cce/cce_bulletin_0043.html)
- [Huawei Cloud CCE PSP Configuration](https://support.huaweicloud.com/usermanual-cce/cce_10_0466.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and JSON-style assessment reports with hcloud CLI command previews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes confirmation-required execution previews, rollback planning, and post-upgrade verification guidance.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
