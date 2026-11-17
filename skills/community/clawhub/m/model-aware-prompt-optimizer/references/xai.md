# xAI Grok profile

xAI's public documentation provides capability and API guidance rather than a broad model-specific prompt-engineering template. Apply the universal profile and avoid inventing a special Grok syntax.

- State the task, evidence needs, tool scope, required output, and completion conditions directly.
- For reasoning-heavy requests, ask for the result, proof, checks, or concise rationale rather than hidden reasoning traces.
- When web, X search, code execution, or client-side tools are available, state which evidence or action requires which tool and how to handle failure.
- Keep static system instructions and examples stable in deployed prompt stacks when prompt caching matters; append conversation turns instead of rewriting earlier messages.

## API advice kept outside the prompt

- `reasoning_effort` is an API control on supported Grok models and should not be encoded as verbose reasoning instructions in the prompt.
- Reasoning-model parameter support varies; do not recommend sampling or stop parameters without checking the exact model documentation.
- Prompt caching benefits from stable prefixes and a stable conversation or cache key.

## Official sources

- Reasoning: https://docs.x.ai/developers/model-capabilities/text/reasoning
- Prompt caching best practices: https://docs.x.ai/developers/advanced-api-usage/prompt-caching/best-practices
- Tool advanced usage: https://docs.x.ai/developers/tools/advanced-usage

