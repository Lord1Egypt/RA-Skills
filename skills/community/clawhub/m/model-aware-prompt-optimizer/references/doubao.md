# ByteDance Doubao / Seed profile

The public Volcano Engine documentation exposes general prompt best practices and prompt-optimization workflows, but model-variant-specific text prompting rules are less centralized. Apply the universal profile conservatively.

- Define role, task, necessary context, constraints, expected output, and evaluation criteria clearly.
- Separate fixed instructions from retrieved context and user input with clear delimiters.
- For RAG, identify the retrieved context as evidence, define whether outside knowledge is allowed, and state the fallback when the context is insufficient.
- Use examples only when they establish a required output pattern or decision boundary.
- Treat model switching in Ark as meaningful: do not assume a prompt tuned for another provider needs no evaluation on Doubao or Seed.

## API advice kept outside the prompt

- Keep model parameters and platform prompt-optimization settings outside the copy-ready prompt.
- Validate the rewrite on representative inputs using the selected model and version.

## Official sources

- Volcano Ark documentation and Prompt Best Practices index: https://www.volcengine.com/docs/82379/
- Prompt generation and optimization workflow: https://www.volcengine.com/docs/82379/1399496

