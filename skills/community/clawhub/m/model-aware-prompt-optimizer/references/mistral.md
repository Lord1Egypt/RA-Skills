# Mistral profile

- Use a clear system prompt for stable behavior and separate it from the user's task and data.
- Make instructions explicit, use role separation correctly, and format the prompt consistently.
- Add few-shot examples when they clarify classification, transformation, or output behavior.
- Specify output format, allowed labels, length, and failure behavior where required.
- Apply the universal profile to agent, evidence, permission, validation, and stop rules.
- Do not manually add tokenizer control tokens when an SDK or serving layer already applies the selected model's chat template.

## Official sources

- Model best practices: https://docs.mistral.ai/models/best-practices
- Prompt engineering: https://docs.mistral.ai/models/best-practices/prompt-engineering
- Prompting capabilities cookbook: https://docs.mistral.ai/resources/cookbooks/mistral-prompting-prompting_capabilities

