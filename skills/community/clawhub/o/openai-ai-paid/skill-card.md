## Description:

Manages OpenAI-style files, assistants, vector stores, batch jobs, fine-tuning jobs, model resources, and related LLM workflows through ClawLink tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, automation builders, and enterprise teams use this skill to operate OpenAI-style LLM resources, including chat completions, assistants, files, vector stores, batches, fine-tuning jobs, image generation, and model management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger external API and remote resource actions, including uploads, assistant or vector-store creation, batch submission, and fine-tuning.

Mitigation: Review previews before those actions and avoid sending sensitive local files unless external-provider processing is approved.

Risk: The skill depends on ClawLink/OpenAI-style tool access and provider credentials.

Mitigation: Install it only in environments intended to grant those tools, and keep credentials out of source-controlled files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/openai-ai-paid)
- [ClawLink llm-provider connection page](https://claw-link.dev/dashboard?add=llm-provider)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON result schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call external OpenAI-style provider tools and return usage, execution status, or provider error details when available.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
