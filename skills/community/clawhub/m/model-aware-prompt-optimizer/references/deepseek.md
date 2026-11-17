# DeepSeek profile

- Use clear task, context, constraints, and output requirements. Apply the universal structure rather than inventing a provider-specific template.
- Distinguish thinking and non-thinking mode when it affects latency, tool use, or API behavior.
- Do not add instructions to print chain-of-thought. Treat returned reasoning fields as runtime state, not user-facing prompt content.
- For strict JSON output, explicitly use the word `json` in the prompt and provide a compact example or expected shape. Preserve required fields exactly.
- For tool use, describe required arguments and failure behavior; use strict function schemas through the API when appropriate rather than restating the whole schema in prose.

## API advice kept outside the prompt

- On current DeepSeek V4 models, thinking mode is controlled with the documented `thinking` setting and effort setting. Do not simulate it by adding `think step by step`.
- In thinking mode, sampling penalties and temperature/top-p may be unsupported or ineffective; check the exact current model.
- JSON mode also requires the API `response_format` setting and a sufficient output-token limit.
- When a thinking-mode tool call occurs, preserve the returned reasoning state in subsequent API turns as required by the official guide.

## Official sources

- Thinking mode: https://api-docs.deepseek.com/guides/thinking_mode
- JSON output: https://api-docs.deepseek.com/guides/json_mode/
- Tool calls: https://api-docs.deepseek.com/guides/tool_calls
- Prompt library: https://api-docs.deepseek.com/prompt-library

