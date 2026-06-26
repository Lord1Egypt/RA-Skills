# OpenAI Skill

This skill teaches an agent how to use the **OpenAI API** (via the [OpenAI MCP server](../mcp/README.md)) **correctly, safely, and cheaply**.

> ⚠️ OpenAI calls (chat, responses, embeddings, images, audio) are **billed**. Moderation and model listing are free. Cost discipline is the core of this skill.

## Start here

- **[SKILL.md](SKILL.md)** — the main, numbered operating guide (model selection, cost control, error handling, safety, security). **Read this first.**

## Reference

- [reference/models.md](reference/models.md) — model families, cost/quality tiers, which model for which task.
- [reference/endpoints.md](reference/endpoints.md) — the 7 tools + generic passthrough catalog.
- [reference/parameters.md](reference/parameters.md) — common chat/responses/embeddings parameters.
- [reference/common-errors.md](reference/common-errors.md) — error codes and reactions.
- [reference/best-practices.md](reference/best-practices.md) — model choice, cost, caching, moderation, structured output, security.

## Recipes

- [recipes/chat-completion.md](recipes/chat-completion.md)
- [recipes/rag-embeddings.md](recipes/rag-embeddings.md)
- [recipes/structured-extraction.md](recipes/structured-extraction.md)

## Prompts

- [prompts/model-selection.md](prompts/model-selection.md)
- [prompts/cost-control.md](prompts/cost-control.md)

## Tests

- [tests/skill-evaluation.md](tests/skill-evaluation.md)
- [tests/failure-cases.md](tests/failure-cases.md)

## Relationship to the MCP server

The **MCP server** provides the callable tools (the hands). This **skill** provides the judgment (the brain): when to call, which model, how to cap cost, how to stay safe. Use both together.

> Verification needed: confirm models and pricing with <https://platform.openai.com/docs/api-reference>.
