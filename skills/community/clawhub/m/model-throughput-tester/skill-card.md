## Description:

Benchmark LLM model throughput by measuring tokens per second, latency, and output speed through auto mode with OpenClaw or direct API mode for OpenAI-compatible endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsag1](https://clawhub.ai/user/tsag1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to benchmark and compare LLM response throughput, latency, token output, and error rate before selecting or switching models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API mode can send API keys and benchmark prompts to any configured endpoint, including insecure HTTP endpoints.

Mitigation: Prefer auto mode when possible; in API mode, use trusted HTTPS endpoints and avoid placing real keys directly in shell history.

Risk: Generated reports can store the benchmark prompt and API URL locally.

Mitigation: Use non-sensitive benchmark prompts and review generated Markdown or CSV reports before sharing them.

Risk: Auto mode estimates token counts and cannot enforce the max token limit, which can make slow models appear to fail by timeout.

Mitigation: Use API mode for precise completion-token counts and max-token control, or raise the timeout and use a shorter prompt for slow models in auto mode.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tsag1/skills/model-throughput-tester)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Release evidence](evidence.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Terminal summary text plus a Markdown throughput report, with optional CSV output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Auto mode estimates token counts and excludes warmup from summary by default; API mode uses reported completion tokens when available.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
