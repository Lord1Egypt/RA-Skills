# Moonshot Kimi profile

- Write clear instructions with the important details and context the model would otherwise need to guess.
- Assign a role when expertise or perspective improves accuracy.
- Use triple quotes, XML tags, or section headings to distinguish instructions from source text and variable input.
- Define steps when the task genuinely has an ordered transformation; do not add ceremonial steps to simple tasks.
- Provide a few-shot example when it is more efficient than describing a difficult style or output boundary.
- Specify length in sentences, paragraphs, or bullet counts when possible; exact word counts are less reliable.
- For grounded answers, state that the supplied reference controls the answer and define the fallback when the answer is absent.
- For complex task families, classify the request before applying scenario-specific instructions when that reduces irrelevant rules.
- For long conversations, summarize or filter earlier history. For very long documents, use chunked summaries and recursively aggregate them when the whole document cannot be handled at once.

## Official source

- Best practices for prompts: https://platform.moonshot.ai/docs/guide/prompt-best-practice

