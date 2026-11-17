## Description:

Shadow-test local Ollama models against a cloud baseline with a multi-judge ensemble and promote local models when they statistically prove equivalent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up evidence-based evaluation and routing for local Ollama models against cloud LLM baselines across defined task types such as summarize, classify, extract, format, analyze, and RAG.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task prompts and candidate outputs may be sent to Anthropic, OpenAI, or Gemini for baseline generation and sampled judge scoring.

Mitigation: Confirm the data is appropriate for those providers before use, and use API keys tied to accounts and policies you control.

Risk: Score history is stored locally and may contain prompts, outputs, or evaluation metadata.

Mitigation: Store score files in an access-controlled location and apply retention rules appropriate for the evaluated workload.

Risk: An optional scheduled accumulator loop can repeatedly run model evaluations and incur provider costs.

Mitigation: Review the cadence, sampling rate, budget, and provider quotas before enabling a production schedule.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/llm-eval-router)
- [Publisher profile](https://clawhub.ai/user/nissan)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with YAML, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance includes local score storage patterns, API usage expectations, model promotion criteria, and routing policy examples.]

## Skill Version(s):

1.2.2 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
