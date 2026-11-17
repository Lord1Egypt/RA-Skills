## Description:

Hardware LLM Optimizer v2 uses llmfit to inspect CPU, GPU, RAM, and VRAM and recommend local LLMs, quantization choices, estimated speed, and fit levels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smseow001](https://clawhub.ai/user/smseow001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and local AI users use this skill to decide which LLMs and quantization settings are appropriate for available CPU, GPU, RAM, and VRAM. It also supports hardware simulation, usage-based filtering, and command examples for local model workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill references a remote curl-to-shell installer that can execute arbitrary local code.

Mitigation: Review the skill before installing; independently trust and verify the llmfit source, and prefer a pinned, checksummed, or signed release.

Risk: The skill inspects local CPU, RAM, GPU, VRAM, driver, and platform information.

Mitigation: Run it only in environments where local hardware inspection is acceptable, and review generated recommendations before acting on them.

## Reference(s):

- [Hardware LLM Optimizer v2 ClawHub page](https://clawhub.ai/smseow001/skills/hardware-llm-optimizer-v2)
- [llmfit installer](https://llmfit.axjns.dev/install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON output from llmfit]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include hardware inspection results, model recommendations, quantization guidance, fit scores, and speed estimates.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
