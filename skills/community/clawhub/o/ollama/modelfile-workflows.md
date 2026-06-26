# Modelfile Workflows

## When to Reach for a Modelfile

Use a Modelfile when prompt behavior, context size, stop tokens, or adapters should be reproducible across sessions.
Do not keep those decisions hidden in application code if they need to be shared or debugged later.

## Minimal Pattern

```text
FROM MODEL:TAG
PARAMETER temperature 0
PARAMETER num_ctx 32768
SYSTEM You are a concise coding assistant.
```

Build and run it with a new explicit name:

```bash
ollama create my-coder -f ./Modelfile
ollama run my-coder
```

## Inspection Workflow

Start from the current live definition before editing:

```bash
ollama show --modelfile MODEL:TAG
```

Use that output to see inherited template, stops, and defaults before creating a derived model.

## Rules That Prevent Drift

- Pin the base model tag in `FROM` instead of using a floating alias when reproducibility matters.
- Change one thing at a time: context, temperature, template, or adapter.
- If app prompts and model behavior fight each other, inspect the Modelfile before rewriting the application.
- Use a new model name for meaningful behavior changes so rollback is easy.

## Context Control

If a coding or agent tool needs a larger context window, set it explicitly in the Modelfile or runtime options and verify the load with `ollama ps`.
Larger context costs memory, so treat every increase as a hardware decision.
