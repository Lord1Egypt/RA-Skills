## Description:

Find the best local LLM for your machine. Tests speed, quality and RAM fit, then tells you if a model is worth running on your hardware.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thebluehouse75](https://clawhub.ai/user/thebluehouse75)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and local LLM users use this skill to benchmark models on their own hardware, compare speed, quality, and memory fit, and decide whether a model is practical to run locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install a global npm CLI.

Mitigation: Install only if comfortable adding the MetriLLM CLI globally, preferably without sudo and after checking the package source.

Risk: The optional leaderboard share command publishes benchmark results and hardware details.

Mitigation: Use the share command only when intentionally publishing model name, scores, CPU, RAM, and GPU information to the public leaderboard.

## Reference(s):

- [MetriLLM source repository](https://github.com/MetriLLM/metrillm)
- [MetriLLM community leaderboard](https://metrillm.dev)
- [Ollama](https://ollama.com)
- [LM Studio](https://lmstudio.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and benchmark interpretation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide the agent to run MetriLLM commands that produce JSON benchmark results.]

## Skill Version(s):

0.2.11 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
