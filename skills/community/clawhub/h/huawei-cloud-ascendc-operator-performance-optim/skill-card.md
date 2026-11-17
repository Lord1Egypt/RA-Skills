## Description:

Develops and optimizes custom AscendC operators for Ascend NPUs by analyzing bottlenecks, applying memory, compute, and data-layout techniques, and validating performance and correctness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to optimize performance-critical AscendC custom operators, identify operator bottlenecks, apply Ascend NPU memory/compute/data-layout optimizations, and validate accuracy and speedup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read and modify local AscendC operator projects and run build or profiling commands.

Mitigation: Review the selected operator directory first, work in a controlled workspace, and keep a backup before allowing changes or command execution.

Risk: The profiling scripts remove existing OPPROF_* directories in the selected operator directory.

Mitigation: Copy or archive existing OPPROF_* profiling results before running the scripts, or run profiling in a fresh working directory.

Risk: The troubleshooting material includes broad permission guidance for /tmp/opprof.

Mitigation: Avoid chmod 777; use a private user-owned profiling directory with restrictive permissions.

Risk: Optimization guidance or code changes can produce incorrect results or misleading performance gains.

Mitigation: Validate against a baseline implementation, compare numerical accuracy within the stated tolerances, and rerun before/after profiling on realistic inputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-ascendc-operator-performance-optim)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Verification Methods](references/verification-method.md)
- [Troubleshooting](references/troubleshooting.md)
- [AscendC Operator Code Generation Reference Documents Load Guide](references/ascendc-api/GUIDE.md)
- [Tiling Optimization Reference](references/tiling-prof.md)
- [Data Copy Optimization Reference](references/data-copy-prof.md)
- [API Usage Optimization Reference](references/api-usage-prof.md)
- [Memory Optimization Reference](references/memory-prof.md)
- [Pipeline Optimization Reference](references/pipeline-prof.md)
- [Scalar Optimization Reference](references/scalar-prof.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and C++ code blocks, profiling report descriptions, and optimization recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide local compilation and profiling workflows and produce terminal comparison output or paths to generated profiling artifacts.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
