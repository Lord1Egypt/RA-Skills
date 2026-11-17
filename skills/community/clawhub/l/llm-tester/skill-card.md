## Description:

LLM Tester compares multiple LLM models on shared samples and prompt templates, records latency, token usage, and success rate, and generates a standardized JSON benchmark report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuzhihui886](https://clawhub.ai/user/yuzhihui886)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run repeatable LLM model comparisons against shared text samples and prompt templates for model selection, prompt evaluation, and cost or latency review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials and benchmark sample text are sent to the endpoint configured by LLM_API_BASE.

Mitigation: Use non-sensitive benchmark samples, verify LLM_API_BASE is the intended HTTPS provider endpoint, and use a narrowly scoped API key with spending limits.

Risk: An untrusted shell, CI job, or wrapper could redirect requests by setting LLM_API_BASE.

Mitigation: Run the skill only in controlled environments where LLM_API_BASE cannot be supplied by untrusted configuration.

Risk: The dependency list does not pin package versions.

Mitigation: Review and pin dependencies before using the skill in managed or production environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuzhihui886/skills/llm-tester)
- [Publisher profile](https://clawhub.ai/user/yuzhihui886)
- [Default LLM API endpoint](https://coding.dashscope.aliyuncs.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [CLI guidance, console status text, and JSON benchmark reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports summarize per-model success rate, average latency, token usage, failures, and timeouts for each sample and prompt combination.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
