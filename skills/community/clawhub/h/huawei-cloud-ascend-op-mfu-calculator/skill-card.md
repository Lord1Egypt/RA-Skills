## Description: <br>
Calculates Machine FLOP Utilization for Ascend NPU operators such as matmul, GEMM, and FlashAttention, with formulas, derivation steps, and performance interpretation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaweiclouddev](https://clawhub.ai/user/huaweiclouddev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and performance engineers use this skill to calculate MFU for Ascend NPU operators, compare operator implementations, interpret utilization, and identify optimization opportunities from dimensions, execution time, and peak FLOPS inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MFU results can be inaccurate when operator dimensions, execution time, precision, or peak FLOPS values are wrong or stale. <br>
Mitigation: Verify profiler inputs and hardware peak FLOPS against current official documentation before relying on the result. <br>
Risk: Profiler CSVs or operator details may contain workload information the user does not want analyzed. <br>
Mitigation: Only provide profiler data and operator details that are appropriate to share with the agent. <br>


## Reference(s): <br>
- [Huawei Cloud Ascend Operator MFU Calculator](https://clawhub.ai/huaweiclouddev/huawei-cloud-ascend-op-mfu-calculator) <br>
- [MFU Calculation Methodology](references/mfu-calculation-methodology.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Ascend 910B Series Technical Specifications](https://e.huawei.com/cn/products/computing/ascend-910) <br>
- [FlashAttention Technical Paper](https://arxiv.org/abs/2205.14135) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, code] <br>
**Output Format:** [Markdown with formulas, calculation steps, short Python snippets, and optimization guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided operator dimensions, execution time, hardware peak FLOPS, and optional device details; outputs should be reviewed for input and hardware-spec accuracy.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
