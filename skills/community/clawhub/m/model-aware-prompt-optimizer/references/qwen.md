# Alibaba Qwen profile

- Make the task clear, specific, and unambiguous. Include necessary purpose, context, constraints, and expected output.
- Use a system message for stable role, behavior, and constraints when the selected Qwen variant supports it.
- Separate fixed prompt instructions from dynamic template variables.
- Use examples to clarify style or output boundaries, and state structured-output requirements explicitly.
- Do not assume all Qwen-family reasoning or multimodal variants handle system messages, thinking controls, or structured output identically. Check the exact model when those features matter.

## API advice kept outside the prompt

- Adjust one sampling parameter at a time when testing; parameter support and recommended values vary by model and mode.
- Some Qwen thinking variants cannot disable thinking, and some structured-output combinations have mode restrictions.
- When JSON mode requires the prompt to mention `json`, preserve that keyword and specify the expected shape.

## Official sources

- Prompt engineering guide: https://help.aliyun.com/zh/model-studio/prompt-engineering-guide
- Text generation and message roles: https://help.aliyun.com/zh/model-studio/text-generation
- OpenAI-compatible Chat Completions: https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions

