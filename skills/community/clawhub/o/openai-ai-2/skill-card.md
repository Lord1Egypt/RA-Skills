## Description:

Manages llm-provider files, assistants, vector stores, batches, fine-tuning jobs, images, and model resources through ClawLink-style provider tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation teams use this skill to operate OpenAI-style provider resources, including model calls, assistants, vector stores, file uploads, batch jobs, image generation, and fine-tuning workflows. It is intended for agent-assisted API operations where users can review sensitive or write actions before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents toward write actions that create or change remote provider resources.

Mitigation: Confirm upload, batch, assistant, vector-store, image, and fine-tuning actions before execution, and preview tool parameters when available.

Risk: The skill examples include uploading local files and connecting them to vector stores, which may expose private documents to the connected provider account.

Mitigation: Use only approved input files and avoid private, regulated, or confidential documents unless the account and data handling path are authorized.

Risk: The skill requests broad read, exec, and write capabilities for provider-resource automation.

Mitigation: Run it in a scoped workspace and review shell commands, configuration changes, and remote API operations before allowing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/openai-ai-2)
- [llm-provider ClawLink connection dashboard](https://claw-link.dev/dashboard?add=llm-provider)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe or propose remote API actions, including uploads, assistant setup, vector-store changes, batch jobs, image generation, and fine-tuning operations.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
