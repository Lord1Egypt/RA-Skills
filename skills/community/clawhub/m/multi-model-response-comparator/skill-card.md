## Description:

Compare responses from multiple AI models for the same task and summarize differences in quality, style, speed, and likely cost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xujfcn](https://clawhub.ai/user/xujfcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, evaluators, and prompt engineers use this skill to compare 2-4 model outputs for the same prompt and choose models by quality, style, correctness, likely cost, and likely latency tradeoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and model outputs may be sent to whichever model provider or OpenAI-compatible runtime the user configures.

Mitigation: Review provider data-handling policies before sending sensitive prompts or outputs through the comparison workflow.

Risk: Provider charges, latency, and exact pricing can vary, and the skill only supports likely or expected cost/latency notes unless the user provides metrics.

Mitigation: Use measured provider pricing and latency data when exact cost or performance claims are needed.

## Reference(s):

- [Comparison Rubric](references/comparison-rubric.md)
- [Example Prompts](references/example-prompts.md)
- [Crazyrouter](https://crazyrouter.com)
- [Crazyrouter OpenAI-Compatible Runtime](https://crazyrouter.com/v1)
- [ClawHub Skill Page](https://clawhub.ai/xujfcn/skills/multi-model-response-comparator)
- [Publisher Profile](https://clawhub.ai/user/xujfcn)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown comparison report with model strengths, weaknesses, use-case fit, cost/latency sensitivity, and a final recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill asks the agent to label inferred cost or latency as likely or expected unless the user provides exact metrics.]

## Skill Version(s):

0.2.0 (source: release evidence, artifact metadata, catalog.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
