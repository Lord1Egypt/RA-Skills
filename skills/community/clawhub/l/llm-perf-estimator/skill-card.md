## Description:

Estimate LLM inference performance metrics including TTFT, decode speed, and VRAM requirements based on model architecture, GPU specs, and quantization format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyu68](https://clawhub.ai/user/zhangyu68)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to estimate single-GPU LLM inference latency, decode throughput, and memory requirements before selecting model, GPU, context length, and quantization settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A local config.json shared with the agent may contain environment-specific paths or unrelated details.

Mitigation: Review the config file before sharing it and remove fields that are not needed for architecture and performance estimation.

Risk: Estimated TTFT, decode speed, and VRAM needs may differ from actual deployed performance because framework behavior and hardware utilization vary.

Mitigation: Use the report for planning and compare against benchmark measurements before making capacity, deployment, or purchasing decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangyu68/skills/llm-perf-estimator)
- [Hugging Face model config](https://huggingface.co/{org}/{model}/blob/main/config.json)
- [ModelScope model config](https://modelscope.cn/models/{org}/{model}/file/view/master/config.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with summary tables, estimates, assumptions, and caveats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include intermediate calculations when requested; estimates are approximate and rounded for readability.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
