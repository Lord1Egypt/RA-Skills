## Description: <br>
Benchmarks LLM throughput by measuring tokens per second, latency, output speed, and error rate in OpenClaw auto mode or OpenAI-compatible API mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tsag1](https://clawhub.ai/user/tsag1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI practitioners use this skill to compare model throughput and latency before selecting or changing LLM endpoints. It supports quick OpenClaw auto-mode tests and direct OpenAI-compatible API benchmarks across one or more models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API mode can send prompts to a user-provided endpoint with a user-provided API key. <br>
Mitigation: Use trusted endpoints, use appropriately scoped keys, and prefer auto mode when an API key is not needed. <br>
Risk: Generated reports can include the model, API URL, test prompt, and benchmark results. <br>
Mitigation: Use non-sensitive test prompts and review or redact reports before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tsag1/model-throughput-tester) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown benchmark report with terminal status output and optional CSV] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include model, API URL when supplied, test prompt, latency, output token counts or estimates, tokens per second, and error rate.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
