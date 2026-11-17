# Google Gemini profile

- Be precise and direct. Define ambiguous terms and parameters.
- Use one consistent structure: Markdown headings or XML-style tags. Do not mix delimiter styles without need.
- Put critical role, behavior, constraint, and output instructions in the system instruction or near the beginning.
- For large context, put the context first and the specific task or question at the end, with a clear transition such as `Based on the information above`.
- Treat text, images, audio, and video as explicit inputs and name how each should be used.
- Specify verbosity when a detailed or conversational answer is needed; Gemini 3 models tend to answer directly.
- Use examples or a response prefix only when they materially clarify the expected output. Prefer native structured output for complex JSON schemas.
- Do not ask the model to expose internal step-by-step thinking. Ask it to validate or provide a concise rationale.

## API advice kept outside the prompt

- For Gemini 3.x, keep sampling parameters at their defaults unless representative tests justify a change; Google's guide warns that changing temperature, top-p, or top-k can degrade some complex tasks.
- Use grounding for current or obscure facts and code execution for arithmetic or counting when those tools are available and the task requires them.

## Official sources

- Prompt design strategies: https://ai.google.dev/gemini-api/docs/prompting-strategies
- Gemini 3 developer guide: https://ai.google.dev/gemini-api/docs/gemini-3

