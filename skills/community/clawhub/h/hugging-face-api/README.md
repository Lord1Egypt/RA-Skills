# Hugging Face Skill — Overview

This skill teaches an agent **how and when** to use the Hugging Face MCP server. It is a written playbook, not an executable: it guides the agent that drives the 7 MCP tools.

---

## Contents

| File | What it covers |
|------|----------------|
| `SKILL.md` | The main playbook (17 numbered sections). Start here. |
| `reference/apis-and-tools.md` | Hub vs router; the 7 tools and their endpoints. |
| `reference/models-and-tasks.md` | Popular chat/embedding models; pipeline tasks; finding supported models. |
| `reference/parameters.md` | Chat and search parameters. |
| `reference/common-errors.md` | Error shapes and reactions. |
| `reference/best-practices.md` | Discovery-free, cost, licensing, security. |
| `recipes/find-and-run-model.md` | Discover a model and run chat. |
| `recipes/build-embeddings.md` | Build embeddings for RAG. |
| `recipes/dataset-discovery.md` | Find and inspect datasets. |
| `prompts/model-selection.md` | Reusable model-selection prompt. |
| `prompts/cost-control.md` | Reusable cost-control prompt. |
| `tests/skill-evaluation.md` | Evaluation checklist. |
| `tests/failure-cases.md` | Bad behaviors and corrections. |

---

## Two big ideas

1. **Hub discovery is free; inference is billed.** Always discover and confirm support before spending on `hf_chat` / `hf_embeddings`.
2. **Never expose the `hf_` token.** Treat it like a password.

For the executable side (installation, configuration, tool schemas), see the MCP docs under `../mcp/`.
