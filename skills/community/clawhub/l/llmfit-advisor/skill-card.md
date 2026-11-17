## Description:

Guides an agent to use llmfit for hardware-aware local LLM model and quantization recommendations across coding, chat, reasoning, and general use cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bshaot](https://clawhub.ai/user/bshaot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and local LLM users use this skill to select suitable local models, quantization settings, and runtimes based on available CPU, RAM, GPU memory, context length, and task type.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide use of llmfit commands that inspect local hardware details such as CPU, RAM, and GPU information.

Mitigation: Tell users what hardware details will be inspected and avoid sharing the resulting system profile beyond the local recommendation task.

Risk: The artifact includes Docker and update-script examples that may fetch upstream images or code.

Mitigation: Use pinned, verified Docker image tags or digests and review upstream update scripts before running them.

## Reference(s):

- [Llmfit Documentation](https://github.com/AlexsJones/llmfit)
- [Hugging Face Model Hub](https://huggingface.co)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell command examples and JSON output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local hardware information and llmfit JSON recommendation output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
