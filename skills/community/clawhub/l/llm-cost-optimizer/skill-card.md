## Description: <br>
Analyze LLM API usage logs to suggest cost optimizations, including model downgrades, caching opportunities, and prompt compression across OpenAI, Anthropic, Google, DeepSeek, and Meta models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evezart](https://clawhub.ai/user/evezart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering teams, and operations teams use this skill to analyze LLM usage logs, estimate spend by model and task, and identify downgrade, caching, or prompt-compression opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Usage logs may contain operational metadata such as model names, token counts, task types, timestamps, or session IDs. <br>
Mitigation: Review and redact sensitive log fields before analysis; the reviewed artifacts process the provided data locally and do not show upload or credential behavior. <br>
Risk: Cost-saving recommendations are heuristic and may not preserve quality for every workload. <br>
Mitigation: Validate model downgrades, caching changes, and prompt-compression suggestions against representative production tasks before broad rollout. <br>
Risk: Hard-coded model pricing can become outdated. <br>
Mitigation: Confirm current provider pricing before using estimated savings for purchasing, budgeting, or production migration decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evezart/llm-cost-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON-style analysis results and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local cost summaries, optimization recommendations, estimated savings, confidence values, and suggested actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
