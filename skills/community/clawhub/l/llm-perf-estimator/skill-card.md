## Description: <br>
Estimate LLM inference performance metrics including TTFT, decode speed, and VRAM requirements based on model architecture, GPU specs, and quantization format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangyu68](https://clawhub.ai/user/zhangyu68) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to estimate single-GPU LLM inference latency, decode throughput, and VRAM needs before choosing a model, GPU, sequence length, and quantization format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A local config file path could expose unrelated private files if the user provides the wrong file. <br>
Mitigation: Provide only the intended model config.json or paste the relevant public model configuration. <br>
Risk: Performance and memory results are estimates and may differ from real framework behavior. <br>
Mitigation: Review the stated assumptions and validate important deployment decisions with benchmark runs on the target stack. <br>


## Reference(s): <br>
- [Hugging Face model config](https://huggingface.co/{org}/{model}/blob/main/config.json) <br>
- [ModelScope model config](https://modelscope.cn/models/{org}/{model}/file/view/master/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown report with configuration, VRAM, performance, assumptions, and caveats sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Estimates depend on supplied model architecture, GPU specifications, quantization format, and framework assumptions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
