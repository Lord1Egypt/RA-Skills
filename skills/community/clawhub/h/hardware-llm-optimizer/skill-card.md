## Description:

Auto-detects PC CPU, GPU, RAM, and VRAM to recommend runnable local LLM sizes, quantization settings, deployment tools, and bottleneck fixes with Chinese-language output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smseow001](https://clawhub.ai/user/smseow001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and local LLM users use this skill to inspect a PC's available CPU, memory, GPU, and VRAM, then choose practical model sizes, quantization levels, and local deployment tools. It is especially oriented toward Chinese-speaking users who want quick hardware-fit guidance for running LLMs locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects basic local hardware details and may run nvidia-smi when available.

Mitigation: Review this disclosed local inspection behavior before use and run the skill only in environments where local hardware inventory checks are acceptable.

Risk: The skill depends on psutil for hardware detection.

Mitigation: Install psutil in a virtual environment, avoid administrator or root-level pip installs, and use pinned dependencies when reproducibility matters.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese-language text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports local hardware capacity, model-size recommendations, quantization guidance, deployment tool suggestions, bottleneck analysis, and optimization tips.]

## Skill Version(s):

1.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
