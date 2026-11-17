## Description:

Adapts PyTorch VLA models to Ascend NPU by scanning and fixing compatibility issues, applying runtime patches, and providing verification and training templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers adapting PyTorch VLA projects for Huawei Ascend NPUs use this skill to scan and address compatibility issues, apply runtime patches, verify model and data pipelines, and prepare training scripts and an adaptation summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verification permits model-supplied code execution without a separate opt-in.

Mitigation: Require explicit approval for custom model code; use reviewed model repositories in an isolated environment without unrelated secrets, and inspect proposed changes.

Risk: Training disables a network safeguard.

Mitigation: Restore peer allowlisting or restrict training networking.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cloudrobo-npu-patcher)
- [Entry point NPU setup (P_ENT)](references/fix-templates/P_ENT.md)
- [Flash Attention to NPU (P_FLA)](references/fix-templates/P_FLA.md)
- [PyTorch Lightning metrics (P_LTM)](references/fix-templates/P_LTM.md)
- [Random tensor device mismatch (P_RND)](references/fix-templates/P_RND.md)
- [Target computation optimization (P_TGT)](references/fix-templates/P_TGT.md)
- [Tensor indexing vectorization (P_VEC)](references/fix-templates/P_VEC.md)
- [NPU adaptation summary template](templates/ADAPTATION_SUMMARY.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Python code, shell commands, configuration guidance, and Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project-specific adaptation output; requires review and validation against the target model and NPU environment.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
