# Anthropic Claude profile

- Start from clear success criteria and a way to evaluate them.
- Use clear, direct instructions and enough context for the task.
- Assign a role when domain perspective changes the answer.
- Use XML tags to separate instructions, context, examples, and variable inputs when the separation improves clarity. Keep tag names consistent.
- Add a few relevant, diverse examples when format, classification boundaries, or style is difficult to describe; do not add examples mechanically.
- State the desired output format and constraints explicitly.
- For long context, make the task and evidence boundaries unmistakable.
- For agentic work, specify tools, permissions, persistence, recovery, verification, and completion criteria without over-scaffolding.
- Do not add assistant-response prefills for newer Claude variants that do not support them. If the user's existing stack uses prefills, flag migration instead of silently preserving an incompatible pattern.
- Do not request disclosure of private chain-of-thought. Ask for concise reasoning summaries or evidence when needed.

## Official sources

- Prompting best practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Prompt engineering overview: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview
- Console prompting tools: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-tools

