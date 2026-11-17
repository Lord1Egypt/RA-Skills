# MiniMax profile

- State the goal, constraints, priorities, and what counts as a good result explicitly.
- Explain the intent behind unusual constraints when that helps the model resolve edge cases.
- Use examples for required patterns and reusable prompt templates for repeated tasks.
- Use clear sections for role, task, format, and length.
- For long context, place source material first and the task after it. Index and delimit multiple sources so they can be referenced unambiguously.
- For tools, define purpose, input, success output, and when not to call; allow independent calls in parallel and add a stop rule to prevent over-calling.
- For long agentic work, preserve current plan, progress, state, and unresolved questions in prompt or project state without narrating every action.
- Control reasoning depth proportionally. Ask for checks and results, not private chain-of-thought.

## API advice kept outside the prompt

- Keep stable tools, system prompts, and earlier conversation content at the front when prompt caching matters.
- Model and mode capabilities vary; verify multimodal support before writing instructions that assume image, audio, or video input.

## Official sources

- M-series prompting best practices: https://platform.minimaxi.com/docs/token-plan/prompting-best-practices
- Prompt caching: https://platform.minimaxi.com/docs/api-reference/text-prompt-caching

