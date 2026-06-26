## Description: <br>
Compare responses from multiple AI models for the same task and summarize differences in quality, style, speed, and likely cost. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xujfcn](https://clawhub.ai/user/xujfcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, evaluators, and model operations teams use this skill to compare 2-4 model responses to the same prompt and choose the best model for a specific workflow. It is useful for model selection, prompt benchmarking, and quality-cost tradeoff analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and model outputs may be sent to an external OpenAI-compatible provider when using the included provider example. <br>
Mitigation: Use appropriate API keys, follow provider terms, and avoid sending sensitive prompts unless the provider is approved for that data. <br>
Risk: Cost and latency comparisons can be misleading when measured data is not provided. <br>
Mitigation: Label cost and latency as likely or expected unless the user supplies exact metrics. <br>


## Reference(s): <br>
- [Comparison Rubric](references/comparison-rubric.md) <br>
- [Example Prompts](references/example-prompts.md) <br>
- [Crazyrouter](https://crazyrouter.com) <br>
- [Crazyrouter OpenAI-Compatible Base URL](https://crazyrouter.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown comparison report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the same task and success criteria across compared models; cost and latency are labeled as likely or expected unless user-supplied metrics are available.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
