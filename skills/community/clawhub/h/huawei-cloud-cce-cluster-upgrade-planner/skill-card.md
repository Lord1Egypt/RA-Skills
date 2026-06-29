## Description: <br>
Plans Huawei Cloud CCE Kubernetes cluster upgrades by assessing upgrade paths, pre-checks, addon compatibility, breaking changes, deprecated APIs, upgrade windows, migration strategy, and execution previews with two-step confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to plan Huawei Cloud CCE cluster upgrades, validate version and addon compatibility, estimate maintenance windows, and generate reviewable hcloud command previews before making production changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated hcloud upgrade commands can trigger high-impact Huawei CCE changes if executed. <br>
Mitigation: Treat UpgradeCluster, UpgradeNodePool, UpdateAddonInstance, CreateUpgradeWorkFlow, pause, retry, continue, and cancel commands as production-changing guidance; manually verify exact hcloud behavior and explicitly approve execution. <br>
Risk: Execution previews are protected by instruction-level two-step confirmation rather than an independently verified safe dry run. <br>
Mitigation: Review every command, parameter, cluster ID, region, target version, addon operation, and node operation before running anything in a live environment. <br>
Risk: Cloud credentials could be exposed if access keys are copied into prompts, commands, or outputs. <br>
Mitigation: Use hcloud profile configuration or environment variables, and check only credential presence with hcloud configure list. <br>


## Reference(s): <br>
- [Upgrade Workflow](references/upgrade-workflow.md) <br>
- [Pre-Upgrade Checklist](references/pre-upgrade-checklist.md) <br>
- [Addon Compatibility and Upgrade Order](references/addon-compatibility.md) <br>
- [CCE Kubernetes Version Upgrade Path Matrix](references/k8s-version-matrix.md) <br>
- [Upgrade Window Estimation](references/upgrade-window-estimation.md) <br>
- [Risk Rules and Guardrails](references/risk-rules.md) <br>
- [Output Schema](references/output-schema.md) <br>
- [Huawei Cloud CCE cluster upgrade documentation](https://support.huaweicloud.com/usermanual-cce/cce_10_0197.html) <br>
- [Huawei Cloud CCE pre-upgrade checks](https://support.huaweicloud.com/usermanual-cce/cce_10_0549.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON assessment sections and inline hcloud shell command previews] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated upgrade commands require manual review and explicit approval before execution.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
