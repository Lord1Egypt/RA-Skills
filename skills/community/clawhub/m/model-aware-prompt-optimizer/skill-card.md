## Description:

Rewrite, improve, migrate, or adapt an existing user prompt for the specific language model the user is using while preserving intent, facts, variables, constraints, and output requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daiwk](https://clawhub.ai/user/daiwk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and prompt authors use this skill to rewrite or migrate prompts for a target model family while preserving the prompt's facts, variables, constraints, schemas, and output requirements. It is useful for adapting prompts across OpenAI GPT, Claude, Gemini, Grok, DeepSeek, Kimi, Qwen, Doubao/Seed, MiniMax, Mistral, and Llama-style models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A rewritten prompt can preserve sensitive business rules, private data, or tool permissions from the original prompt.

Mitigation: Review the optimized prompt before use, especially when the source prompt includes private data, production permissions, or sensitive operating constraints.

Risk: Model-specific prompt guidance can become stale as provider behavior and API settings change.

Mitigation: Validate the rewritten prompt on representative inputs for the selected target model before relying on it in production.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/daiwk/skills/model-aware-prompt-optimizer)
- [Skill Definition](SKILL.md)
- [Universal Optimization Profile](references/universal.md)
- [OpenAI Profile](references/openai.md)
- [Anthropic Claude Profile](references/anthropic.md)
- [Google Gemini Profile](references/google.md)
- [xAI Grok Profile](references/xai.md)
- [DeepSeek Profile](references/deepseek.md)
- [Moonshot Kimi Profile](references/kimi.md)
- [Alibaba Qwen Profile](references/qwen.md)
- [ByteDance Doubao / Seed Profile](references/doubao.md)
- [MiniMax Profile](references/minimax.md)
- [Mistral Profile](references/mistral.md)
- [Meta Llama Instruct Profile](references/llama.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with a copy-ready optimized prompt and concise notes about changes, assumptions, and optional API settings when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill rewrites prompts as text and does not execute the task contained in the prompt.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
