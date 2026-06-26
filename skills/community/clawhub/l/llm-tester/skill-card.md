## Description: <br>
LLM Tester compares multiple LLM models across sample files and prompt templates, recording latency, token usage, success rates, and JSON benchmark reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuzhihui886](https://clawhub.ai/user/yuzhihui886) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and prompt engineers use this skill to compare LLM behavior, speed, token use, and success rates on the same samples and prompts. It supports model selection, prompt optimization, cost estimation, and repeatable benchmark reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected sample files and prompt templates are sent to the configured LLM provider. <br>
Mitigation: Use only data approved for the configured provider and avoid benchmarking sensitive or confidential content unless that provider is trusted for the data. <br>
Risk: DASHSCOPE_API_KEY authorizes external model calls, and LLM_API_BASE can redirect requests to another endpoint. <br>
Mitigation: Protect the API key, avoid logging it, and override LLM_API_BASE only for trusted endpoints. <br>
Risk: Generated benchmark reports may contain prompts, model outputs, token counts, and business-sensitive evaluation results. <br>
Mitigation: Store reports in an appropriate private location and avoid publishing them when they contain sensitive prompts, outputs, or business data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yuzhihui886/llm-tester) <br>
- [DashScope-compatible chat completions endpoint](https://coding.dashscope.aliyuncs.com/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, json, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local JSON benchmark report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include timestamp, benchmark configuration, per-model summaries, and per-sample results.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
